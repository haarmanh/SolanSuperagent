#!/usr/bin/env python3
"""
Solān Observatorium Proxy Server
Secure server-side proxy that handles API keys and forwards requests to Solān v3.0 API
Never exposes API keys to client-side code
"""

import os
import json
import asyncio
from fastapi import FastAPI, Request, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
import httpx
from pydantic import BaseModel
from typing import Dict, List, Optional

# Configuration
ANALYZER_BASE = os.getenv("ANALYZER_BASE", "http://127.0.0.1:8000")
SOLAN_ADMIN_KEY = os.getenv("SOLAN_ADMIN_KEY", "admin-key")
SOLAN_ANALYST_KEY = os.getenv("SOLAN_ANALYST_KEY", "analyst-key")

app = FastAPI(title="Solān Observatorium Proxy", version="1.0")

# CORS for local development
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production: specify exact origins
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Request models
class BiasRequest(BaseModel):
    text: str

class AlignmentRequest(BaseModel):
    claims: Dict[str, float]

class CoherenceRequest(BaseModel):
    statements: List[str]

# Serve the Observatorium interface
@app.get("/")
async def serve_observatorium():
    """Serve the main Observatorium interface"""
    return FileResponse("solan_observatorium_v3.html")

# Health endpoint proxy
@app.get("/api/health")
async def proxy_health():
    """Proxy health check to Solān API"""
    try:
        async with httpx.AsyncClient() as client:
            response = await client.get(
                f"{ANALYZER_BASE}/health",
                headers={"X-API-Key": SOLAN_ADMIN_KEY}
            )
            return response.json()
    except Exception as e:
        raise HTTPException(status_code=503, detail=f"Analyzer API unavailable: {str(e)}")

# Bias detection proxy
@app.post("/api/analyzer/bias")
async def proxy_bias_detection(request: BiasRequest):
    """Proxy bias detection to Solān API with server-side key"""
    try:
        # Sanitize and limit input
        text = str(request.text or "").strip()[:8000]
        
        async with httpx.AsyncClient() as client:
            response = await client.post(
                f"{ANALYZER_BASE}/analyzer/bias",
                headers={
                    "Content-Type": "application/json",
                    "X-API-Key": SOLAN_ANALYST_KEY
                },
                json={"text": text}
            )
            
            if response.status_code == 200:
                return response.json()
            else:
                raise HTTPException(
                    status_code=response.status_code,
                    detail=f"Analyzer API error: {response.text}"
                )
                
    except httpx.RequestError as e:
        raise HTTPException(status_code=503, detail=f"Connection error: {str(e)}")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Internal error: {str(e)}")

# Alignment checker proxy
@app.post("/api/analyzer/alignment")
async def proxy_alignment_check(request: AlignmentRequest):
    """Proxy alignment check to Solān API with server-side key"""
    try:
        async with httpx.AsyncClient() as client:
            response = await client.post(
                f"{ANALYZER_BASE}/analyzer/alignment",
                headers={
                    "Content-Type": "application/json",
                    "X-API-Key": SOLAN_ANALYST_KEY
                },
                json={"claims": request.claims}
            )
            
            if response.status_code == 200:
                return response.json()
            else:
                raise HTTPException(
                    status_code=response.status_code,
                    detail=f"Analyzer API error: {response.text}"
                )
                
    except httpx.RequestError as e:
        raise HTTPException(status_code=503, detail=f"Connection error: {str(e)}")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Internal error: {str(e)}")

# Coherence analysis proxy
@app.post("/api/analyzer/coherence")
async def proxy_coherence_analysis(request: CoherenceRequest):
    """Proxy coherence analysis to Solān API with server-side key"""
    try:
        # Sanitize and limit statements
        statements = [str(s).strip() for s in request.statements if str(s).strip()][:50]
        
        if not statements:
            raise HTTPException(status_code=400, detail="No valid statements provided")
        
        async with httpx.AsyncClient() as client:
            response = await client.post(
                f"{ANALYZER_BASE}/analyzer/coherence",
                headers={
                    "Content-Type": "application/json",
                    "X-API-Key": SOLAN_ANALYST_KEY
                },
                json={"statements": statements}
            )
            
            if response.status_code == 200:
                return response.json()
            else:
                raise HTTPException(
                    status_code=response.status_code,
                    detail=f"Analyzer API error: {response.text}"
                )
                
    except httpx.RequestError as e:
        raise HTTPException(status_code=503, detail=f"Connection error: {str(e)}")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Internal error: {str(e)}")

# Logs endpoint proxy (admin only)
@app.get("/api/logs/tail")
async def proxy_logs_tail():
    """Proxy logs access to Solān API with admin key"""
    try:
        async with httpx.AsyncClient() as client:
            response = await client.get(
                f"{ANALYZER_BASE}/logs/tail",
                headers={"X-API-Key": SOLAN_ADMIN_KEY}
            )
            
            if response.status_code == 200:
                return response.json()
            else:
                raise HTTPException(
                    status_code=response.status_code,
                    detail=f"Analyzer API error: {response.text}"
                )
                
    except httpx.RequestError as e:
        raise HTTPException(status_code=503, detail=f"Connection error: {str(e)}")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Internal error: {str(e)}")

# Status endpoint for proxy health
@app.get("/api/proxy/status")
async def proxy_status():
    """Check proxy server status"""
    try:
        # Test connection to analyzer
        async with httpx.AsyncClient() as client:
            response = await client.get(
                f"{ANALYZER_BASE}/health",
                headers={"X-API-Key": SOLAN_ADMIN_KEY},
                timeout=5.0
            )
            analyzer_status = "online" if response.status_code == 200 else "error"
    except:
        analyzer_status = "offline"
    
    return {
        "proxy_status": "online",
        "analyzer_status": analyzer_status,
        "analyzer_base": ANALYZER_BASE,
        "version": "1.0"
    }

if __name__ == "__main__":
    import uvicorn
    
    print("🔒 Starting Solān Observatorium Proxy Server...")
    print(f"📡 Analyzer API: {ANALYZER_BASE}")
    print(f"🌐 Proxy Server: http://localhost:8080")
    print(f"🎯 Observatorium: http://localhost:8080/")
    print("🔑 API keys are handled server-side (secure)")
    
    uvicorn.run(
        app, 
        host="0.0.0.0", 
        port=8080,
        log_level="info"
    )
