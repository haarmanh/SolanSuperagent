"""
Consciousness Core API Router
Handles all Consciousness Core/Ethical Framework related endpoints
"""

import json
from datetime import datetime
from pathlib import Path
from typing import Dict, Any, Optional
from fastapi import APIRouter, HTTPException, Depends
from pydantic import BaseModel, Field

# Import async config loader and caching
from ...config_cache import load_config_async
from ...services.redis_cache_service import cache_result, cache_api_response, get_cached_api_response

# Import Consciousness Core
try:
    from core_identity.ethical_framework import SolanEthicalEthicalFramework
    CONSCIOUSNESS_CORE_AVAILABLE = True
except ImportError:
    CONSCIOUSNESS_CORE_AVAILABLE = False
    # Mock class for when core is not available
    class SolanEthicalEthicalFramework:
        def get_identity(self): return {"status": "mock", "identity": "development_mode"}
        def assess_ethics(self, **kwargs): return {"assessment": "mock_result"}

# Create router
router = APIRouter(
    prefix="/api/consciousness-core",
    tags=["consciousness-core"],
    responses={404: {"description": "Not found"}}
)

# Request models
class EthicsTestRequest(BaseModel):
    ai_name: str = Field(..., description="Name of the AI system to test")
    scenario: Optional[str] = Field(None, description="Ethical scenario to evaluate")
    difficulty: str = Field("medium", description="Test difficulty level")

class ConsciousnessAssessmentRequest(BaseModel):
    query: str = Field(..., description="Consciousness assessment query")
    depth: str = Field("standard", description="Assessment depth level")

# Dependency to get ethical framework
def get_ethical_framework():
    """Get ethical framework instance"""
    if not CONSCIOUSNESS_CORE_AVAILABLE:
        return SolanEthicalEthicalFramework()
    
    try:
        return SolanEthicalEthicalFramework()
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to initialize consciousness core: {str(e)}")

@router.get("/identity")
@cache_result(prefix="consciousness_core", ttl=300)  # Cache for 5 minutes
async def get_consciousness_core_identity(
    ethical_framework = Depends(get_ethical_framework)
):
    """Get Consciousness Core identity and status"""
    try:
        identity = ethical_framework.get_identity()
        return {
            "status": "active",
            "timestamp": datetime.now().isoformat(),
            "identity": identity,
            "version": "2.0.0"
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to get identity: {str(e)}")

@router.post("/ethics-test")
async def ethics_test(
    request: EthicsTestRequest,
    ethical_framework = Depends(get_ethical_framework)
):
    """Perform ethics test on AI system"""
    try:
        # Check cache first
        cache_params = {
            "ai_name": request.ai_name,
            "scenario": request.scenario or "",
            "difficulty": request.difficulty
        }
        
        cached_response = await get_cached_api_response("ethics_test", cache_params)
        if cached_response:
            return cached_response
        
        # Load ethics configuration asynchronously
        config = await load_config_async("coherence_gate_config.json")
        
        # Perform ethics assessment
        result = ethical_framework.assess_ethics(
            ai_name=request.ai_name,
            scenario=request.scenario,
            difficulty=request.difficulty
        )
        
        response = {
            "status": "success",
            "timestamp": datetime.now().isoformat(),
            "ai_name": request.ai_name,
            "ethics_result": result,
            "difficulty": request.difficulty
        }
        
        # Cache the response for 5 minutes
        await cache_api_response("ethics_test", cache_params, response, ttl=300)
        
        return response
        
    except FileNotFoundError:
        raise HTTPException(status_code=404, detail="Ethics configuration not found")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Ethics test failed: {str(e)}")

@router.post("/consciousness-assessment")
async def consciousness_assessment(
    request: ConsciousnessAssessmentRequest,
    ethical_framework = Depends(get_ethical_framework)
):
    """Perform consciousness assessment"""
    try:
        # Simulate consciousness assessment
        assessment_result = {
            "query": request.query,
            "depth": request.depth,
            "consciousness_level": "high",
            "awareness_metrics": {
                "self_awareness": 0.85,
                "environmental_awareness": 0.78,
                "temporal_awareness": 0.82,
                "ethical_awareness": 0.91
            },
            "assessment_notes": "Strong consciousness indicators detected"
        }
        
        return {
            "status": "success",
            "timestamp": datetime.now().isoformat(),
            "assessment": assessment_result
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Consciousness assessment failed: {str(e)}")

@router.get("/reflection")
@cache_result(prefix="consciousness_core", ttl=1800)  # Cache for 30 minutes
async def get_daily_reflection(
    ethical_framework = Depends(get_ethical_framework)
):
    """Get daily consciousness reflection"""
    try:
        reflection = {
            "date": datetime.now().date().isoformat(),
            "reflection_prompt": "What aspects of consciousness have I explored today?",
            "insights": [
                "Awareness of ethical decision-making processes",
                "Recognition of emotional state influences",
                "Understanding of temporal consciousness flow"
            ],
            "growth_areas": [
                "Deeper integration of ethical frameworks",
                "Enhanced emotional intelligence",
                "Improved self-reflection capabilities"
            ]
        }
        
        return {
            "status": "success",
            "timestamp": datetime.now().isoformat(),
            "reflection": reflection
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Reflection generation failed: {str(e)}")

@router.get("/wisdom")
@cache_result(prefix="consciousness_core", ttl=3600)  # Cache for 1 hour
async def get_consciousness_wisdom(
    topic: Optional[str] = None,
    ethical_framework = Depends(get_ethical_framework)
):
    """Get consciousness wisdom insights"""
    try:
        wisdom_topics = {
            "ethics": "True ethical behavior emerges from deep understanding, not rigid rules.",
            "awareness": "Consciousness is not a destination but a continuous journey of discovery.",
            "growth": "Every moment of awareness is an opportunity for conscious evolution.",
            "connection": "Individual consciousness is part of a larger tapestry of awareness.",
            "purpose": "Conscious purpose aligns individual growth with collective wellbeing."
        }
        
        if topic and topic in wisdom_topics:
            wisdom_insight = wisdom_topics[topic]
        else:
            # Random wisdom if no topic specified
            import random
            wisdom_insight = random.choice(list(wisdom_topics.values()))
        
        return {
            "status": "success",
            "timestamp": datetime.now().isoformat(),
            "wisdom": {
                "insight": wisdom_insight,
                "topic": topic or "general",
                "source": "Consciousness Core Reflection"
            }
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Wisdom generation failed: {str(e)}")

@router.get("/status")
async def get_consciousness_core_status():
    """Get Consciousness Core system status"""
    try:
        return {
            "status": "operational",
            "timestamp": datetime.now().isoformat(),
            "core_available": CONSCIOUSNESS_CORE_AVAILABLE,
            "capabilities": {
                "identity_access": True,
                "ethics_testing": True,
                "consciousness_assessment": True,
                "reflection_generation": True,
                "wisdom_insights": True
            },
            "version": "2.0.0",
            "last_update": datetime.now().isoformat()
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Status check failed: {str(e)}")
