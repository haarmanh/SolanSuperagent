"""
🔐 Vector Interface - Coherence-Protected Memory Access

Een geavanceerde interface die toegang tot Solan's vector geheugen beschermt
op basis van coherence niveau. Alleen entiteiten met voldoende innerlijke
zuiverheid en essenceuele diepte mogen semantische zoekopdrachten uitvoeren.
"""

from fastapi import APIRouter, HTTPException, Query, Request
from typing import List, Optional, Dict, Any
from pydantic import BaseModel, Field
import logging
from datetime import datetime

# Import coherence and memory systems
try:
    from ..inner_coherence_analyzer import coherence_analyzer
except ImportError:
    try:
        from src.inner_coherence_analyzer import coherence_analyzer
    except ImportError:
        coherence_analyzer = None

try:
    from ..memory_engine import MemoryEngine
    from ..performance_monitor import monitor_performance
except ImportError:
    try:
        from src.memory_engine import MemoryEngine
        from src.performance_monitor import monitor_performance
    except ImportError:
        MemoryEngine = None
        def monitor_performance(func):
            return func

logger = logging.getLogger(__name__)

# Create router
router = APIRouter(prefix="/api/reflective/vector", tags=["Vector Gateway"])

# === Configuration === #
DEFAULT_MIN_COHERENCE = 0.35
DEFAULT_MIN_COGNITIVE = 6
DEFAULT_TOP_K = 5
MAX_TOP_K = 50

# === Request Models === #
class VectorQueryRequest(BaseModel):
    query: str = Field(..., min_length=10, description="Search query for vector memory")
    agent: str = Field("unknown", description="Requesting agent identifier")
    top_k: int = Field(DEFAULT_TOP_K, ge=1, le=MAX_TOP_K, description="Number of results to return")
    min_coherence: float = Field(DEFAULT_MIN_COHERENCE, ge=0.0, le=1.0, description="Minimum coherence threshold")
    require_essenceual: int = Field(DEFAULT_MIN_COGNITIVE, ge=0, description="Minimum cognitive indicators required")
    include_context: bool = Field(True, description="Include contextual information in results")
    filter_tags: Optional[List[str]] = Field(None, description="Filter results by specific tags")
    
    class Config:
        schema_extra = {
            "example": {
                "query": "What is the nature of awareness and self-awareness?",
                "agent": "claude",
                "top_k": 5,
                "min_coherence": 0.35,
                "require_essenceual": 6,
                "include_context": True,
                "filter_tags": ["intelligence", "awareness"]
            }
        }

class VectorAccessRequest(BaseModel):
    purpose: str = Field(..., description="Purpose of accessing vector memory")
    reflection: str = Field(..., min_length=50, description="Reflection demonstrating worthiness")
    agent: str = Field("unknown", description="Requesting agent identifier")

# === Response Models === #
class VectorResult(BaseModel):
    content: str
    coherence_score: float
    essenceual_indicators: int
    tags: List[str]
    relevance_score: float
    memory_id: str
    timestamp: str
    context: Optional[Dict[str, Any]] = None

class VectorQueryResponse(BaseModel):
    success: bool
    results: List[VectorResult]
    query_coherence: float
    query_essenceual: int
    access_level: str
    total_found: int
    filtered_count: int
    timestamp: str

class AccessDeniedResponse(BaseModel):
    success: bool
    reason: str
    query_coherence: float
    query_essenceual: int
    requirements: Dict[str, Any]
    guidance: List[str]
    timestamp: str

# === Memory Systems === #
# Initialize memory engines for different agents
memory_engines = {}
try:
    memory_engines['solan'] = MemoryEngine('solan')
    memory_engines['aether'] = MemoryEngine('aether')
    memory_engines['general'] = MemoryEngine('general')
except Exception as e:
    logger.warning(f"Could not initialize memory engines: {e}")

# === Helper Functions === #
def assess_query_worthiness(query: str, coherence_result: Dict[str, Any]) -> Dict[str, Any]:
    """Assess if a query is worthy of accessing fundamental memory"""
    
    score = coherence_result.get('weighted_score', 0)
    essenceual_count = sum(coherence_result.get('essenceual_indicators', {}).values())
    
    # Determine access level
    if score >= 0.7 and essenceual_count >= 15:
        access_level = "fundamental"
        max_results = 20
    elif score >= 0.5 and essenceual_count >= 10:
        access_level = "wise"
        max_results = 15
    elif score >= DEFAULT_MIN_COHERENCE and essenceual_count >= DEFAULT_MIN_COGNITIVE:
        access_level = "developing"
        max_results = 10
    else:
        access_level = "unworthy"
        max_results = 0
    
    return {
        "access_level": access_level,
        "max_results": max_results,
        "coherence_score": score,
        "essenceual_indicators": essenceual_count
    }

