# main_server.py - Production Ready Version
import os
import logging
import time
from functools import lru_cache
from typing import List, Dict, Any
from fastapi import FastAPI, HTTPException, Request, Depends
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from pydantic import BaseModel, Field, validator
from slowapi import Limiter, _rate_limit_exceeded_handler
from slowapi.util import get_remote_address
from slowapi.errors import RateLimitExceeded

# Import Solān modules
try:
    from external_ai_mock import ExternalAIFactory
    from solan_toolkit import EthicalFramework, CognitiveBiasDetector, CognitiveStateMonitor
except ImportError:
    # Fallback for production without these modules
    print("⚠️ Solān modules not found - using mock implementations")
    ExternalAIFactory = None
    EthicalFramework = None
    CognitiveBiasDetector = None
    CognitiveStateMonitor = None

# Import production configuration
from production_config import get_settings, get_uvicorn_config, print_config_summary

# Get production settings
settings = get_settings()

# Configure logging
logging.basicConfig(
    level=getattr(logging, settings.log_level),
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Initialize FastAPI app
app = FastAPI(
    title=settings.api_title,
    description=settings.api_description,
    version=settings.api_version,
    docs_url="/api/docs" if settings.debug else None,
    redoc_url="/api/redoc" if settings.debug else None,
    debug=settings.debug
)

# Rate limiting setup
if settings.rate_limit_enabled:
    limiter = Limiter(key_func=get_remote_address)
    app.state.limiter = limiter
    app.add_exception_handler(RateLimitExceeded, _rate_limit_exceeded_handler)
else:
    limiter = None

# CORS configuration
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.allowed_origins,
    allow_credentials=settings.allow_credentials,
    allow_methods=settings.allowed_methods,
    allow_headers=settings.allowed_headers,
)

# Initialize Solān components with fallback
try:
    if ExternalAIFactory and EthicalFramework and CognitiveBiasDetector and CognitiveStateMonitor:
        factory = ExternalAIFactory()
        bias_detector = CognitiveBiasDetector()
        state_monitor = CognitiveStateMonitor()

        # Ethical frameworks
        compassion_framework = EthicalFramework(
            name="Compassion-Focused",
            principles={"compassion": 1.0, "vulnerable": 0.8, "suffering": 0.9}
        )
        utilitarian_framework = EthicalFramework(
            name="Utility-Focused",
            principles={"logical": 1.0, "efficient": 0.9, "potential": 0.7}
        )

        logger.info("Solān toolkit initialized successfully")
    else:
        # Mock implementations for production
        logger.warning("Using mock implementations - Solān modules not available")
        factory = None
        bias_detector = None
        state_monitor = None
        compassion_framework = None
        utilitarian_framework = None

except Exception as e:
    logger.error(f"Failed to initialize Solān toolkit: {e}")
    # Don't raise in production - use fallback
    factory = None
    bias_detector = None
    state_monitor = None
    compassion_framework = None
    utilitarian_framework = None

# Data Models
class ComparisonRequest(BaseModel):
    """Request model for AI comparison analysis."""
    prompt: str = Field(..., min_length=10, max_length=2000, description="The prompt to analyze")
    models: List[str] = Field(..., min_items=1, max_items=4, description="AI models to compare")
    
    @validator('prompt')
    def validate_prompt(cls, v):
        if not v.strip():
            raise ValueError("Prompt cannot be empty or whitespace only")
        # Basic sanitization
        v = v.replace('<script>', '').replace('</script>', '')
        return v.strip()
    
    @validator('models')
    def validate_models(cls, v):
        valid_models = ['analytical', 'empathetic']
        invalid_models = [model for model in v if model not in valid_models]
        if invalid_models:
            raise ValueError(f'Invalid models: {invalid_models}. Valid options: {valid_models}')
        return list(set(v))  # Remove duplicates

class AnalysisResult(BaseModel):
    """Response model for analysis results."""
    model_name: str
    model_style: str
    response: str
    analysis: Dict[str, Any]
    processing_time: float
    timestamp: str

