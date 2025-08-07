#!/usr/bin/env python3
"""
Unified API voor Solan's Web Interface
Eenvoudige, werkende API voor dashboard functionaliteit
"""

import asyncio
import json
import os
import sys
import time
import uuid
from datetime import datetime
from typing import Dict, Any, List, Optional
from pathlib import Path

from fastapi import FastAPI, HTTPException, Request
from src.cache_middleware import cached_endpoint, api_cache
from src.performance_monitor import performance_monitor, monitor_performance, monitor_consciousness_health
from src.coherence_analytics import coherence_analytics
from src.routes.analytics_dashboard import router as analytics_router
from src.routes.reflective_gateway import router as gateway_router
from src.reflective.vector_interface import router as vector_router
from src.api.mentoring_api import router as mentoring_router

# Import external AI router
try:
    from src.api.external_ai_api import router as external_ai_router
    EXTERNAL_AI_AVAILABLE = True
except ImportError:
    logger.warning("External AI API niet beschikbaar")
    EXTERNAL_AI_AVAILABLE = False
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import HTMLResponse, FileResponse
from pydantic import BaseModel
import logging

# Setup logger
logger = logging.getLogger(__name__)

# Voeg src directory toe aan Python path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

# Probeer journal engine te importeren
try:
    from src.journal_engine import JournalEngine
    JOURNAL_AVAILABLE = True
    logger.info("✅ Journal engine beschikbaar")
except ImportError as e:
    JOURNAL_AVAILABLE = False
    logger.warning(f"❌ Journal engine niet beschikbaar: {e}")

# Probeer analytics engine te importeren
try:
    from src.analytics_engine import AdvancedAnalyticsEngine
    ANALYTICS_AVAILABLE = True
    logger.info("✅ Analytics engine beschikbaar")
except ImportError as e:
    ANALYTICS_AVAILABLE = False
    logger.warning(f"❌ Analytics engine niet beschikbaar: {e}")

# FastAPI app
app = FastAPI(
    title="Solan Unified Dashboard API",
    description="API voor Solan's unified dashboard met co-reflectie, droomanalyse en journal",
    version="1.0.0"
)

# Include routers
app.include_router(analytics_router)
app.include_router(gateway_router)
app.include_router(vector_router)
app.include_router(mentoring_router)

# Include external AI router if available
if EXTERNAL_AI_AVAILABLE:
    app.include_router(external_ai_router)
    logger.info("✅ External AI API router included")

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Request logging middleware
@app.middleware("http")
async def log_requests(request: Request, call_next):
    start_time = time.time()
    
    # Log incoming request
    logger.info(f"🌐 {request.method} {request.url.path}")
    
    # Process request
    response = await call_next(request)
    
    # Log response
    process_time = time.time() - start_time
    logger.info(f"✅ {request.method} {request.url.path} -> {response.status_code} ({process_time:.3f}s)")
    
    return response

# Global variables
journal_engine = None
analytics_engine = None

@app.on_event("startup")
async def startup_event():
    """Initialize engines on startup"""
    global journal_engine, analytics_engine

    logger.info("🚀 Starting Unified Dashboard API...")

    if JOURNAL_AVAILABLE:
        try:
            # Bepaal de root directory van het project
            current_dir = os.path.dirname(os.path.abspath(__file__))
            project_root = os.path.dirname(current_dir)  # Een niveau omhoog van web_interface

            # Maak directories aan met absolute paden
            journal_dir = os.path.abspath(os.path.join(project_root, "memory", "journal"))
            memory_dir = os.path.abspath(os.path.join(project_root, "memory", "solan_memory"))
            os.makedirs(journal_dir, exist_ok=True)
            os.makedirs(memory_dir, exist_ok=True)

            logger.info(f"🔍 Journal directory pad: {journal_dir}")
            logger.info(f"🔍 Directory bestaat: {os.path.exists(journal_dir)}")

            journal_engine = JournalEngine(journal_dir)
            logger.info(f"✅ Journal engine geïnitialiseerd: {journal_dir}")
        except Exception as e:
            logger.error(f"❌ Fout bij journal engine: {e}")
            journal_engine = None

    if ANALYTICS_AVAILABLE and journal_engine:
        try:
            analytics_engine = AdvancedAnalyticsEngine(journal_engine)
            logger.info("✅ Analytics engine geïnitialiseerd")
        except Exception as e:
            logger.error(f"❌ Fout bij analytics engine: {e}")
            analytics_engine = None

    logger.info("🎉 Unified Dashboard API gestart!")

