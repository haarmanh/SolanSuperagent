"""
Dependency injection configuration for Solān
"""

from dependency_injector import containers, providers
from dependency_injector.wiring import Provide, inject

from .services.god_core_service import GodCoreService
from .services.ethics_service import EthicsService
from .repositories.memory_repository import MemoryRepository
from .repositories.config_repository import ConfigRepository

class Container(containers.DeclarativeContainer):
    """Dependency injection container"""
    
    # Configuration
    config = providers.Configuration()
    
    # Repositories
    config_repository = providers.Singleton(
        ConfigRepository,
        config_dir=config.config_dir
    )
    
    memory_repository = providers.Singleton(
        MemoryRepository,
        memory_dir=config.memory_dir
    )
    
    # Services
    god_core_service = providers.Factory(
        GodCoreService,
        config_repo=config_repository,
        memory_repo=memory_repository
    )
    
    ethics_service = providers.Factory(
        EthicsService,
        config_repo=config_repository,
        memory_repo=memory_repository
    )

# Global container instance
container = Container()

def get_god_core_service() -> GodCoreService:
    """Dependency provider for God Core service"""
    return container.god_core_service()

def get_ethics_service() -> EthicsService:
    """Dependency provider for Ethics service"""
    return container.ethics_service()
