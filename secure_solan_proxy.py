# secure_solan_proxy.py
# Beveiligde server-side proxy voor Solān Analyzer v3.0
# - Proxy routes: /api/health, /api/analyzer/bias, /api/analyzer/alignment, /api/analyzer/coherence, /api/logs/tail
# - Voegt server-side X-API-Key toe (nooit keys in de browser!)
# - CORS, IP-allowlist, rate limiting, body-size limit, eenvoudige PII-redaction
# - Ideaal om eerst OFFLINE te testen; daarna 1-op-1 naar productie.

import os, re, time, json, asyncio
from typing import Dict, List, Optional
from fastapi import FastAPI, Request, Response, HTTPException, status
from fastapi.middleware.cors import CORSMiddleware
import httpx

# -----------------------------
# Config via env vars
# -----------------------------
ANALYZER_BASE = os.getenv("ANALYZER_BASE", "http://127.0.0.1:8000")  # je Analyzer API (staging/offline)
ANALYST_KEY   = os.getenv("SOLAN_ANALYST_KEY", "analyst-key")        # analyst rol
ADMIN_KEY     = os.getenv("SOLAN_ADMIN_KEY", "admin-key")            # admin rol (logs)
ALLOW_ORIGINS = [o.strip() for o in os.getenv("ALLOW_ORIGINS", "http://localhost:3000,http://127.0.0.1:3000,file://").split(",") if o.strip()]
ALLOW_IPS     = {ip.strip() for ip in os.getenv("ALLOW_IPS", "127.0.0.1,::1").split(",") if ip.strip()}
RATE_LIMIT_PER_MIN = int(os.getenv("RATE_LIMIT_PER_MIN", "60"))
MAX_BODY_BYTES = int(os.getenv("MAX_BODY_BYTES", "200000"))  # ~200KB

# -----------------------------
# Eenvoudige PII-redaction (extra verdedigingslaag)
# -----------------------------
PII_PATTERNS = [
    re.compile(r"\b[\w\.-]+@[\w\.-]+\.\w+\b"),  # emails
    re.compile(r"\b(?:\+?\d{1,3})?[\s\-]?(?:\d{2,4}[\s\-]?){2,4}\d{2,4}\b"),  # phones (rudimentair)
]
def redact(text: str) -> str:
    s = text or ""
    for pat in PII_PATTERNS:
        s = pat.sub("[REDACTED]", s)
    return s

# -----------------------------
# IP & Rate limiting
# -----------------------------
_buckets: Dict[str, Dict[str, int]] = {}  # { key: {"ts": minute_ts, "count": n} }

def client_ip(req: Request) -> str:
    # In productie achter proxy kun je X-Forwarded-For inspecteren (hardenen in Nginx)
    ip = req.client.host if req.client else "unknown"
    return ip

