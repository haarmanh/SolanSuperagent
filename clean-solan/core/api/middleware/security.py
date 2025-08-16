"""
Security middleware for Solān API
Handles CORS, rate limiting, authentication, and security headers
"""

import time
from typing import Dict, Any
from fastapi import Request, Response, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from slowapi import Limiter, _rate_limit_exceeded_handler
from slowapi.util import get_remote_address
from slowapi.errors import RateLimitExceeded

# Rate limiter configuration
limiter = Limiter(key_func=get_remote_address)

def configure_cors(app):
    """Configure CORS middleware with security best practices"""
    
    # Production-ready CORS settings
    allowed_origins = [
        "http://localhost:3000",  # React dev server
        "http://localhost:8080",  # Vue dev server
        "http://127.0.0.1:3000",
        "http://127.0.0.1:8080",
        # Add your production domains here
    ]
    
    app.add_middleware(
        CORSMiddleware,
        allow_origins=allowed_origins,  # Specific origins only
        allow_credentials=True,
        allow_methods=["GET", "POST", "PUT", "DELETE"],  # Specific methods
        allow_headers=["*"],
        max_age=600,  # Cache preflight for 10 minutes
    )

def configure_rate_limiting(app):
    """Configure rate limiting"""
    app.state.limiter = limiter
    app.add_exception_handler(RateLimitExceeded, _rate_limit_exceeded_handler)

async def security_headers_middleware(request: Request, call_next):
    """Add security headers to all responses"""
    
    response = await call_next(request)
    
    # Security headers
    response.headers["X-Content-Type-Options"] = "nosniff"
    response.headers["X-Frame-Options"] = "DENY"
    response.headers["X-XSS-Protection"] = "1; mode=block"
    response.headers["Strict-Transport-Security"] = "max-age=31536000; includeSubDomains"
    response.headers["Referrer-Policy"] = "strict-origin-when-cross-origin"
    response.headers["Content-Security-Policy"] = "default-src 'self'"
    
    return response

async def request_logging_middleware(request: Request, call_next):
    """Log all requests for monitoring"""
    
    start_time = time.time()
    
    # Log request
    print(f"📥 {request.method} {request.url.path} - {get_remote_address(request)}")
    
    response = await call_next(request)
    
    # Log response time
    process_time = time.time() - start_time
    response.headers["X-Process-Time"] = str(process_time)
    
    # Log slow requests
    if process_time > 1.0:
        print(f"⚠️ Slow request: {request.method} {request.url.path} took {process_time:.2f}s")
    
    print(f"📤 {response.status_code} - {process_time:.3f}s")
    
    return response

async def api_key_middleware(request: Request, call_next):
    """Simple API key validation for sensitive endpoints"""
    
    # List of endpoints that require API key
    protected_endpoints = [
        "/api/god-core/consciousness-assessment",
        "/api/ethics/bias-assessment"
    ]
    
    # Check if endpoint requires API key
    if any(request.url.path.startswith(endpoint) for endpoint in protected_endpoints):
        api_key = request.headers.get("X-API-Key")
        
        if not api_key:
            raise HTTPException(
                status_code=401,
                detail="API key required for this endpoint"
            )
        
        # Simple API key validation (in production, use proper key management)
        valid_keys = ["solan-dev-key", "solan-prod-key"]  # Replace with secure key management
        
        if api_key not in valid_keys:
            raise HTTPException(
                status_code=403,
                detail="Invalid API key"
            )
    
    response = await call_next(request)
    return response

def get_rate_limit_for_endpoint(endpoint: str) -> str:
    """Get rate limit configuration for specific endpoint"""
    
    rate_limits = {
        # God Core endpoints
        "/api/god-core/identity": "30/minute",
        "/api/god-core/ethics-test": "10/minute", 
        "/api/god-core/consciousness-assessment": "5/minute",
        "/api/god-core/reflection": "20/minute",
        "/api/god-core/wisdom": "15/minute",
        
        # Ethics endpoints
        "/api/ethics/dilemma-analysis": "5/minute",
        "/api/ethics/framework-assessment": "10/minute",
        "/api/ethics/bias-assessment": "3/minute",
        "/api/ethics/principles": "60/minute",
        "/api/ethics/frameworks": "60/minute",
        
        # Default rate limit
        "default": "100/minute"
    }
    
    return rate_limits.get(endpoint, rate_limits["default"])

class SecurityConfig:
    """Security configuration class"""
    
    def __init__(self):
        self.api_keys_enabled = True
        self.rate_limiting_enabled = True
        self.cors_enabled = True
        self.security_headers_enabled = True
        self.request_logging_enabled = True
    
    def is_development_mode(self) -> bool:
        """Check if running in development mode"""
        import os
        return os.getenv("ENVIRONMENT", "development") == "development"
    
    def get_allowed_origins(self) -> list:
        """Get allowed CORS origins based on environment"""
        if self.is_development_mode():
            return [
                "http://localhost:3000",
                "http://localhost:8080", 
                "http://127.0.0.1:3000",
                "http://127.0.0.1:8080"
            ]
        else:
            # Production origins - replace with your actual domains
            return [
                "https://your-production-domain.com",
                "https://api.your-domain.com"
            ]

# Global security config instance
security_config = SecurityConfig()

def setup_security_middleware(app):
    """Setup all security middleware"""
    
    # Configure CORS
    if security_config.cors_enabled:
        configure_cors(app)
    
    # Configure rate limiting
    if security_config.rate_limiting_enabled:
        configure_rate_limiting(app)
    
    # Add security headers middleware
    if security_config.security_headers_enabled:
        app.middleware("http")(security_headers_middleware)
    
    # Add request logging middleware
    if security_config.request_logging_enabled:
        app.middleware("http")(request_logging_middleware)
    
    # Add API key middleware
    if security_config.api_keys_enabled:
        app.middleware("http")(api_key_middleware)
    
    print("🔒 Security middleware configured successfully")

# Rate limiting decorators for specific endpoints
def rate_limit_god_core():
    """Rate limit decorator for God Core endpoints"""
    return limiter.limit("10/minute")

def rate_limit_ethics():
    """Rate limit decorator for Ethics endpoints"""
    return limiter.limit("5/minute")

def rate_limit_general():
    """Rate limit decorator for general endpoints"""
    return limiter.limit("30/minute")
