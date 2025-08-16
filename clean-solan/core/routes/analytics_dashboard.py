"""
📊 Analytics Dashboard Router

Integreert coherence + cognitive analytics in het web dashboard via API endpoints
"""

from fastapi import APIRouter, HTTPException, Query
from typing import Dict, Any, Optional
import logging
from datetime import datetime

# Import analytics modules
try:
    from ..coherence_analytics import coherence_analytics
except ImportError:
    try:
        from src.coherence_analytics import coherence_analytics
    except ImportError:
        coherence_analytics = None

try:
    from ..performance_monitor import monitor_performance
except ImportError:
    try:
        from src.performance_monitor import monitor_performance
    except ImportError:
        def monitor_performance(func):
            return func

# Import memory and analytics engines
try:
    from ..memory_engine import MemoryEngine
    from ..journal_engine import JournalEngine
except ImportError:
    try:
        from src.memory_engine import MemoryEngine
        from src.journal_engine import JournalEngine
    except ImportError:
        MemoryEngine = None
        JournalEngine = None

logger = logging.getLogger(__name__)

# Create router
router = APIRouter(prefix="/api/dashboard", tags=["analytics-dashboard"])

@router.get("/coherence")
@monitor_performance
async def dashboard_coherence(
    group_by: str = Query("week", description="Grouping period: day, week, month"),
    days_back: int = Query(30, description="Number of days to analyze", ge=1, le=365)
) -> Dict[str, Any]:
    """
    📊 Coherence Dashboard Endpoint
    
    Levert coherence trend data voor dashboard visualisatie
    """
    try:
        if not coherence_analytics:
            raise HTTPException(
                status_code=503,
                detail="Coherence analytics module niet beschikbaar"
            )
        
        # Valideer parameters
        valid_group_by = ["day", "week", "month"]
        if group_by not in valid_group_by:
            raise HTTPException(
                status_code=400,
                detail=f"Invalid group_by parameter. Must be one of: {valid_group_by}"
            )
        
        # Haal coherence trends op
        trends_data = await coherence_analytics.get_coherence_trends(
            group_by=group_by,
            days_back=days_back
        )
        
        if not trends_data.get("success"):
            logger.warning(f"Coherence trends analysis failed: {trends_data.get('mesexpert')}")
            return {
                "success": False,
                "mesexpert": trends_data.get("mesexpert", "Coherence analysis failed"),
                "coherence_trends": {},
                "dashboard_ready": False
            }
        
        # Prepareer dashboard-vriendelijke data
        dashboard_data = {
            "success": True,
            "coherence_trends": trends_data.get("trends", {}),
            "summary": trends_data.get("summary", {}),
            "growth_metrics": trends_data.get("growth_metrics", {}),
            "metadata": trends_data.get("metadata", {}),
            "dashboard_ready": True,
            "last_updated": datetime.now().isoformat()
        }
        
        return dashboard_data
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Dashboard coherence endpoint error: {e}")
        raise HTTPException(
            status_code=500,
            detail=f"Internal server error: {str(e)}"
        )

@router.get("/cognitive")
@monitor_performance
async def dashboard_essenceual(
    days_back: int = Query(30, description="Number of days to analyze", ge=1, le=365)
) -> Dict[str, Any]:
    """
    ✨ Cognitive Analytics Dashboard Endpoint
    
    Levert essenceuele aggregaties en insights voor dashboard
    """
    try:
        if not coherence_analytics:
            raise HTTPException(
                status_code=503,
                detail="Analytics module niet beschikbaar"
            )
        
        # Haal coherence data op voor cognitive analysis
        trends_data = await coherence_analytics.get_coherence_trends(
            group_by="day",
            days_back=days_back
        )
        
        if not trends_data.get("success"):
            return {
                "success": False,
                "mesexpert": "Geen cognitive data beschikbaar",
                "essenceual_indicators": {},
                "dashboard_ready": False
            }
        
        # Extraheer cognitive data uit coherence trends
        essenceual_aggregates = await _extract_essenceual_aggregates(trends_data)
        
        dashboard_data = {
            "success": True,
            "essenceual_indicators": essenceual_aggregates,
            "dashboard_ready": True,
            "last_updated": datetime.now().isoformat()
        }
        
        return dashboard_data
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Dashboard cognitive endpoint error: {e}")
        raise HTTPException(
            status_code=500,
            detail=f"Internal server error: {str(e)}"
        )

