#!/usr/bin/env python3
"""
Solān AI Observatorium - Production Configuration
Environment-based configuration management for production deployment
"""

import os
import secrets
from typing import List, Optional
from functools import lru_cache

try:
    from pydantic_settings import BaseSettings
    from pydantic import validator
except ImportError:
    try:
        from pydantic import BaseSettings, validator
    except ImportError:
        # Fallback for older versions
        class BaseSettings:
            def __init__(self, **kwargs):
                for key, value in kwargs.items():
                    setattr(self, key, value)

        def validator(field_name, pre=False):
            def decorator(func):
                return func
            return decorator

class ProductionSettings(BaseSettings):
    """Production configuration settings"""
    
    # API Configuration
    api_host: str = "0.0.0.0"
    api_port: int = 8000
    api_workers: int = 4
    api_title: str = "Solān AI Analysis API"
    api_description: str = "Advanced AI analysis toolkit for bias detection and ethical alignment"
    api_version: str = "1.0.0"
    
    # Security Configuration
    secret_key: str = secrets.token_urlsafe(32)
    access_token_expire_minutes: int = 30
    algorithm: str = "HS256"
    
    # CORS Configuration
    allowed_origins: List[str] = [
        "http://localhost:3000",
        "http://localhost:8080", 
        "http://127.0.0.1:5500",
        "https://solanai.ai",
        "https://www.solanai.ai"
    ]
    allowed_methods: List[str] = ["GET", "POST", "OPTIONS"]
    allowed_headers: List[str] = ["*"]
    allow_credentials: bool = True
    
    # Rate Limiting Configuration
    rate_limit_enabled: bool = True
    rate_limit_requests_per_minute: int = 10
    rate_limit_burst: int = 20
    
    # Logging Configuration
    log_level: str = "INFO"
    log_format: str = "json"
    log_file: Optional[str] = "logs/solan_observatorium.log"
    log_rotation: str = "1 day"
    log_retention: str = "30 days"
    
    # Cache Configuration
    cache_enabled: bool = True
    cache_ttl: int = 300  # 5 minutes
    cache_max_size: int = 1000
    redis_url: Optional[str] = None
    
    # Database Configuration (for future use)
    database_url: Optional[str] = None
    database_echo: bool = False
    
    # Monitoring Configuration
    metrics_enabled: bool = True
    health_check_enabled: bool = True
    prometheus_enabled: bool = False
    prometheus_port: int = 9090
    
    # Performance Configuration
    max_request_size: int = 10 * 1024 * 1024  # 10MB
    request_timeout: int = 30  # seconds
    keepalive_timeout: int = 5
    
    # AI Model Configuration
    default_models: List[str] = ["analytical", "empathetic"]
    max_models_per_request: int = 4
    max_prompt_length: int = 2000
    min_prompt_length: int = 10
    
    # Feature Flags
    bias_detection_enabled: bool = True
    ethical_alignment_enabled: bool = True
    detailed_analysis_enabled: bool = True
    export_functionality_enabled: bool = True
    
    # Development/Debug Configuration
    debug: bool = False
    reload: bool = False
    testing: bool = False
    
    @validator('allowed_origins', pre=True)
    def parse_origins(cls, v):
        if isinstance(v, str):
            return [origin.strip() for origin in v.split(',')]
        return v
    
    @validator('log_level')
    def validate_log_level(cls, v):
        valid_levels = ['DEBUG', 'INFO', 'WARNING', 'ERROR', 'CRITICAL']
        if v.upper() not in valid_levels:
            raise ValueError(f'Log level must be one of: {valid_levels}')
        return v.upper()
    
    @validator('secret_key')
    def validate_secret_key(cls, v):
        if len(v) < 32:
            raise ValueError('Secret key must be at least 32 characters long')
        return v
    
    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"
        case_sensitive = False
        
        # Environment variable prefixes
        env_prefix = ""
        
        # Field aliases for environment variables
        fields = {
            'api_host': {'env': 'API_HOST'},
            'api_port': {'env': 'API_PORT'},
            'api_workers': {'env': 'API_WORKERS'},
            'secret_key': {'env': 'SECRET_KEY'},
            'allowed_origins': {'env': 'ALLOWED_ORIGINS'},
            'rate_limit_enabled': {'env': 'RATE_LIMIT_ENABLED'},
            'rate_limit_requests_per_minute': {'env': 'RATE_LIMIT_REQUESTS_PER_MINUTE'},
            'log_level': {'env': 'LOG_LEVEL'},
            'log_format': {'env': 'LOG_FORMAT'},
            'cache_enabled': {'env': 'CACHE_ENABLED'},
            'cache_ttl': {'env': 'CACHE_TTL'},
            'redis_url': {'env': 'REDIS_URL'},
            'database_url': {'env': 'DATABASE_URL'},
            'metrics_enabled': {'env': 'METRICS_ENABLED'},
            'health_check_enabled': {'env': 'HEALTH_CHECK_ENABLED'},
            'debug': {'env': 'DEBUG'},
            'testing': {'env': 'TESTING'}
        }

