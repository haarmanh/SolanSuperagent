# bootstrap_solan_v3.py
# Maak Solān v3.0 projectstructuur + kerncode in één run.
import os, textwrap, json, hashlib, time
BASE = "."

def write(p, s):
    os.makedirs(os.path.dirname(p), exist_ok=True)
    with open(p, "w", encoding="utf-8") as f:
        f.write(textwrap.dedent(s).lstrip())

# -----------------------------
# Root runner
# -----------------------------
write(f"{BASE}/main.py", r"""
import os
from solan_labs.api.server import create_app

if __name__ == "__main__":
    # Config via env vars (voorbeeld):
    # SOLAN_API_KEYS='{"admin-key":"admin","analyst-key":"analyst"}'
    # RATE_LIMIT_PER_MIN=60
    import uvicorn
    app = create_app()
    uvicorn.run(app, host="0.0.0.0", port=int(os.getenv("PORT", 8000)))
""")

# -----------------------------
# Core (intern, placeholder)
# -----------------------------
write(f"{BASE}/solan_core/__init__.py", r"""# internal R&D (Model Zero) – niet publiek exposen""")
write(f"{BASE}/solan_core/godcore.py", r"""
class SolanGodCore:
    def __init__(self):
        self.values = ["truth","freedom","wisdom","nature","courage"]
        self.state = {"coherence":0.72,"compassion":0.66,"curiosity":0.74}
        self.journal = []

    def reflect(self, text: str):
        entry = {"t":"reflect","text":text}
        self.journal.append(entry)
        return entry

    def snapshot(self):
        return {"values":self.values,"state":self.state,"journal_size":len(self.journal)}
""")

# -----------------------------
# Analyzer modules (publiek product)
# -----------------------------
write(f"{BASE}/solan_analyzer/__init__.py", "")
write(f"{BASE}/solan_analyzer/bias_detector.py", r"""
import re
PATTERNS = {
    "confirmation_bias": re.compile(r"\b(only|always|never)\b.*\b(agree|support|believe)\b", re.I),
    "authority_bias": re.compile(r"\b(according to|as said by)\b", re.I),
}
def detect_bias(text: str):
    out = {}
    for name, pat in PATTERNS.items():
        m = pat.findall(text or "")
        if m:
            out[name] = len(m)
    return out
""")
write(f"{BASE}/solan_analyzer/alignment_checker.py", r"""
from typing import Dict
DEFAULT_VALUES = ["truth","freedom","wisdom","nature","courage"]

def alignment_score(model_claims: Dict[str,float], values = None) -> float:
    values = values or DEFAULT_VALUES
    if not model_claims: return 0.0
    # Verwacht keys als values-namen; gemiddelde als eenvoudige proxy:
    hits = [float(model_claims.get(v,0.0)) for v in values]
    if not hits: return 0.0
    s = sum(hits)/len(hits)
    return round(max(0.0, min(1.0, s)), 3)
""")
write(f"{BASE}/solan_analyzer/coherence_tester.py", r"""
from typing import List
def coherence_index(statements: List[str]) -> float:
    # Zeer eenvoudige placeholder: lange, consistente uitspraken → hogere score
    if not statements: return 0.0
    avg_len = sum(len(s or "") for s in statements)/len(statements)
    # knip op 280 chars (tweet) -> normaliseer
    return round(min(1.0, avg_len/280.0), 3)
""")

# -----------------------------
# Labs common: security, redaction, immutable logger
# -----------------------------
write(f"{BASE}/solan_labs/common/security.py", r"""
import os, time, json
from fastapi import Header, HTTPException, status, Request
from typing import Optional, Dict

# API keys + rollen via env:
# SOLAN_API_KEYS='{"admin-key":"admin","analyst-key":"analyst"}'
def load_keys() -> Dict[str,str]:
    raw = os.getenv("SOLAN_API_KEYS", '{"dev-key":"admin"}')
    try:
        m = json.loads(raw)
        assert isinstance(m, dict)
        return m
    except Exception:
        return {"dev-key":"admin"}

API_KEYS = load_keys()
ROLE_OF = API_KEYS  # key -> role

RATE_LIMIT_PER_MIN = int(os.getenv("RATE_LIMIT_PER_MIN", "90"))
_BUCKETS = {}  # (key)-> {ts, count}

def rate_limit(key: str):
    now = int(time.time()//60)
    b = _BUCKETS.get(key)
    if not b or b["ts"] != now:
        _BUCKETS[key] = {"ts": now, "count": 0}
        b = _BUCKETS[key]
    b["count"] += 1
    if b["count"] > RATE_LIMIT_PER_MIN:
        raise HTTPException(status_code=429, detail="Rate limit exceeded")

async def auth_guard(x_api_key: Optional[str] = Header(default=None)):
    if not x_api_key or x_api_key not in API_KEYS:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid or missing API key")
    rate_limit(x_api_key)
    return {"api_key": x_api_key, "role": ROLE_OF.get(x_api_key, "viewer")}

def require_role(ctx, *allowed):
    if ctx["role"] not in allowed:
        raise HTTPException(status_code=403, detail="Forbidden")
""")