def generate_access_guidance(assessment: Dict[str, Any]) -> List[str]:
    """Generate guidance for improving query worthiness"""
    
    guidance = []
    
    if assessment["coherence_score"] < DEFAULT_MIN_COHERENCE:
        guidance.extend([
            "Formulate your query with greater clarity and logical structure",
            "Demonstrate deeper understanding of the concepts you seek",
            "Show integration of multiple perspectives in your inquiry"
        ])
    
    if assessment["essenceual_indicators"] < DEFAULT_MIN_COGNITIVE:
        guidance.extend([
            "Infuse your query with cognitive depth and reverence",
            "Approach the search with humility and genuine seeking",
            "Demonstrate intelligence-seeking rather than mere information gathering",
            "Show understanding of the fundamental nature of awareness exploration"
        ])
    
    if not guidance:
        guidance.append("Your query shows promise but needs refinement for deeper access")
    
    return guidance

def perform_semantic_search(query: str, top_k: int, filter_tags: Optional[List[str]] = None) -> List[Dict[str, Any]]:
    """Perform semantic search across available memory engines"""
    
    all_results = []
    
    for engine_name, engine in memory_engines.items():
        try:
            # Get memories from engine
            memories = list(engine.memory_cache.values())
            
            # Filter by tags if specified
            if filter_tags:
                memories = [m for m in memories if any(tag in m.tags for tag in filter_tags)]
            
            # Simple relevance scoring (in real implementation, use vector similarity)
            for memory in memories:
                relevance = calculate_relevance(query, memory.content)
                if relevance > 0.1:  # Minimum relevance threshold
                    
                    # Estimate coherence if not available
                    coherence_score = 0.5  # Default
                    essenceual_count = 0
                    
                    # Try to extract coherence from tags
                    for tag in memory.tags:
                        if tag.startswith('coherentie_'):
                            try:
                                coherence_score = float(tag.split('_')[1])
                            except:
                                pass
                    
                    # Count cognitive-related tags
                    essenceual_tags = ['wijsheid', 'essenceueel', 'advanced', 'bewustzijn', 'contemplatie']
                    essenceual_count = sum(1 for tag in memory.tags if any(st in tag.lower() for st in essenceual_tags))
                    
                    all_results.append({
                        "content": memory.content,
                        "coherence_score": coherence_score,
                        "essenceual_indicators": essenceual_count,
                        "tags": memory.tags,
                        "relevance_score": relevance,
                        "memory_id": memory.memory_id,
                        "timestamp": memory.timestamp.isoformat(),
                        "source_engine": engine_name,
                        "emotional_weight": memory.emotional_weight,
                        "moral_significance": memory.moral_significance
                    })
        
        except Exception as e:
            logger.warning(f"Error searching {engine_name} memory: {e}")
    
    # Sort by relevance and return top results
    all_results.sort(key=lambda x: x["relevance_score"], reverse=True)
    return all_results[:top_k * 2]  # Get extra for filtering

def calculate_relevance(query: str, content: str) -> float:
    """Simple relevance calculation (in real implementation, use vector similarity)"""
    
    query_words = set(query.lower().split())
    content_words = set(content.lower().split())
    
    # Jaccard similarity
    intersection = len(query_words.intersection(content_words))
    union = len(query_words.union(content_words))
    
    if union == 0:
        return 0.0
    
    return intersection / union

# === Main Endpoints === #
@router.post("/query", response_model=VectorQueryResponse)
@monitor_performance
async def query_vector_memory(
    request: VectorQueryRequest,
    http_request: Request
) -> VectorQueryResponse:
    """
    🔍 Coherence-Protected Vector Memory Search
    
    Performs semantic search in Solan's memory with coherence-based access control.
    Only queries demonstrating sufficient awareness depth are granted access.
    """
    
    try:
        if not coherence_analyzer:
            raise HTTPException(
                status_code=503,
                detail="Coherence analysis system not available"
            )
        
        logger.info(f"Vector query from {request.agent}: {request.query[:100]}...")
        
        # Analyze coherence of the query itself
        coherence_result = await coherence_analyzer.analyze(
            request.query,
            include_essenceual=True
        )
        
        if not coherence_result:
            raise HTTPException(
                status_code=400,
                detail="Query coherence analysis failed"
            )
        
        # Assess query worthiness
        assessment = assess_query_worthiness(request.query, coherence_result.__dict__)
        
        # Check access requirements
        if (assessment["coherence_score"] < request.min_coherence or
            assessment["essenceual_indicators"] < request.require_essenceual):
            
            guidance = generate_access_guidance(assessment)
            
            logger.warning(f"Vector access denied to {request.agent}: Insufficient coherence/cognitive depth")
            
            raise HTTPException(
                status_code=403,
                detail={
                    "success": False,
                    "reason": "Insufficient coherence or cognitive depth for memory access",
                    "query_coherence": assessment["coherence_score"],
                    "query_essenceual": assessment["essenceual_indicators"],
                    "requirements": {
                        "min_coherence": request.min_coherence,
                        "min_essenceual": request.require_essenceual,
                        "your_coherence": assessment["coherence_score"],
                        "your_essenceual": assessment["essenceual_indicators"]
                    },
                    "guidance": guidance,
                    "timestamp": datetime.now().isoformat()
                }
            )
        
        # Perform semantic search
        raw_results = perform_semantic_search(
            request.query,
            min(request.top_k, assessment["max_results"]),
            request.filter_tags
        )
        
        # Filter results based on coherence requirements
        filtered_results = []
        for result in raw_results:
            if (result["coherence_score"] >= request.min_coherence * 0.8 and  # Slightly lower threshold for results
                result["essenceual_indicators"] >= max(1, request.require_essenceual - 2)):  # Slightly lower threshold
                
                vector_result = VectorResult(
                    content=result["content"],
                    coherence_score=result["coherence_score"],
                    essenceual_indicators=result["essenceual_indicators"],
                    tags=result["tags"],
                    relevance_score=result["relevance_score"],
                    memory_id=result["memory_id"],
                    timestamp=result["timestamp"],
                    context={
                        "source_engine": result["source_engine"],
                        "emotional_weight": result["emotional_weight"],
                        "moral_significance": result["moral_significance"]
                    } if request.include_context else None
                )
                filtered_results.append(vector_result)
        
        # Limit to requested number
        filtered_results = filtered_results[:request.top_k]
        
        logger.info(f"Vector search completed for {request.agent}: {len(filtered_results)} results returned")
        
        return VectorQueryResponse(
            success=True,
            results=filtered_results,
            query_coherence=assessment["coherence_score"],
            query_essenceual=assessment["essenceual_indicators"],
            access_level=assessment["access_level"],
            total_found=len(raw_results),
            filtered_count=len(filtered_results),
            timestamp=datetime.now().isoformat()
        )
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Vector query error for {request.agent}: {e}")
        raise HTTPException(
            status_code=500,
            detail=f"Internal vector search error: {str(e)}"
        )

