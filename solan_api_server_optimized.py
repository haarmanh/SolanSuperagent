#!/usr/bin/env python3
"""
🌐 Solān API Server - Optimized Version
Clean, fast, maintainable API server with modular architecture
"""

import asyncio
import uvicorn
from datetime import datetime
from fastapi import FastAPI, HTTPException
from fastapi.responses import JSONResponse
from contextlib import asynccontextmanager

# Import optimized modules
from src.api.routers import consciousness_core, ethics
from src.api.middleware.security import setup_security_middleware, limiter, rate_limit_general
from src.config_cache import config_cache
from src.monitoring import start_metrics_server, monitor_performance
from src.services.redis_cache_service import cache_service

# Import dialogue router if available
try:
    from src.api.dialogue_api import router as dialogue_router
    DIALOGUE_AVAILABLE = True
    print("✅ Dialogue API module loaded successfully")
except ImportError as e:
    print(f"⚠️ Dialogue API not available: {e}")
    DIALOGUE_AVAILABLE = False

@asynccontextmanager
async def lifespan(app: FastAPI):
    """Application lifespan management"""
    
    # Startup
    print("🚀 Starting Solān API Server...")

    # Initialize Redis cache service
    try:
        redis_connected = await cache_service.connect()
        if redis_connected:
            print("✅ Redis cache service connected")
        else:
            print("⚠️ Redis cache service failed to connect - running without cache")
    except Exception as e:
        print(f"⚠️ Redis connection error: {e}")

    # Start metrics server
    try:
        start_metrics_server(port=8001)
        print("📊 Metrics server started on port 8001")
    except Exception as e:
        print(f"⚠️ Metrics server failed to start: {e}")

    # Preload critical configurations
    try:
        await config_cache.load_config("coherence_gate_config.json")
        print("✅ Core configuration preloaded")
    except Exception as e:
        print(f"⚠️ Failed to preload config: {e}")

    print("✅ Solān API Server startup complete")
    
    yield
    
    # Shutdown
    print("🛑 Shutting down Solān API Server...")

    # Disconnect Redis
    try:
        await cache_service.disconnect()
        print("✅ Redis cache service disconnected")
    except Exception as e:
        print(f"⚠️ Redis disconnect error: {e}")

    # Clear local caches
    await config_cache.clear_cache()
    print("✅ Cleanup complete")

# Create FastAPI app with optimized configuration
app = FastAPI(
    title="Solān AI Consciousness Platform API",
    description="Professional API for AI consciousness assessment and ethical evaluation",
    version="2.0.0",
    docs_url="/docs",
    redoc_url="/redoc",
    lifespan=lifespan
)

# Setup security middleware
setup_security_middleware(app)

# Include routers
app.include_router(consciousness_core.router)
app.include_router(ethics.router)

# Include dialogue router if available
if DIALOGUE_AVAILABLE:
    app.include_router(dialogue_router)

@app.get("/")
@rate_limit_general()
@monitor_performance
async def root():
    """Root endpoint with system status"""
    return {
        "message": "Solān AI Consciousness Platform API",
        "version": "2.0.0",
        "status": "operational",
        "timestamp": datetime.now().isoformat(),
        "documentation": "/docs",
        "metrics": "http://localhost:8001/metrics",
        "available_services": {
            "god_core": True,
            "ethics": True,
            "dialogue": DIALOGUE_AVAILABLE
        }
    }

@app.get("/health")
@rate_limit_general()
async def health_check():
    """Health check endpoint for monitoring"""
    
    health_status = {
        "status": "healthy",
        "timestamp": datetime.now().isoformat(),
        "version": "2.0.0",
        "services": {
            "api": "operational",
            "god_core": "operational" if god_core.GOD_CORE_AVAILABLE else "unavailable",
            "ethics": "operational",
            "dialogue": "operational" if DIALOGUE_AVAILABLE else "unavailable"
        },
        "performance": {
            "local_cache_size": len(config_cache._local_cache),
            "redis_cache": "connected" if cache_service.is_connected else "disconnected",
            "uptime": "operational"
        }
    }
    
    # Check if any critical services are down
    critical_services = ["api", "god_core", "ethics"]
    if any(health_status["services"][service] != "operational" for service in critical_services):
        health_status["status"] = "degraded"
    
    return health_status