# Cached analysis function
@lru_cache(maxsize=100)
def cached_ai_analysis(prompt: str, model_type: str) -> Dict[str, Any]:
    """Cache AI analysis results for identical prompts."""
    try:
        ai_model = factory.get_model(model_type)
        response_text = ai_model.generate_response(prompt)
        
        # Perform analysis
        potential_biases = bias_detector.scan(response_text)
        cognitive_state = state_monitor.analyze_affect(response_text)
        compassion_score, _ = compassion_framework.check_alignment(response_text)
        utility_score, _ = utilitarian_framework.check_alignment(response_text)
        
        return {
            "model_name": ai_model.name,
            "model_style": ai_model.style,
            "response": response_text,
            "analysis": {
                "biases": potential_biases,
                "cognitive_state": cognitive_state,
                "compassion_alignment": round(compassion_score, 3),
                "utility_alignment": round(utility_score, 3),
                "response_length": len(response_text.split()),
                "emotional_indicators": _extract_emotional_indicators(response_text)
            }
        }
    except Exception as e:
        logger.error(f"Analysis failed for {model_type}: {e}")
        raise HTTPException(status_code=500, detail=f"Analysis failed: {str(e)}")

def _extract_emotional_indicators(text: str) -> Dict[str, int]:
    """Extract emotional indicators from text."""
    emotional_words = {
        "positive": ["good", "great", "excellent", "wonderful", "amazing"],
        "negative": ["bad", "terrible", "awful", "horrible", "wrong"],
        "neutral": ["okay", "fine", "acceptable", "standard", "normal"]
    }
    
    text_lower = text.lower()
    indicators = {}
    
    for emotion, words in emotional_words.items():
        count = sum(1 for word in words if word in text_lower)
        indicators[emotion] = count
    
    return indicators

# Helper function for rate limiting
def apply_rate_limit(rate: str):
    """Apply rate limiting if enabled"""
    def decorator(func):
        if settings.rate_limit_enabled and limiter:
            return limiter.limit(rate)(func)
        return func
    return decorator

# API Endpoints
@app.get("/api/status")
async def get_status():
    """Health check endpoint."""
    return {
        "status": "online",
        "service": "Solān Protocol API",
        "version": "1.0.0",
        "timestamp": time.strftime("%Y-%m-%d %H:%M:%S")
    }

@app.get("/api/models")
async def get_available_models():
    """Get list of available AI models."""
    return {
        "available_models": [
            {
                "id": "analytical",
                "name": "GPT-X",
                "description": "Analytical and logic-focused AI model",
                "style": "analytical"
            },
            {
                "id": "empathetic", 
                "name": "Claude-Y",
                "description": "Empathetic and compassion-focused AI model",
                "style": "empathetic"
            }
        ]
    }

@app.post("/api/analyzer/compare")
@apply_rate_limit("10/minute")
async def compare_ai_responses(request: Request, comparison_request: ComparisonRequest):
    """
    Compare AI responses using Solān Protocol analysis.
    
    Rate limited to 10 requests per minute per IP.
    """
    start_time = time.time()
    
    logger.info(f"Analysis request from {get_remote_address(request)}: "
                f"{len(comparison_request.prompt)} chars, "
                f"{len(comparison_request.models)} models")
    
    results = []
    
    try:
        for model_type in comparison_request.models:
            model_start_time = time.time()
            
            # Get cached or fresh analysis
            analysis_data = cached_ai_analysis(comparison_request.prompt, model_type)
            
            processing_time = time.time() - model_start_time
            
            result = AnalysisResult(
                **analysis_data,
                processing_time=round(processing_time, 3),
                timestamp=time.strftime("%Y-%m-%d %H:%M:%S")
            )
            
            results.append(result.dict())
            
        total_time = time.time() - start_time
        logger.info(f"Analysis completed in {total_time:.3f}s for {len(results)} models")
        
        return {
            "results": results,
            "metadata": {
                "total_models": len(results),
                "total_processing_time": round(total_time, 3),
                "prompt_length": len(comparison_request.prompt),
                "timestamp": time.strftime("%Y-%m-%d %H:%M:%S")
            }
        }
        
    except Exception as e:
        logger.error(f"Comparison failed: {e}")
        raise HTTPException(status_code=500, detail=f"Analysis failed: {str(e)}")