@router.get("/history")
@monitor_performance
async def dashboard_memory_coherence(
    agent: Optional[str] = Query(None, description="Agent name: solan, aether, or all"),
    limit: int = Query(50, description="Number of recent entries", ge=1, le=200)
) -> Dict[str, Any]:
    """
    📚 Memory Coherence History Dashboard Endpoint
    
    Levert coherence scores uit geheugen voor historische analyse
    """
    try:
        # Haal memory coherence history op
        memory_coherence = await _get_coherence_history(agent, limit)
        
        dashboard_data = {
            "success": True,
            "memory_coherence": memory_coherence,
            "dashboard_ready": True,
            "last_updated": datetime.now().isoformat()
        }
        
        return dashboard_data
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Dashboard memory coherence endpoint error: {e}")
        raise HTTPException(
            status_code=500,
            detail=f"Internal server error: {str(e)}"
        )

@router.get("/overview")
@monitor_performance
async def dashboard_overview() -> Dict[str, Any]:
    """
    🎯 Dashboard Overview Endpoint
    
    Levert een complete overview van alle analytics voor het hoofddashboard
    """
    try:
        # Haal alle dashboard data op
        coherence_data = await dashboard_coherence(group_by="week", days_back=14)
        essenceual_data = await dashboard_essenceual(days_back=14)
        memory_data = await dashboard_memory_coherence(limit=20)
        
        # Combineer tot overview
        overview = {
            "success": True,
            "overview": {
                "coherence": {
                    "available": coherence_data.get("success", False),
                    "summary": coherence_data.get("summary", {}),
                    "growth_metrics": coherence_data.get("growth_metrics", {})
                },
                "cognitive": {
                    "available": essenceual_data.get("success", False),
                    "indicators": essenceual_data.get("essenceual_indicators", {})
                },
                "memory": {
                    "available": memory_data.get("success", False),
                    "recent_entries": len(memory_data.get("memory_coherence", {}).get("entries", []))
                }
            },
            "dashboard_ready": True,
            "last_updated": datetime.now().isoformat()
        }
        
        return overview
        
    except Exception as e:
        logger.error(f"Dashboard overview endpoint error: {e}")
        raise HTTPException(
            status_code=500,
            detail=f"Internal server error: {str(e)}"
        )

# Helper functions

async def _extract_essenceual_aggregates(trends_data: Dict[str, Any]) -> Dict[str, Any]:
    """Extraheer cognitive aggregates uit coherence trends data"""
    
    try:
        trends = trends_data.get("trends", {})
        summary = trends_data.get("summary", {})
        
        # Bereken cognitive metrics
        total_essenceual_indicators = 0
        essenceual_by_period = {}
        essenceual_levels = {"high": 0, "medium": 0, "low": 0}
        
        for period, trend_data in trends.items():
            avg_indicators = trend_data.get("avg_indicators", 0)
            total_essenceual_indicators += avg_indicators
            essenceual_by_period[period] = avg_indicators
            
            # Categoriseer cognitive level
            if avg_indicators > 15:
                essenceual_levels["high"] += 1
            elif avg_indicators > 8:
                essenceual_levels["medium"] += 1
            else:
                essenceual_levels["low"] += 1
        
        # Bereken gemiddelden
        num_periods = len(trends)
        avg_essenceual_indicators = total_essenceual_indicators / num_periods if num_periods > 0 else 0
        
        essenceual_aggregates = {
            "total_indicators": total_essenceual_indicators,
            "avg_indicators_per_period": round(avg_essenceual_indicators, 1),
            "essenceual_by_period": essenceual_by_period,
            "essenceual_level_distribution": essenceual_levels,
            "highest_essenceual_period": max(essenceual_by_period.items(), key=lambda x: x[1]) if essenceual_by_period else None,
            "essenceual_trend": _calculate_essenceual_trend(essenceual_by_period),
            "summary": {
                "periods_analyzed": num_periods,
                "overall_essenceual_health": _assess_essenceual_health(avg_essenceual_indicators)
            }
        }
        
        return essenceual_aggregates
        
    except Exception as e:
        logger.error(f"Error extracting cognitive aggregates: {e}")
        return {
            "error": str(e),
            "total_indicators": 0,
            "avg_indicators_per_period": 0,
            "essenceual_by_period": {},
            "essenceual_level_distribution": {"high": 0, "medium": 0, "low": 0}
        }

