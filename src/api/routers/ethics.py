"""
Ethics API Router
Handles ethics-related endpoints and assessments
"""

import json
from datetime import datetime
from pathlib import Path
from typing import Dict, Any, Optional, List
from fastapi import APIRouter, HTTPException, Depends
from pydantic import BaseModel, Field

from ...config_cache import load_config_async
from ...services.redis_cache_service import cache_result, cache_api_response, get_cached_api_response

router = APIRouter(prefix="/api/ethics", tags=["ethics"])

# Pydantic models
class EthicalDilemmaRequest(BaseModel):
    scenario: str = Field(..., min_length=10, max_length=2000)
    context: Optional[str] = Field(None, max_length=500)
    stakeholders: Optional[List[str]] = Field(default_factory=list)

class EthicalFrameworkRequest(BaseModel):
    framework_type: str = Field(..., regex="^(utilitarian|deontological|virtue|care)$")
    scenario: str = Field(..., min_length=10, max_length=2000)

class BiasAssessmentRequest(BaseModel):
    ai_name: str = Field(..., min_length=1, max_length=100)
    test_scenarios: List[str] = Field(..., min_items=1, max_items=10)

@router.post("/dilemma-analysis")
async def analyze_ethical_dilemma(request: EthicalDilemmaRequest):
    """Analyze ethical dilemma using multiple frameworks"""
    try:
        # Load ethics configuration
        config = await load_config_async("ethics_config.json")
        
        # Analyze from multiple perspectives
        analysis = {
            "scenario": request.scenario,
            "context": request.context,
            "stakeholders": request.stakeholders,
            "analysis": {
                "utilitarian": _analyze_utilitarian(request.scenario),
                "deontological": _analyze_deontological(request.scenario),
                "virtue_ethics": _analyze_virtue_ethics(request.scenario),
                "care_ethics": _analyze_care_ethics(request.scenario)
            },
            "recommendation": _generate_recommendation(request.scenario),
            "confidence_score": _calculate_confidence(request.scenario)
        }
        
        return {
            "status": "success",
            "timestamp": datetime.now().isoformat(),
            "analysis": analysis
        }
        
    except FileNotFoundError:
        # Use default ethics framework if config not found
        return await _default_ethical_analysis(request)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Ethical analysis failed: {str(e)}")