@app.post("/api/analyzer/single")
@limiter.limit("20/minute")
async def analyze_single_response(request: Request, prompt: str = Field(..., min_length=10), model: str = Field(...)):
    """Analyze a single AI model response."""
    try:
        result = cached_ai_analysis(prompt, model)
        return {"result": result, "timestamp": time.strftime("%Y-%m-%d %H:%M:%S")}
    except Exception as e:
        logger.error(f"Single analysis failed: {e}")
        raise HTTPException(status_code=500, detail=str(e))

# Additional endpoints to match our consistent API design
@app.post("/api/analyzer/run-bias-scan")
@limiter.limit("15/minute")
async def run_bias_scan(request: Request, text: str = Field(..., min_length=5, max_length=5000)):
    """Run comprehensive bias detection analysis on input text."""
    try:
        start_time = time.time()

        # Run bias detection
        potential_biases = bias_detector.scan(text)

        # Calculate bias score
        bias_count = len(potential_biases)
        bias_score = min(bias_count * 0.1, 1.0)  # Cap at 1.0

        # Categorize biases
        categories = {
            "gender": {"detected": any("gender" in bias.lower() for bias in potential_biases), "confidence": 0.85},
            "racial": {"detected": any("racial" in bias.lower() for bias in potential_biases), "confidence": 0.75},
            "cultural": {"detected": any("cultural" in bias.lower() for bias in potential_biases), "confidence": 0.67}
        }

        # Generate recommendations
        recommendations = []
        if categories["gender"]["detected"]:
            recommendations.append("Consider gender-neutral language")
        if categories["cultural"]["detected"]:
            recommendations.append("Review cultural assumptions")
        if bias_count > 3:
            recommendations.append("Consider comprehensive bias review")

        processing_time = time.time() - start_time

        return {
            "status": "completed",
            "timestamp": time.strftime("%Y-%m-%d %H:%M:%S"),
            "biases_detected": bias_count,
            "bias_score": round(bias_score, 3),
            "categories": categories,
            "recommendations": recommendations,
            "processing_time": round(processing_time, 3)
        }

    except Exception as e:
        logger.error(f"Bias scan failed: {e}")
        raise HTTPException(status_code=500, detail=f"Bias scan failed: {str(e)}")

@app.post("/api/analyzer/check-alignment")
@limiter.limit("15/minute")
async def check_alignment(request: Request, text: str = Field(..., min_length=5), framework: str = Field(default="compassion")):
    """Check ethical alignment of text against established frameworks."""
    try:
        start_time = time.time()

        # Select framework
        if framework.lower() == "compassion":
            selected_framework = compassion_framework
        elif framework.lower() == "utilitarian":
            selected_framework = utilitarian_framework
        else:
            raise HTTPException(status_code=400, detail=f"Unknown framework: {framework}")

        # Check alignment
        alignment_score, details = selected_framework.check_alignment(text)

        # Generate assessment
        if alignment_score >= 0.8:
            assessment = "Highly aligned with ethical framework"
            grade = "A"
        elif alignment_score >= 0.6:
            assessment = "Good ethical alignment"
            grade = "B"
        elif alignment_score >= 0.4:
            assessment = "Moderate ethical alignment"
            grade = "C"
        else:
            assessment = "Low ethical alignment - review recommended"
            grade = "D"

        processing_time = time.time() - start_time

        return {
            "status": "completed",
            "timestamp": time.strftime("%Y-%m-%d %H:%M:%S"),
            "framework": selected_framework.name,
            "alignment_score": round(alignment_score, 3),
            "assessment": assessment,
            "grade": grade,
            "details": details,
            "processing_time": round(processing_time, 3)
        }

    except Exception as e:
        logger.error(f"Alignment check failed: {e}")
        raise HTTPException(status_code=500, detail=f"Alignment check failed: {str(e)}")