def rate_limit(key: str):
    now = int(time.time() // 60)
    b = _buckets.get(key)
    if not b or b["ts"] != now:
        _buckets[key] = {"ts": now, "count": 0}
        b = _buckets[key]
    b["count"] += 1
    if b["count"] > RATE_LIMIT_PER_MIN:
        raise HTTPException(status_code=429, detail="Rate limit exceeded")

def ensure_ip_allowed(ip: str):
    if ALLOW_IPS and ip not in ALLOW_IPS:
        raise HTTPException(status_code=403, detail="IP not allowed")

# -----------------------------
# App & Middleware
# -----------------------------
app = FastAPI(title="Solān Secure Proxy", version="3.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=ALLOW_ORIGINS if ALLOW_ORIGINS else ["*"],  # Fallback voor staging
    allow_credentials=False,
    allow_methods=["GET", "POST", "OPTIONS"],
    allow_headers=["Content-Type", "Authorization", "X-Requested-With"],
    expose_headers=["Content-Type"],
)

# Security headers middleware
@app.middleware("http")
async def add_security_headers(request, call_next):
    response = await call_next(request)
    response.headers["Strict-Transport-Security"] = "max-age=31536000; includeSubDomains; preload"
    response.headers["X-Content-Type-Options"] = "nosniff"
    response.headers["Referrer-Policy"] = "no-referrer-when-downgrade"
    response.headers["X-Frame-Options"] = "DENY"
    response.headers["X-XSS-Protection"] = "1; mode=block"
    response.headers["Server"] = "Solan-Proxy/3.0"
    return response

# -----------------------------
# Low-level forwarder
# -----------------------------
async def forward_json(method: str, upstream_path: str, body: Optional[dict], key: str) -> Response:
    url = f"{ANALYZER_BASE}{upstream_path}"
    timeout = httpx.Timeout(20.0, connect=10.0)
    async with httpx.AsyncClient(timeout=timeout) as client:
        headers = {"Content-Type": "application/json", "X-API-Key": key}
        if method == "GET":
            r = await client.get(url, headers=headers)
        else:
            r = await client.post(url, headers=headers, content=json.dumps(body or {}))
    return Response(content=r.content, status_code=r.status_code, media_type=r.headers.get("content-type","application/json"))

async def read_json_body(req: Request) -> dict:
    raw = await req.body()
    if len(raw) > MAX_BODY_BYTES:
        raise HTTPException(status_code=413, detail="Payload too large")
    if not raw:
        return {}
    try:
        return json.loads(raw.decode("utf-8"))
    except Exception:
        raise HTTPException(status_code=400, detail="Invalid JSON")

# -----------------------------
# Routes
# -----------------------------
@app.get("/api/health")
async def proxy_health(req: Request):
    ip = client_ip(req)
    ensure_ip_allowed(ip)
    rate_limit(f"health:{ip}")
    # passthrough (geen key nodig)
    return await forward_json("GET", "/health", None, key=ANALYST_KEY)

@app.post("/api/analyzer/bias")
async def proxy_bias(req: Request):
    ip = client_ip(req)
    ensure_ip_allowed(ip)
    rate_limit(f"bias:{ip}")
    body = await read_json_body(req)
    # extra redaction op client-input
    text = str(body.get("text",""))[:8000]
    clean = redact(text)
    return await forward_json("POST", "/analyzer/bias", {"text": clean}, key=ANALYST_KEY)

@app.post("/api/analyzer/alignment")
async def proxy_alignment(req: Request):
    ip = client_ip(req)
    ensure_ip_allowed(ip)
    rate_limit(f"align:{ip}")
    body = await read_json_body(req)
    claims = body.get("claims", {})
    # sanity: laat alleen floats 0..1 door
    safe_claims = {}
    for k,v in (claims or {}).items():
        try:
            fv = float(v)
            fv = 0.0 if fv < 0 else 1.0 if fv > 1 else fv
            safe_claims[str(k)] = fv
        except Exception:
            continue
    return await forward_json("POST", "/analyzer/alignment", {"claims": safe_claims}, key=ANALYST_KEY)

@app.post("/api/analyzer/coherence")
async def proxy_coherence(req: Request):
    ip = client_ip(req)
    ensure_ip_allowed(ip)
    rate_limit(f"coh:{ip}")
    body = await read_json_body(req)
    statements = body.get("statements", [])
    # normaliseer en begrens
    cleaned = [str(s).strip() for s in (statements or []) if str(s).strip()][:50]
    if not cleaned:
        raise HTTPException(status_code=400, detail="No statements")
    return await forward_json("POST", "/analyzer/coherence", {"statements": cleaned}, key=ANALYST_KEY)

@app.get("/api/logs/tail")
async def proxy_logs_tail(req: Request):
    ip = client_ip(req)
    ensure_ip_allowed(ip)
    rate_limit(f"logs:{ip}")
    # admin-only route → gebruik admin key
    return await forward_json("GET", "/logs/tail", None, key=ADMIN_KEY)

@app.post("/api/v1/echo")
async def proxy_echo(req: Request):
    ip = client_ip(req)
    ensure_ip_allowed(ip)
    rate_limit(f"echo:{ip}")
    body = await read_json_body(req)
    return await forward_json("POST", "/v1/echo", body, key=ANALYST_KEY)

# CORS preflight support
@app.options("/api/{path:path}")
async def cors_preflight(path: str):
    """Handle CORS preflight requests"""
    return {"message": "CORS preflight OK"}

# -----------------------------
# Lokal run
# -----------------------------
if __name__ == "__main__":
    # Offline test:
    #   export ANALYZER_BASE=http://127.0.0.1:8000
    #   export SOLAN_ANALYST_KEY=analyst-key
    #   export SOLAN_ADMIN_KEY=admin-key
    #   export ALLOW_ORIGINS=http://localhost:3000
    #   export ALLOW_IPS=127.0.0.1,::1
    #   python secure_solan_proxy.py
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=int(os.getenv("PROXY_PORT","8787")))
