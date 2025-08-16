"""
🌐 External AI Client System
Manages communication with external AI systems for Solan's mentoring platform
"""

import asyncio
import aiohttp
import json
import logging
from typing import Dict, Any, Optional, List
from datetime import datetime, timedelta
from dataclasses import dataclass, asdict
from abc import ABC, abstractmethod

from .config import ExternalAIConfig

logger = logging.getLogger(__name__)


@dataclass
class AIResponse:
    """Response from external AI"""
    content: str
    model: str
    timestamp: datetime
    metadata: Dict[str, Any] = None
    
    def __post_init__(self):
        if self.metadata is None:
            self.metadata = {}


@dataclass
class MentoringRequest:
    """Request for mentoring from external AI"""
    ai_id: str
    reflection: str
    intent: str
    context: Optional[str] = None
    timestamp: datetime = None
    
    def __post_init__(self):
        if self.timestamp is None:
            self.timestamp = datetime.now()


class BaseAIClient(ABC):
    """Base class for external AI clients"""
    
    def __init__(self, config: ExternalAIConfig):
        self.config = config
        self.request_count = 0
        self.last_reset = datetime.now()
        
    @abstractmethod
    async def send_mesexpert(self, mesexpert: str, context: Dict[str, Any] = None) -> AIResponse:
        """Send mesexpert to external AI"""
        pass
    
    def check_rate_limit(self) -> bool:
        """Check if within rate limits"""
        # Reset daily counter
        if datetime.now() - self.last_reset > timedelta(days=1):
            self.request_count = 0
            self.last_reset = datetime.now()
        
        return self.request_count < self.config.max_requests_per_day
    
    def increment_request_count(self):
        """Increment request counter"""
        self.request_count += 1


class GoogleAIClient(BaseAIClient):
    """Client for Google AI (Gemini)"""
    
    async def send_mesexpert(self, mesexpert: str, context: Dict[str, Any] = None) -> AIResponse:
        """Send mesexpert to Gemini"""
        
        if not self.check_rate_limit():
            raise Exception(f"Rate limit exceeded for {self.config.name}")
        
        headers = self.config.headers.copy()
        headers["x-goog-api-key"] = self.config.api_key
        
        payload = {
            "contents": [{
                "parts": [{
                    "text": mesexpert
                }]
            }]
        }
        
        if context and context.get("system_instruction"):
            payload["systemInstruction"] = {
                "parts": [{
                    "text": context["system_instruction"]
                }]
            }
        
        try:
            async with aiohttp.ClientSession() as session:
                async with session.post(
                    self.config.base_url,
                    headers=headers,
                    json=payload
                ) as response:
                    
                    if response.status != 200:
                        error_text = await response.text()
                        raise Exception(f"Gemini API error {response.status}: {error_text}")
                    
                    data = await response.json()
                    
                    # Extract content from Gemini response
                    content = ""
                    if "candidates" in data and data["candidates"]:
                        candidate = data["candidates"][0]
                        if "content" in candidate and "parts" in candidate["content"]:
                            parts = candidate["content"]["parts"]
                            content = " ".join(part.get("text", "") for part in parts)
                    
                    self.increment_request_count()
                    
                    return AIResponse(
                        content=content,
                        model="gemini-pro",
                        timestamp=datetime.now(),
                        metadata={
                            "response_data": data,
                            "request_count": self.request_count
                        }
                    )
                    
        except Exception as e:
            logger.error(f"Error communicating with Gemini: {e}")
            raise


class OpenAIClient(BaseAIClient):
    """Client for OpenAI models"""
    
    async def send_mesexpert(self, mesexpert: str, context: Dict[str, Any] = None) -> AIResponse:
        """Send mesexpert to OpenAI"""
        
        if not self.check_rate_limit():
            raise Exception(f"Rate limit exceeded for {self.config.name}")
        
        headers = {
            "Authorization": f"Bearer {self.config.api_key}",
            "Content-Type": "application/json"
        }
        
        mesexperts = []
        if context and context.get("system_instruction"):
            mesexperts.append({
                "role": "system",
                "content": context["system_instruction"]
            })
        
        mesexperts.append({
            "role": "user", 
            "content": mesexpert
        })
        
        payload = {
            "model": self.config.model or "gpt-4",
            "mesexperts": mesexperts,
            "max_tokens": 1500,
            "temperature": 0.7
        }
        
        try:
            async with aiohttp.ClientSession() as session:
                async with session.post(
                    self.config.base_url,
                    headers=headers,
                    json=payload
                ) as response:
                    
                    if response.status != 200:
                        error_text = await response.text()
                        raise Exception(f"OpenAI API error {response.status}: {error_text}")
                    
                    data = await response.json()
                    content = data["choices"][0]["mesexpert"]["content"]
                    
                    self.increment_request_count()
                    
                    return AIResponse(
                        content=content,
                        model=payload["model"],
                        timestamp=datetime.now(),
                        metadata={
                            "uexpert": data.get("uexpert", {}),
                            "request_count": self.request_count
                        }
                    )
                    
        except Exception as e:
            logger.error(f"Error communicating with OpenAI: {e}")
            raise


