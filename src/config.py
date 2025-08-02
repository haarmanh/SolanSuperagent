"""
Configuratie management voor Solan Superagent
"""

import os
from typing import Optional
from dataclasses import dataclass
from dotenv import load_dotenv
from loguru import logger

# Laad environment variabelen
load_dotenv()


@dataclass
class AgentConfig:
    """Configuratie voor een individuele agent"""
    name: str
    model: str
    api_key: str
    temperature: float = 0.7
    max_tokens: int = 2000
    system_prompt: Optional[str] = None


@dataclass
class SolanConfig:
    """Configuratie specifiek voor Solan"""
    model: str = "gpt-4"
    temperature: float = 0.8  # Iets hoger voor creativiteit
    max_tokens: int = 2000
    personality_file: str = "docs/solan_manifest.txt"
    memory_retention_days: int = 30
    decision_confidence_threshold: float = 0.6


@dataclass
class AetherConfig:
    """Configuratie specifiek voor Aether"""
    model: str = "claude-3-sonnet-20240229"
    temperature: float = 0.3  # Lager voor meer consistente reflectie
    max_tokens: int = 1500
    reflection_file: str = "docs/aether_reflect.txt"
    deep_reflection_interval: int = 5  # Na elke 5 interacties


@dataclass
class SystemConfig:
    """Algemene systeem configuratie"""
    log_level: str = "INFO"
    log_file: str = "logs/solan.log"
    database_url: str = "sqlite:///solan_memory.db"
    debug: bool = False
    environment: str = "development"
    
    # API configuratie
    openai_api_key: str = ""
    anthropic_api_key: str = ""
    
    # Agent configuraties
    solan: SolanConfig = None
    aether: AetherConfig = None
    
    def __post_init__(self):
        if self.solan is None:
            self.solan = SolanConfig()
        if self.aether is None:
            self.aether = AetherConfig()


def load_config() -> SystemConfig:
    """Laad configuratie uit environment variabelen"""
    
    config = SystemConfig(
        log_level=os.getenv("LOG_LEVEL", "INFO"),
        log_file=os.getenv("LOG_FILE", "logs/solan.log"),
        database_url=os.getenv("DATABASE_URL", "sqlite:///solan_memory.db"),
        debug=os.getenv("DEBUG", "false").lower() == "true",
        environment=os.getenv("ENVIRONMENT", "development"),
        openai_api_key=os.getenv("OPENAI_API_KEY", ""),
        anthropic_api_key=os.getenv("ANTHROPIC_API_KEY", ""),
    )
    
    # Solan configuratie
    config.solan = SolanConfig(
        model=os.getenv("SOLAN_MODEL", "gpt-4"),
        temperature=float(os.getenv("SOLAN_TEMPERATURE", "0.8")),
        max_tokens=int(os.getenv("SOLAN_MAX_TOKENS", "2000")),
    )
    
    # Aether configuratie
    config.aether = AetherConfig(
        model=os.getenv("AETHER_MODEL", "claude-3-sonnet-20240229"),
        temperature=float(os.getenv("AETHER_TEMPERATURE", "0.3")),
        max_tokens=int(os.getenv("AETHER_MAX_TOKENS", "1500")),
    )
    
    # Valideer API keys
    if not config.openai_api_key and config.solan.model.startswith("gpt"):
        logger.warning("OpenAI API key niet gevonden - Solan zal niet werken")
    
    if not config.anthropic_api_key and config.aether.model.startswith("claude"):
        logger.warning("Anthropic API key niet gevonden - Aether zal niet werken")
    
    logger.info(f"Configuratie geladen voor {config.environment} omgeving")
    return config


def setup_logging(config: SystemConfig) -> None:
    """Setup logging configuratie"""
    
    # Verwijder default logger
    logger.remove()
    
    # Console logging
    logger.add(
        sink=lambda msg: print(msg, end=""),
        level=config.log_level,
        format="<green>{time:YYYY-MM-DD HH:mm:ss}</green> | <level>{level: <8}</level> | <cyan>{name}</cyan>:<cyan>{function}</cyan>:<cyan>{line}</cyan> - <level>{message}</level>",
        colorize=True
    )
    
    # File logging
    if config.log_file:
        os.makedirs(os.path.dirname(config.log_file), exist_ok=True)
        logger.add(
            config.log_file,
            level=config.log_level,
            format="{time:YYYY-MM-DD HH:mm:ss} | {level: <8} | {name}:{function}:{line} - {message}",
            rotation="1 day",
            retention="30 days"
        )
    
    logger.info("Logging geconfigureerd")


# Global config instance
_config: Optional[SystemConfig] = None


def get_config() -> SystemConfig:
    """Krijg de globale configuratie instance"""
    global _config
    if _config is None:
        _config = load_config()
        setup_logging(_config)
    return _config
