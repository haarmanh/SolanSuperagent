import os, time, json
from fastapi import Header, HTTPException, status, Request
from typing import Optional, Dict
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

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