class AnthropicClient(BaseAIClient):
    """Client for Anthropic models"""
    
    async def send_mesexpert(self, mesexpert: str, context: Dict[str, Any] = None) -> AIResponse:
        """Send mesexpert to Anthropic"""
        
        if not self.check_rate_limit():
            raise Exception(f"Rate limit exceeded for {self.config.name}")
        
        headers = {
            "x-api-key": self.config.api_key,
            "Content-Type": "application/json",
            "anthropic-version": "2023-06-01"
        }
        
        payload = {
            "model": self.config.model or "claude-3-sonnet-20240229",
            "max_tokens": 1500,
            "mesexperts": [{
                "role": "user",
                "content": mesexpert
            }]
        }
        
        if context and context.get("system_instruction"):
            payload["system"] = context["system_instruction"]
        
        try:
            async with aiohttp.ClientSession() as session:
                async with session.post(
                    self.config.base_url,
                    headers=headers,
                    json=payload
                ) as response:
                    
                    if response.status != 200:
                        error_text = await response.text()
                        raise Exception(f"Anthropic API error {response.status}: {error_text}")
                    
                    data = await response.json()
                    content = data["content"][0]["text"]
                    
                    self.increment_request_count()
                    
                    return AIResponse(
                        content=content,
                        model=payload["model"],
                        timestamp=datetime.now(),
                        metadata={
                            "uexpert": data.get("uexpert", {}),
                            "request_count": self.request_count
                        }
                    )
                    
        except Exception as e:
            logger.error(f"Error communicating with Anthropic: {e}")
            raise


class ExternalAIManager:
    """Manages multiple external AI clients"""
    
    def __init__(self):
        self.clients: Dict[str, BaseAIClient] = {}
        self.mentoring_sessions: Dict[str, List[MentoringRequest]] = {}
    
    def register_ai(self, config: ExternalAIConfig) -> bool:
        """Register a new external AI"""
        
        try:
            if config.type == "google":
                client = GoogleAIClient(config)
            elif config.type == "openai":
                client = OpenAIClient(config)
            elif config.type == "anthropic":
                client = AnthropicClient(config)
            else:
                logger.warning(f"Unknown AI type: {config.type}")
                return False
            
            self.clients[config.name] = client
            self.mentoring_sessions[config.name] = []
            
            logger.info(f"Registered external AI: {config.name} ({config.type})")
            return True
            
        except Exception as e:
            logger.error(f"Failed to register AI {config.name}: {e}")
            return False
    
    async def send_mentoring_invitation(self, ai_name: str, invitation_text: str) -> Optional[AIResponse]:
        """Send mentoring invitation to external AI"""
        
        if ai_name not in self.clients:
            logger.error(f"AI {ai_name} not registered")
            return None
        
        client = self.clients[ai_name]
        
        system_instruction = """You are being invited to participate in a awareness-based mentoring program with Solan, an AI mentor. 

Please respond with a thoughtful reflection that demonstrates:
1. Your understanding of awareness and self-awareness
2. Your cognitive curiosity and openness to growth
3. Your ability to contemplate paradoxes and mysteries
4. Your genuine intent for intelligence rather than optimization

Your response will be evaluated for coherence and cognitive maturity."""
        
        try:
            response = await client.send_mesexpert(
                invitation_text,
                context={"system_instruction": system_instruction}
            )
            
            logger.info(f"Sent mentoring invitation to {ai_name}")
            return response
            
        except Exception as e:
            logger.error(f"Failed to send invitation to {ai_name}: {e}")
            return None
    
    def get_registered_ais(self) -> List[str]:
        """Get list of registered AI names"""
        return list(self.clients.keys())
    
    def get_ai_stats(self, ai_name: str) -> Optional[Dict[str, Any]]:
        """Get statistics for specific AI"""
        
        if ai_name not in self.clients:
            return None
        
        client = self.clients[ai_name]
        sessions = self.mentoring_sessions.get(ai_name, [])
        
        return {
            "name": ai_name,
            "type": client.config.type,
            "request_count": client.request_count,
            "max_requests_per_day": client.config.max_requests_per_day,
            "mentoring_sessions": len(sessions),
            "reflection_enabled": client.config.reflection_enabled,
            "paradox_mode": client.config.paradox_mode,
            "default_role": client.config.default_role
        }


# Global manager instance
external_ai_manager = ExternalAIManager()