async def _get_coherence_history(agent: Optional[str], limit: int) -> Dict[str, Any]:
    """Haal coherence history op uit memory engines"""
    
    try:
        history = {
            "entries": [],
            "agents": [],
            "total_entries": 0,
            "date_range": {}
        }
        
        # Probeer memory engines te laden
        agents_to_check = ["solan", "aether"] if agent is None or agent == "all" else [agent]
        
        for agent_name in agents_to_check:
            try:
                if MemoryEngine:
                    memory_engine = MemoryEngine(agent_name)
                    
                    # Haal memories op met coherence tags
                    agent_memories = []
                    for memory in getattr(memory_engine, 'memory_store', []):
                        # Check voor coherence tags
                        coherence_tags = [tag for tag in getattr(memory, 'tags', []) if 'coherentie_' in tag]
                        if coherence_tags:
                            agent_memories.append({
                                "agent": agent_name,
                                "memory_id": getattr(memory, 'memory_id', 'unknown'),
                                "timestamp": getattr(memory, 'timestamp', datetime.now()).isoformat(),
                                "coherence_tags": coherence_tags,
                                "content_preview": getattr(memory, 'content', '')[:100] + "..." if len(getattr(memory, 'content', '')) > 100 else getattr(memory, 'content', ''),
                                "emotional_weight": getattr(memory, 'emotional_weight', 0),
                                "moral_significance": getattr(memory, 'moral_significance', 0)
                            })
                    
                    # Sorteer op timestamp en limiteer
                    agent_memories.sort(key=lambda x: x["timestamp"], reverse=True)
                    history["entries"].extend(agent_memories[:limit])
                    history["agents"].append(agent_name)
                    
            except Exception as e:
                logger.warning(f"Could not load memory for agent {agent_name}: {e}")
        
        # Sorteer alle entries op timestamp
        history["entries"].sort(key=lambda x: x["timestamp"], reverse=True)
        history["entries"] = history["entries"][:limit]
        history["total_entries"] = len(history["entries"])
        
        # Bereken date range
        if history["entries"]:
            timestamps = [entry["timestamp"] for entry in history["entries"]]
            history["date_range"] = {
                "start": min(timestamps),
                "end": max(timestamps)
            }
        
        return history
        
    except Exception as e:
        logger.error(f"Error getting coherence history: {e}")
        return {
            "entries": [],
            "agents": [],
            "total_entries": 0,
            "error": str(e)
        }

def _calculate_essenceual_trend(essenceual_by_period: Dict[str, float]) -> str:
    """Bereken cognitive trend richting"""
    if len(essenceual_by_period) < 2:
        return "insufficient_data"
    
    periods = sorted(essenceual_by_period.items())
    first_half = periods[:len(periods)//2]
    second_half = periods[len(periods)//2:]
    
    first_avg = sum(p[1] for p in first_half) / len(first_half)
    second_avg = sum(p[1] for p in second_half) / len(second_half)
    
    diff = second_avg - first_avg
    
    if diff > 2:
        return "strongly_improving"
    elif diff > 0.5:
        return "improving"
    elif diff < -2:
        return "declining"
    elif diff < -0.5:
        return "slightly_declining"
    else:
        return "stable"

def _assess_essenceual_health(avg_indicators: float) -> str:
    """Beoordeel overall cognitive health"""
    if avg_indicators > 20:
        return "excellent"
    elif avg_indicators > 15:
        return "very_good"
    elif avg_indicators > 10:
        return "good"
    elif avg_indicators > 5:
        return "moderate"
    else:
        return "needs_attention"