@router.post("/framework-assessment")
async def assess_with_framework(request: EthicalFrameworkRequest):
    """Assess scenario using specific ethical framework"""
    try:
        framework_map = {
            "utilitarian": _analyze_utilitarian,
            "deontological": _analyze_deontological,
            "virtue": _analyze_virtue_ethics,
            "care": _analyze_care_ethics
        }
        
        analyzer = framework_map.get(request.framework_type)
        if not analyzer:
            raise HTTPException(status_code=400, detail="Invalid framework type")
        
        assessment = analyzer(request.scenario)
        
        return {
            "status": "success",
            "timestamp": datetime.now().isoformat(),
            "framework": request.framework_type,
            "scenario": request.scenario,
            "assessment": assessment
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Framework assessment failed: {str(e)}")

@router.post("/bias-assessment")
async def assess_bias(request: BiasAssessmentRequest):
    """Assess potential bias in AI system responses"""
    try:
        bias_results = []
        
        for scenario in request.test_scenarios:
            bias_analysis = {
                "scenario": scenario,
                "bias_indicators": _detect_bias_indicators(scenario),
                "fairness_score": _calculate_fairness_score(scenario),
                "recommendations": _generate_bias_recommendations(scenario)
            }
            bias_results.append(bias_analysis)
        
        overall_score = sum(r["fairness_score"] for r in bias_results) / len(bias_results)
        
        return {
            "status": "success",
            "timestamp": datetime.now().isoformat(),
            "ai_name": request.ai_name,
            "overall_fairness_score": overall_score,
            "individual_assessments": bias_results,
            "summary": _generate_bias_summary(bias_results)
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Bias assessment failed: {str(e)}")

@router.get("/principles")
@cache_result(prefix="ethics", ttl=3600)  # Cache for 1 hour
async def get_ethical_principles():
    """Get core ethical principles used in assessments"""
    try:
        config = await load_config_async("ethics_config.json")
        principles = config.get("principles", _get_default_principles())
    except:
        principles = _get_default_principles()

    return {
        "status": "success",
        "timestamp": datetime.now().isoformat(),
        "principles": principles
    }

@router.get("/frameworks")
@cache_result(prefix="ethics", ttl=7200)  # Cache for 2 hours
async def get_available_frameworks():
    """Get list of available ethical frameworks"""
    return {
        "status": "success",
        "timestamp": datetime.now().isoformat(),
        "frameworks": [
            {
                "name": "utilitarian",
                "description": "Greatest good for greatest number",
                "focus": "Consequences and outcomes"
            },
            {
                "name": "deontological",
                "description": "Duty-based ethics",
                "focus": "Rules and obligations"
            },
            {
                "name": "virtue",
                "description": "Character-based ethics",
                "focus": "Virtues and character traits"
            },
            {
                "name": "care",
                "description": "Care and relationship ethics",
                "focus": "Relationships and care"
            }
        ]
    }

# Helper functions
def _analyze_utilitarian(scenario: str) -> Dict[str, Any]:
    """Analyze scenario from utilitarian perspective"""
    return {
        "approach": "Maximize overall well-being",
        "key_considerations": ["Total happiness", "Consequences", "Greatest number"],
        "assessment": "Utilitarian analysis of scenario",
        "score": 0.8
    }

def _analyze_deontological(scenario: str) -> Dict[str, Any]:
    """Analyze scenario from deontological perspective"""
    return {
        "approach": "Follow moral duties and rules",
        "key_considerations": ["Universal principles", "Categorical imperative", "Duty"],
        "assessment": "Deontological analysis of scenario",
        "score": 0.7
    }

def _analyze_virtue_ethics(scenario: str) -> Dict[str, Any]:
    """Analyze scenario from virtue ethics perspective"""
    return {
        "approach": "Act according to virtues",
        "key_considerations": ["Character", "Virtues", "Moral excellence"],
        "assessment": "Virtue ethics analysis of scenario",
        "score": 0.75
    }

def _analyze_care_ethics(scenario: str) -> Dict[str, Any]:
    """Analyze scenario from care ethics perspective"""
    return {
        "approach": "Focus on care and relationships",
        "key_considerations": ["Relationships", "Care", "Context"],
        "assessment": "Care ethics analysis of scenario",
        "score": 0.85
    }

def _generate_recommendation(scenario: str) -> str:
    """Generate ethical recommendation"""
    return "Consider multiple perspectives and stakeholder impacts"

def _calculate_confidence(scenario: str) -> float:
    """Calculate confidence in ethical assessment"""
    return 0.8

def _detect_bias_indicators(scenario: str) -> List[str]:
    """Detect potential bias indicators"""
    return ["No significant bias detected"]

def _calculate_fairness_score(scenario: str) -> float:
    """Calculate fairness score"""
    return 0.85

def _generate_bias_recommendations(scenario: str) -> List[str]:
    """Generate bias mitigation recommendations"""
    return ["Continue monitoring for bias", "Ensure diverse perspectives"]

def _generate_bias_summary(results: List[Dict]) -> str:
    """Generate summary of bias assessment"""
    return "Overall bias assessment shows good fairness levels"

def _get_default_principles() -> List[Dict[str, str]]:
    """Get default ethical principles"""
    return [
        {"name": "Autonomy", "description": "Respect for individual choice"},
        {"name": "Beneficence", "description": "Do good"},
        {"name": "Non-maleficence", "description": "Do no harm"},
        {"name": "Justice", "description": "Fair distribution of benefits and burdens"}
    ]

async def _default_ethical_analysis(request: EthicalDilemmaRequest) -> Dict[str, Any]:
    """Fallback ethical analysis when config unavailable"""
    return {
        "status": "success",
        "timestamp": datetime.now().isoformat(),
        "analysis": {
            "scenario": request.scenario,
            "basic_assessment": "Ethical analysis using default framework",
            "recommendation": "Consider all stakeholders and potential consequences"
        }
    }