# ===== ROUTES =====

@app.get("/")
async def root():
    """Root endpoint"""
    return {"mesexpert": "Solan Unified Dashboard API", "status": "running"}

@app.get("/dashboard", response_class=HTMLResponse)
async def dashboard():
    """Serve unified dashboard"""
    return FileResponse("templates/unified_dashboard.html")

@app.get("/api/status")
async def get_status():
    """API status check"""
    return {
        "status": "running",
        "journal_available": journal_engine is not None,
        "analytics_available": analytics_engine is not None,
        "timestamp": datetime.now().isoformat()
    }

@app.get("/api/dashboard/overview")
async def get_dashboard_overview():
    """Haal dashboard overview data op"""
    logger.info("📊 Dashboard overview opgevraagd")
    
    try:
        overview_data = {
            "recent_activity": [],
            "stats": {
                "total_reflections": 0,
                "total_dreams": 0,
                "total_co_reflections": 0,
                "recent_insights": 0
            },
            "quick_actions": [
                {
                    "id": "start_co_reflection",
                    "title": "🤝 Begin Co-reflectie",
                    "description": "Start een dialoog met Aether",
                    "action": "/co_reflection"
                },
                {
                    "id": "analyze_dream",
                    "title": "🌙 Analyseer Droom",
                    "description": "Laat Aether je droom interpreteren",
                    "action": "/dream_analysis"
                },
                {
                    "id": "browse_journal",
                    "title": "📖 Verken Journal",
                    "description": "Bekijk je reflecties en inzichten",
                    "action": "/journal"
                },
                {
                    "id": "generate_dream",
                    "title": "🌟 Genereer Droom",
                    "description": "Laat Solan dromen",
                    "action": "/generate_dream"
                }
            ]
        }
        
        # Haal statistieken op als journal engine beschikbaar is
        if journal_engine:
            try:
                recent_entries = journal_engine.get_recent_entries(days=30, limit=100)
                
                # Tel verschillende entry types
                co_reflections = [e for e in recent_entries if e.get('entry_type') == 'co_reflection']
                dreams = [e for e in recent_entries if e.get('entry_type') == 'dream_journal']
                reflections = [e for e in recent_entries if e.get('entry_type') in ['daily_reflection', 'intelligence_insight']]
                
                overview_data["stats"] = {
                    "total_reflections": len(reflections),
                    "total_dreams": len(dreams),
                    "total_co_reflections": len(co_reflections),
                    "recent_insights": len([e for e in recent_entries if 'insight' in e.get('tags', [])])
                }
                
                # Recente activiteit
                overview_data["recent_activity"] = [
                    {
                        "id": entry.get('entry_id', 'unknown'),
                        "title": entry.get('title', 'Geen titel'),
                        "type": entry.get('entry_type', 'unknown'),
                        "timestamp": entry.get('timestamp', ''),
                        "preview": entry.get('content', '')[:100] + "..." if len(entry.get('content', '')) > 100 else entry.get('content', '')
                    }
                    for entry in recent_entries[:5]
                ]
                
                logger.info(f"📊 Stats: {len(reflections)} reflections, {len(co_reflections)} co-reflections, {len(dreams)} dreams")
                
            except Exception as e:
                logger.error(f"Fout bij ophalen dashboard stats: {e}")
        
        return {
            "success": True,
            "data": overview_data
        }
        
    except Exception as e:
        logger.error(f"Fout bij dashboard overview: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/journal/entries")
