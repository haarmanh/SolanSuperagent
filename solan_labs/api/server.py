import os
from fastapi import FastAPI, Depends, Request
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

    @app.post("/v1/echo")
    async def echo(req: Request):
        """Simple echo endpoint for testing"""
        try:
            data = await req.json()
        except Exception:
            data = {"_raw": (await req.body()).decode('utf-8', errors='ignore')}
        return {"ok": True, "echo": data}

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