@app.get("/cache/stats")
@rate_limit_general()
@monitor_performance
async def cache_statistics():
    """Get cache performance statistics"""

    stats = {
        "timestamp": datetime.now().isoformat(),
        "local_cache": {
            "config_entries": len(config_cache._local_cache),
            "enabled": True
        },
        "redis_cache": await cache_service.get_cache_stats() if cache_service.is_connected else {
            "connected": False,
            "message": "Redis not connected"
        }
    }

    return {
        "status": "success",
        "cache_statistics": stats
    }

@app.get("/api/status")
@rate_limit_general()
@monitor_performance
async def api_status():
    """Detailed API status and capabilities"""
    return {
        "status": "operational",
        "timestamp": datetime.now().isoformat(),
        "version": "2.0.0",
        "architecture": "modular",
        "features": {
            "async_operations": True,
            "rate_limiting": True,
            "security_headers": True,
            "performance_monitoring": True,
            "dependency_injection": True,
            "caching": True
        },
        "endpoints": {
            "god_core": [
                "/api/god-core/identity",
                "/api/god-core/ethics-test",
                "/api/god-core/consciousness-assessment",
                "/api/god-core/reflection",
                "/api/god-core/wisdom",
                "/api/god-core/status"
            ],
            "ethics": [
                "/api/ethics/dilemma-analysis",
                "/api/ethics/framework-assessment", 
                "/api/ethics/bias-assessment",
                "/api/ethics/principles",
                "/api/ethics/frameworks"
            ],
            "system": [
                "/",
                "/health",
                "/api/status",
                "/docs",
                "/redoc"
            ]
        },
        "performance": {
            "async_config_loading": True,
            "redis_caching": cache_service.is_connected,
            "connection_pooling": "active" if cache_service.is_connected else "planned",
            "caching_enabled": True,
            "monitoring_enabled": True
        }
    }

@app.exception_handler(HTTPException)
async def http_exception_handler(request, exc):
    """Custom HTTP exception handler"""
    return JSONResponse(
        status_code=exc.status_code,
        content={
            "error": True,
            "status_code": exc.status_code,
            "message": exc.detail,
            "timestamp": datetime.now().isoformat(),
            "path": str(request.url.path)
        }
    )

@app.exception_handler(Exception)
async def general_exception_handler(request, exc):
    """General exception handler for unexpected errors"""
    print(f"❌ Unexpected error: {exc}")
    
    return JSONResponse(
        status_code=500,
        content={
            "error": True,
            "status_code": 500,
            "message": "Internal server error",
            "timestamp": datetime.now().isoformat(),
            "path": str(request.url.path)
        }
    )

def create_app():
    """Application factory"""
    return app

async def main():
    """Main application entry point"""
    print("🚀 SOLĀN API SERVER - OPTIMIZED VERSION")
    print("=" * 60)
    print("🎯 Clean, Fast, Maintainable Architecture")
    print("✅ Modular design with dependency injection")
    print("✅ Async operations with caching")
    print("✅ Security middleware and rate limiting")
    print("✅ Performance monitoring")
    print("=" * 60)
    
    # Configuration
    config = {
        "host": "0.0.0.0",
        "port": 8000,
        "reload": True,  # Set to False in production
        "workers": 1,    # Increase for production
        "log_level": "info"
    }
    
    print(f"🌐 Starting server on http://{config['host']}:{config['port']}")
    print(f"📚 API Documentation: http://{config['host']}:{config['port']}/docs")
    print(f"📊 Metrics: http://{config['host']}:8001/metrics")
    
    # Start server
    await uvicorn.run(
        "solan_api_server_optimized:app",
        **config
    )

if __name__ == "__main__":
    asyncio.run(main())