class DevelopmentSettings(ProductionSettings):
    """Development-specific settings"""
    
    debug: bool = True
    reload: bool = True
    log_level: str = "DEBUG"
    rate_limit_enabled: bool = False
    cache_enabled: bool = False
    
    allowed_origins: List[str] = [
        "http://localhost:3000",
        "http://localhost:8080",
        "http://127.0.0.1:5500",
        "http://localhost:5173",  # Vite dev server
        "http://localhost:3001"   # Alternative dev port
    ]

class TestingSettings(ProductionSettings):
    """Testing-specific settings"""
    
    testing: bool = True
    debug: bool = True
    log_level: str = "WARNING"
    rate_limit_enabled: bool = False
    cache_enabled: bool = False
    database_url: str = "sqlite:///./test.db"
    
    # Use in-memory cache for testing
    cache_ttl: int = 1
    
    # Reduced limits for testing
    max_models_per_request: int = 2
    max_prompt_length: int = 500

@lru_cache()
def get_settings() -> ProductionSettings:
    """Get cached settings instance based on environment"""
    
    environment = os.getenv("ENVIRONMENT", "production").lower()
    
    if environment == "development":
        return DevelopmentSettings()
    elif environment == "testing":
        return TestingSettings()
    else:
        return ProductionSettings()

def get_uvicorn_config(settings: ProductionSettings) -> dict:
    """Get Uvicorn configuration for production"""
    
    config = {
        "host": settings.api_host,
        "port": settings.api_port,
        "log_level": settings.log_level.lower(),
        "access_log": True,
        "use_colors": not settings.log_format == "json",
        "server_header": False,  # Security: hide server info
        "date_header": False,    # Security: hide date info
    }
    
    # Production-specific settings
    if not settings.debug:
        config.update({
            "workers": settings.api_workers,
            "keepalive_timeout": settings.keepalive_timeout,
            "timeout_keep_alive": settings.keepalive_timeout,
            "limit_max_requests": 1000,  # Restart workers after 1000 requests
            "limit_concurrency": 100,    # Max concurrent connections
        })
    else:
        # Development settings
        config.update({
            "reload": settings.reload,
            "reload_dirs": ["./"],
            "reload_includes": ["*.py", "*.html"],
        })
    
    return config

def validate_production_config(settings: ProductionSettings) -> List[str]:
    """Validate production configuration and return warnings/errors"""
    
    warnings = []
    
    # Security checks
    if settings.secret_key == "your-secret-key-here-change-in-production":
        warnings.append("⚠️ SECRET_KEY is using default value - change for production!")
    
    if settings.debug and not settings.testing:
        warnings.append("⚠️ DEBUG mode is enabled - disable for production!")
    
    if not settings.rate_limit_enabled and not settings.testing:
        warnings.append("⚠️ Rate limiting is disabled - enable for production!")
    
    # Performance checks
    if settings.api_workers < 2 and not settings.debug:
        warnings.append("⚠️ Consider using more workers for production (recommended: 2-4)")
    
    if settings.cache_ttl < 60 and settings.cache_enabled:
        warnings.append("⚠️ Cache TTL is very low - consider increasing for production")
    
    # CORS checks
    if "*" in settings.allowed_origins:
        warnings.append("⚠️ CORS allows all origins - restrict for production!")
    
    return warnings

def print_config_summary(settings: ProductionSettings):
    """Print configuration summary"""
    
    print("🔧 SOLĀN OBSERVATORIUM CONFIGURATION")
    print("=" * 50)
    print(f"Environment: {os.getenv('ENVIRONMENT', 'production')}")
    print(f"API Host: {settings.api_host}:{settings.api_port}")
    print(f"Workers: {settings.api_workers}")
    print(f"Debug Mode: {settings.debug}")
    print(f"Rate Limiting: {settings.rate_limit_enabled}")
    print(f"Cache Enabled: {settings.cache_enabled}")
    print(f"Log Level: {settings.log_level}")
    print(f"Allowed Origins: {len(settings.allowed_origins)} configured")
    
    # Validate and show warnings
    warnings = validate_production_config(settings)
    if warnings:
        print("\n⚠️ CONFIGURATION WARNINGS:")
        for warning in warnings:
            print(f"   {warning}")
    else:
        print("\n✅ Configuration looks good for production!")

if __name__ == "__main__":
    # Test configuration loading
    settings = get_settings()
    print_config_summary(settings)
    
    # Print Uvicorn config
    print(f"\n🚀 Uvicorn Configuration:")
    uvicorn_config = get_uvicorn_config(settings)
    for key, value in uvicorn_config.items():
        print(f"   {key}: {value}")