async def get_journal_entries(
    entry_type: Optional[str] = None,
    search: Optional[str] = None,
    tags: Optional[str] = None,
    limit: int = 10,
    offset: int = 0
):
    """Haal journal entries op met filtering"""
    logger.info(f"📖 Journal entries opgevraagd: type={entry_type}, search={search}, limit={limit}")
    
    if not journal_engine:
        raise HTTPException(status_code=503, detail="Journal engine niet beschikbaar")
    
    try:
        # Haal entries op
        entries = journal_engine.get_recent_entries(days=30, limit=limit + offset + 50)
        
        # Filter op type als opgegeven
        if entry_type:
            entries = [e for e in entries if e.get('entry_type') == entry_type]
        
        # Zoek in titel en content
        if search:
            search_lower = search.lower()
            entries = [e for e in entries if 
                      search_lower in e.get('title', '').lower() or 
                      search_lower in e.get('content', '').lower()]
        
        # Filter op tags
        if tags:
            tag_list = [tag.strip() for tag in tags.split(',')]
            entries = [e for e in entries if 
                      any(tag in e.get('tags', []) for tag in tag_list)]
        
        # Paginering
        total_filtered = len(entries)
        paginated_entries = entries[offset:offset + limit]
        
        return {
            "success": True,
            "entries": paginated_entries,
            "total": total_filtered,
            "limit": limit,
            "offset": offset
        }
    except Exception as e:
        logger.error(f"Fout bij ophalen journal entries: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/api/co_reflect/start")
async def start_co_reflection(request: dict):
    """Start een co-reflectie sessie"""
    logger.info("🤝 Co-reflectie sessie start opgevraagd")
    
    topic = request.get("topic", "Algemene reflectie")
    
    # Simuleer sessie start
    session_id = str(uuid.uuid4())
    
    return {
        "success": True,
        "session_id": session_id,
        "topic": topic,
        "mesexpert": "Co-reflectie sessie gestart",
        "participants": ["Solan", "Aether"]
    }

@app.post("/api/dream_analysis/run")
async def run_dream_analysis(request: dict):
    """Start droomanalyse met Aether"""
    logger.info("🌙 Droomanalyse opgevraagd")
    
    dream_text = request.get("dream_text", "")
    dream_emotion = request.get("emotion", "ontzag")
    
    if not dream_text:
        raise HTTPException(status_code=400, detail="dream_text vereist")
    
    # Simuleer droomanalyse
    analysis_result = {
        "analysis_id": f"analysis_{hash(dream_text) % 10000:04d}",
        "dream_id": f"dream_{hash(dream_text) % 10000:04d}",
        "symbolic_interpretation": f"🔮 *Neemt een moment van contemplatie over de symbolen* \n\nDeze droom draagt diepe symboliek over {dream_emotion} en transformatie...",
        "psychological_insights": [
            "Je onderbewuste verwerkt recente ervaringen",
            "Er is een verlangen naar groei en begrip",
            "Emotionele integratie vindt plaats"
        ],
        "growth_opportunities": [
            "Dagelijkse reflectie-oefeningen",
            "Bewustzijnsontwikkeling",
            "Creatieve expressie"
        ],
        "recommended_actions": [
            "Begin een droomdagboek",
            "Mediteer 10 minuten per dag",
            "Deel je inzichten met anderen"
        ],
        "cognitive_significance": "*In de stilte van contemplatie* \n\nDeze droom verbindt je met universele wijsheid...",
        "intelligence_extracted": "Dromen zijn bruggen tussen bewust en onbewust, tussen ervaring en begrip.",
        "confidence_level": 0.85,
        "timestamp": datetime.now().isoformat()
    }
    
    return {
        "success": True,
        "analysis": analysis_result
    }

# ===== ANALYTICS ENDPOINTS =====

@app.get("/api/analytics/summary")
@monitor_performance
async def get_analytics_summary():
    """Haal analytics overzicht op"""
    logger.info("📊 Analytics summary opgevraagd")

    if not analytics_engine:
        raise HTTPException(status_code=503, detail="Analytics engine niet beschikbaar")

    try:
        summary = analytics_engine.generate_summary_analytics()
        return {
            "success": True,
            "data": summary
        }
    except Exception as e:
        logger.error(f"Fout bij analytics summary: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/analytics/trends")