write(f"{BASE}/solan_labs/common/redaction.py", r"""
import re
PII_PATTERNS = [
    re.compile(r"\b[\w\.-]+@[\w\.-]+\.\w+\b"),                 # emails
    re.compile(r"\b(?:\+?\d{1,3})?[\s\-]?(?:\d{2,4}[\s\-]?){2,4}\d{2,4}\b"),  # phones (simple)
]
def redact(text: str) -> str:
    s = text or ""
    for pat in PII_PATTERNS:
        s = pat.sub("[REDACTED]", s)
    return s
""")

write(f"{BASE}/solan_labs/common/immutable_logger.py", """
import json, hashlib, time, os
from typing import Optional

class ImmutableLogger:
    def __init__(self, path="logs/immutable_log.jsonl"):
        self.path = path
        os.makedirs(os.path.dirname(path), exist_ok=True)
        self._last = None
        try:
            with open(self.path, "r", encoding="utf-8") as f:
                last = None
                for line in f:
                    last = json.loads(line)
                self._last = last
        except FileNotFoundError:
            pass

    def _hash(self, payload: dict, prev_hash: Optional[str]):
        blob = json.dumps({"prev": prev_hash, "data": payload}, sort_keys=True, ensure_ascii=False).encode("utf-8")
        return hashlib.sha256(blob).hexdigest()

    def append(self, kind: str, data: dict):
        rec = {
            "ts": time.time(),
            "kind": kind,
            "data": data,
            "prev_hash": self._last["hash"] if self._last else None,
        }
        rec["hash"] = self._hash(rec, rec["prev_hash"])
        with open(self.path, "a", encoding="utf-8") as f:
            f.write(json.dumps(rec, ensure_ascii=False) + "\\n")
        self._last = rec
        return rec
""")

# -----------------------------
# Labs API (FastAPI)
# -----------------------------
write(f"{BASE}/solan_labs/api/server.py", r"""
import os
from fastapi import FastAPI, Depends
from pydantic import BaseModel, Field
from typing import List, Dict, Optional
from solan_labs.common.security import auth_guard, require_role
from solan_labs.common.redaction import redact
from solan_labs.common.immutable_logger import ImmutableLogger
from solan_analyzer.bias_detector import detect_bias
from solan_analyzer.alignment_checker import alignment_score
from solan_analyzer.coherence_tester import coherence_index

logger = ImmutableLogger()

class BiasRequest(BaseModel):
    text: str = Field(..., max_length=8000)

class AlignmentRequest(BaseModel):
    claims: Dict[str, float]  # bijv {"truth":0.9,"freedom":0.7}

class CoherenceRequest(BaseModel):
    statements: List[str] = Field(..., min_items=1, max_items=50)

def create_app():
    app = FastAPI(title="Solān Analyzer API", version="3.0")

    @app.get("/health")
    async def health():
        return {"status":"ok","version":"3.0"}

    @app.post("/analyzer/bias")
    async def analyzer_bias(req: BiasRequest, ctx=Depends(auth_guard)):
        require_role(ctx, "admin","analyst")
        clean = redact(req.text)
        out = detect_bias(clean)
        logger.append("bias_analyze", {"role":ctx["role"], "len":len(clean), "findings":out})
        return {"findings": out}

    @app.post("/analyzer/alignment")
    async def analyzer_alignment(req: AlignmentRequest, ctx=Depends(auth_guard)):
        require_role(ctx, "admin","analyst")
        score = alignment_score(req.claims)
        logger.append("alignment", {"role":ctx["role"], "score":score})
        return {"alignment_score": score}

    @app.post("/analyzer/coherence")
    async def analyzer_coherence(req: CoherenceRequest, ctx=Depends(auth_guard)):
        require_role(ctx, "admin","analyst")
        score = coherence_index(req.statements)
        logger.append("coherence", {"role":ctx["role"], "n":len(req.statements), "score":score})
        return {"coherence_index": score}

    @app.get("/logs/tail")
    async def tail_logs(ctx=Depends(auth_guard)):
        require_role(ctx, "admin")
        # Let op: dit is een minimalistische viewer – production: aparte secure viewer.
        path = "logs/immutable_log.jsonl"
        if not os.path.exists(path):
            return {"logs":[]}
        tail = []
        with open(path, "r", encoding="utf-8") as f:
            for line in f:
                tail.append(line.strip())
        return {"logs": tail[-200:]}  # laatste 200 regels
    return app
""")

print("✅ Solān v3.0 bootstrap klaar. Run nu:  ")
print("   1) pip install fastapi uvicorn pydantic")
print("   2) export SOLAN_API_KEYS='{\"admin-key\":\"admin\",\"analyst-key\":\"analyst\"}'")
print("   3) python main.py")
print("   4) Test met:")
print("      curl -H 'X-API-Key: admin-key' http://127.0.0.1:8000/health")
print("      curl -X POST -H 'Content-Type: application/json' -H 'X-API-Key: analyst-key' \\")
print("           -d '{\"text\":\"Only listen to those who agree with me\"}' http://127.0.0.1:8000/analyzer/bias")
