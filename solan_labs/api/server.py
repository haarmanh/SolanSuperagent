import os
import json
import pathlib
from datetime import datetime
from fastapi import FastAPI, Depends, Request
from pydantic import BaseModel, Field, EmailStr
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

class Invite(BaseModel):
    name: str = Field(..., min_length=1, max_length=100)
    email: EmailStr
    org: Optional[str] = Field(None, max_length=100)
    role: Optional[str] = Field(None, max_length=100)
    reason: str = Field(..., min_length=10, max_length=1000)

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

    @app.get("/v1/info")
    async def info():
        """API information endpoint"""
        return {
            "service": "Solān AI Analysis API",
            "version": "3.0",
            "status": "operational",
            "features": {
                "bias_detection": True,
                "ethical_alignment": True,
                "coherence_analysis": True,
                "audit_trail": True
            },
            "endpoints": {
                "health": "/health",
                "echo": "/v1/echo",
                "info": "/v1/info",
                "invite": "/v1/invite",
                "bias": "/analyzer/bias",
                "alignment": "/analyzer/alignment",
                "coherence": "/analyzer/coherence"
            }
        }

    @app.post("/v1/invite")
    async def invite(body: Invite):
        """Accept invite requests and store them"""
        # Create data directory if it doesn't exist
        data_dir = pathlib.Path("/data")
        data_dir.mkdir(parents=True, exist_ok=True)

        # Prepare invite record
        invite_record = {
            "name": body.name,
            "email": body.email,
            "org": body.org,
            "role": body.role,
            "reason": body.reason,
            "timestamp": datetime.utcnow().isoformat() + "Z",
            "ip": "unknown",  # Could be enhanced with request.client.host
            "status": "pending"
        }

        # Append to JSONL file
        invites_file = data_dir / "invites.jsonl"
        try:
            with invites_file.open("a", encoding="utf-8") as f:
                f.write(json.dumps(invite_record) + "\n")

            # Log the invite
            logger.append("invite_request", {
                "email": body.email,
                "org": body.org or "none",
                "timestamp": invite_record["timestamp"]
            })

            return {
                "ok": True,
                "message": "Invite request received successfully",
                "timestamp": invite_record["timestamp"]
            }

        except Exception as e:
            logger.append("invite_error", {"error": str(e)})
            return {
                "ok": False,
                "message": "Failed to process invite request",
                "error": "internal_error"
            }

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