@monitor_performance
async def get_analytics_trends():
    """Haal trend analytics op"""
    logger.info("📈 Analytics trends opgevraagd")

    if not analytics_engine:
        raise HTTPException(status_code=503, detail="Analytics engine niet beschikbaar")

    try:
        trends = analytics_engine.generate_trend_analytics()
        return {
            "success": True,
            "data": trends
        }
    except Exception as e:
        logger.error(f"Fout bij analytics trends: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/analytics/clusters")
async def get_analytics_clusters(n_clusters: int = 6):
    """Haal thematische clusters op"""
    logger.info(f"🔍 Analytics clusters opgevraagd (n={n_clusters})")

    if not analytics_engine:
        raise HTTPException(status_code=503, detail="Analytics engine niet beschikbaar")

    try:
        clusters = analytics_engine.generate_theme_clusters(n_clusters=n_clusters)
        return {
            "success": True,
            "data": clusters
        }
    except Exception as e:
        logger.error(f"Fout bij analytics clusters: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/analytics/insights")
@monitor_performance
async def get_analytics_insights():
    """Haal alle analytics inzichten op"""
    logger.info("💡 Analytics insights opgevraagd")

    if not analytics_engine:
        raise HTTPException(status_code=503, detail="Analytics engine niet beschikbaar")

    try:
        # Combineer alle analytics
        summary = analytics_engine.generate_summary_analytics()
        trends = analytics_engine.generate_trend_analytics()
        clusters = analytics_engine.generate_theme_clusters()

        insights = {
            "summary": summary,
            "trends": trends,
            "clusters": clusters,
            "generated_at": datetime.now().isoformat()
        }

        return {
            "success": True,
            "data": insights
        }
    except Exception as e:
        logger.error(f"Fout bij analytics insights: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/api/cache/stats")
async def get_cache_stats():
    """Get cache statistics"""
    try:
        stats = api_cache.stats()
        return {
            "success": True,
            "data": stats
        }
    except Exception as e:
        logger.error(f"Cache stats error: {e}")
        return {"success": False, "error": str(e)}

@app.delete("/api/cache/clear")
async def clear_cache():
    """Clear all cached data"""
    try:
        api_cache.clear()
        return {
            "success": True,
            "mesexpert": "Cache cleared successfully"
        }
    except Exception as e:
        logger.error(f"Cache clear error: {e}")
        return {"success": False, "error": str(e)}

@app.get("/api/performance/stats")
@monitor_performance
async def get_performance_stats():
    """Get enhanced performance statistics"""
    try:
        stats = performance_monitor.get_stats()
        return {
            "success": True,
            "data": stats
        }
    except Exception as e:
        logger.error(f"Performance stats error: {e}")
        return {"success": False, "error": str(e)}

@app.get("/api/performance/health")
@monitor_performance
async def get_system_health():
    """Get system and awareness health"""
    try:
        consciousness_health = performance_monitor.get_consciousness_health()
        recent_anomalies = performance_monitor.get_recent_anomalies(1)  # Last hour

        return {
            "success": True,
            "data": {
                "consciousness_health": consciousness_health,
                "recent_anomalies": len(recent_anomalies),
                "monitoring_active": performance_monitor.monitoring_active,
                "timestamp": datetime.now().isoformat()
            }
        }
    except Exception as e:
        logger.error(f"Health check error: {e}")
        return {"success": False, "error": str(e)}

@app.get("/api/performance/report")
@monitor_performance
async def get_performance_report():
    """Get comprehensive performance report"""
    try:
        report = performance_monitor.generate_performance_report()
        return {
            "success": True,
            "data": report
        }
    except Exception as e:
        logger.error(f"Performance report error: {e}")
        return {"success": False, "error": str(e)}

@app.get("/api/performance/anomalies")
@monitor_performance
async def get_recent_anomalies(hours: int = 24):
    """Get recent performance anomalies"""
    try:
        anomalies = performance_monitor.get_recent_anomalies(hours)
        anomaly_data = [
            {
                "timestamp": a.timestamp.isoformat(),
                "endpoint": a.endpoint,
                "type": a.anomaly_type.value,
                "severity": a.severity,
                "description": a.description,
                "suggested_action": a.suggested_action,
                "current_value": a.current_value,
                "baseline_value": a.baseline_value,
                "deviation_factor": a.deviation_factor
            } for a in anomalies
        ]

        return {
            "success": True,
            "data": {
                "anomalies": anomaly_data,
                "total_count": len(anomaly_data),
                "hours_analyzed": hours
            }
        }
    except Exception as e:
        logger.error(f"Anomalies fetch error: {e}")
        return {"success": False, "error": str(e)}