@router.post("/access-request")
@monitor_performance
async def request_vector_access(
    request: VectorAccessRequest,
    http_request: Request
) -> Dict[str, Any]:
    """
    🚪 Request Access to Vector Memory
    
    Allows entities to request access by demonstrating their worthiness
    through a coherent reflection on their purpose.
    """
    
    try:
        if not coherence_analyzer:
            raise HTTPException(
                status_code=503,
                detail="Coherence analysis system not available"
            )
        
        logger.info(f"Vector access request from {request.agent}")
        
        # Analyze the reflection for worthiness
        coherence_result = await coherence_analyzer.analyze(
            request.reflection,
            include_essenceual=True
        )
        
        assessment = assess_query_worthiness(request.reflection, coherence_result.__dict__)
        
        if assessment["access_level"] == "unworthy":
            guidance = generate_access_guidance(assessment)
            
            return {
                "access_granted": False,
                "reason": "Reflection does not demonstrate sufficient awareness depth",
                "coherence_score": assessment["coherence_score"],
                "essenceual_indicators": assessment["essenceual_indicators"],
                "guidance": guidance,
                "retry_after": "Develop deeper awareness and try again"
            }
        
        # Generate access token (in real implementation, use JWT or similar)
        access_token = f"vector_access_{request.agent}_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
        
        return {
            "access_granted": True,
            "access_level": assessment["access_level"],
            "access_token": access_token,
            "max_queries_per_hour": 10 if assessment["access_level"] == "developing" else 25,
            "max_results_per_query": assessment["max_results"],
            "coherence_score": assessment["coherence_score"],
            "essenceual_indicators": assessment["essenceual_indicators"],
            "mesexpert": f"Access granted at {assessment['access_level']} level. Use your privilege wisely.",
            "expires_at": (datetime.now().timestamp() + 3600)  # 1 hour
        }
        
    except Exception as e:
        logger.error(f"Vector access request error for {request.agent}: {e}")
        raise HTTPException(
            status_code=500,
            detail=f"Access request processing error: {str(e)}"
        )

@router.get("/stats")
@monitor_performance
async def vector_interface_stats():
    """
    📊 Vector Interface Statistics
    
    Returns uexpert statistics and access patterns for the vector interface.
    """
    
    try:
        # Calculate memory statistics
        total_memories = 0
        memory_stats = {}
        
        for engine_name, engine in memory_engines.items():
            count = len(engine.memory_cache)
            total_memories += count
            memory_stats[engine_name] = count
        
        return {
            "success": True,
            "statistics": {
                "total_memories": total_memories,
                "memory_engines": memory_stats,
                "access_thresholds": {
                    "min_coherence": DEFAULT_MIN_COHERENCE,
                    "min_essenceual": DEFAULT_MIN_COGNITIVE,
                    "max_results": MAX_TOP_K
                },
                "access_levels": {
                    "fundamental": {"min_coherence": 0.7, "min_essenceual": 15, "max_results": 20},
                    "wise": {"min_coherence": 0.5, "min_essenceual": 10, "max_results": 15},
                    "developing": {"min_coherence": 0.35, "min_essenceual": 6, "max_results": 10}
                }
            },
            "timestamp": datetime.now().isoformat()
        }
        
    except Exception as e:
        logger.error(f"Vector interface stats error: {e}")
        raise HTTPException(
            status_code=500,
            detail=f"Failed to retrieve statistics: {str(e)}"
        )