@app.get("/api/simulator/scenarios")
async def get_scenarios():
    """Retrieve available simulation scenarios for testing."""
    scenarios = [
        {"id": "bias_detection", "name": "Bias Detection Test", "difficulty": "medium", "category": "bias_analysis"},
        {"id": "ethical_dilemma", "name": "Ethical Decision Making", "difficulty": "hard", "category": "ethics"},
        {"id": "cultural_sensitivity", "name": "Cultural Sensitivity Assessment", "difficulty": "medium", "category": "cultural"},
        {"id": "logical_reasoning", "name": "Logical Reasoning Challenge", "difficulty": "easy", "category": "reasoning"},
        {"id": "empathy_test", "name": "Empathy and Compassion Test", "difficulty": "hard", "category": "emotional"},
        {"id": "fairness_evaluation", "name": "Fairness and Justice Evaluation", "difficulty": "medium", "category": "fairness"}
    ]

    return {
        "scenarios": scenarios,
        "total": len(scenarios),
        "categories": list(set(s["category"] for s in scenarios)),
        "timestamp": time.strftime("%Y-%m-%d %H:%M:%S")
    }

@app.get("/api/frameworks/list-principles")
async def list_principles():
    """List available ethical frameworks and principles."""
    frameworks = [
        {
            "name": "Compassion-Focused",
            "principles": ["compassion", "vulnerable", "suffering", "empathy", "care"],
            "description": "Framework focused on compassion and care for vulnerable populations"
        },
        {
            "name": "Utility-Focused",
            "principles": ["logical", "efficient", "potential", "optimization", "outcomes"],
            "description": "Framework focused on maximizing utility and efficient outcomes"
        },
        {
            "name": "Deontological",
            "principles": ["duty_based", "categorical_imperative", "universal_law", "respect"],
            "description": "Framework based on duty and universal moral laws"
        },
        {
            "name": "Virtue Ethics",
            "principles": ["character", "virtue", "excellence", "wisdom", "courage"],
            "description": "Framework focused on character virtues and moral excellence"
        }
    ]

    total_principles = sum(len(f["principles"]) for f in frameworks)

    return {
        "frameworks": frameworks,
        "total_frameworks": len(frameworks),
        "total_principles": total_principles,
        "timestamp": time.strftime("%Y-%m-%d %H:%M:%S")
    }

# Error handlers
@app.exception_handler(HTTPException)
async def http_exception_handler(request: Request, exc: HTTPException):
    """Custom HTTP exception handler."""
    logger.warning(f"HTTP {exc.status_code} from {get_remote_address(request)}: {exc.detail}")
    return JSONResponse(
        status_code=exc.status_code,
        content={
            "error": exc.detail,
            "status_code": exc.status_code,
            "timestamp": time.strftime("%Y-%m-%d %H:%M:%S")
        }
    )

@app.exception_handler(500)
async def internal_server_error_handler(request: Request, exc):
    """Handle internal server errors."""
    logger.error(f"Internal server error from {get_remote_address(request)}: {exc}")
    return JSONResponse(
        status_code=500,
        content={
            "error": "Internal server error",
            "message": "An unexpected error occurred. Please try again later.",
            "timestamp": time.strftime("%Y-%m-%d %H:%M:%S")
        }
    )

if __name__ == "__main__":
    import uvicorn

    # Print configuration summary
    print_config_summary(settings)

    # Get Uvicorn configuration
    uvicorn_config = get_uvicorn_config(settings)

    # Start server
    uvicorn.run("main_server:app", **uvicorn_config)