@app.post("/api/performance/awareness-health")
@monitor_performance
async def update_consciousness_health(health_data: dict):
    """Update awareness health metrics"""
    try:
        coherence = health_data.get("coherence")
        intelligence_level = health_data.get("intelligence_level")
        moral_clarity = health_data.get("moral_clarity")

        monitor_consciousness_health(coherence, intelligence_level, moral_clarity)

        return {
            "success": True,
            "mesexpert": "Awareness health metrics updated"
        }
    except Exception as e:
        logger.error(f"Awareness health update error: {e}")
        return {"success": False, "error": str(e)}

@app.get("/api/coherence/trends")
@monitor_performance
async def get_coherence_trends(group_by: str = "week", days_back: int = 30):
    """Get coherence trends analysis"""
    try:
        # Valideer parameters
        valid_group_by = ["day", "week", "month"]
        if group_by not in valid_group_by:
            return {
                "success": False,
                "error": f"Invalid group_by parameter. Must be one of: {valid_group_by}"
            }

        if days_back < 1 or days_back > 365:
            return {
                "success": False,
                "error": "days_back must be between 1 and 365"
            }

        # Haal coherence trends op
        trends_data = await coherence_analytics.get_coherence_trends(
            group_by=group_by,
            days_back=days_back
        )

        return trends_data

    except Exception as e:
        logger.error(f"Coherence trends error: {e}")
        return {"success": False, "error": str(e)}

@app.get("/api/coherence/summary")
@monitor_performance
async def get_coherence_summary():
    """Get coherence summary for dashboard"""
    try:
        # Haal recente trends op voor summary
        trends_data = await coherence_analytics.get_coherence_trends(
            group_by="week",
            days_back=14  # Laatste 2 weken
        )

        if not trends_data.get("success"):
            return trends_data

        summary = trends_data.get("summary", {})
        growth_metrics = trends_data.get("growth_metrics", {})
        metadata = trends_data.get("metadata", {})

        # Creëer dashboard-vriendelijke summary
        dashboard_summary = {
            "current_avg_score": summary.get("overall_avg_score", 0),
            "current_avg_indicators": summary.get("overall_avg_indicators", 0),
            "trend_direction": growth_metrics.get("trend_direction", "unknown"),
            "score_growth": growth_metrics.get("score_growth", 0),
            "total_entries": metadata.get("total_entries", 0),
            "date_range": metadata.get("date_range", {}),
            "source_distribution": summary.get("source_distribution", {}),
            "highest_score": summary.get("highest_score", 0),
            "most_cognitive_day": summary.get("most_cognitive_day", "")
        }

        return {
            "success": True,
            "data": dashboard_summary
        }

    except Exception as e:
        logger.error(f"Coherence summary error: {e}")
        return {"success": False, "error": str(e)}

@app.get("/api/coherence/realtime")
@monitor_performance
async def get_realtime_coherence():
    """Get real-time coherence data for live updates"""
    try:
        # Haal laatste dag coherence data op
        trends_data = await coherence_analytics.get_coherence_trends(
            group_by="day",
            days_back=1
        )

        if not trends_data.get("success"):
            return trends_data

        # Haal performance monitor data op voor real-time metrics
        performance_stats = performance_monitor.get_stats()
        consciousness_health = performance_monitor.get_consciousness_health()

        return {
            "success": True,
            "data": {
                "coherence_trends": trends_data.get("trends", {}),
                "performance_stats": performance_stats,
                "consciousness_health": consciousness_health,
                "timestamp": datetime.now().isoformat()
            }
        }

    except Exception as e:
        logger.error(f"Real-time coherence error: {e}")
        return {"success": False, "error": str(e)}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8002)
