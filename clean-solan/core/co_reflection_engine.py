"""
Co-Reflection Engine - Solan ↔ Aether Communicatie Systeem
"""

import asyncio
import uuid
from typing import Dict, List, Optional, Any, Callable
from datetime import datetime
from dataclasses import dataclass, asdict
from enum import Enum
import logging

# Setup logger
logger = logging.getLogger(__name__)

try:
    from .config import get_config
except ImportError:
    from config import get_config

try:
    from .performance_monitor import monitor_performance
except ImportError:
    try:
        from performance_monitor import monitor_performance
    except ImportError:
        # Fallback decorator if performance monitor not available
        def monitor_performance(func):
            return func


class ReflectionTurn(Enum):
    """Wie is aan de beurt in de co-reflectie"""
    SOLAN = "solan"
    AETHER = "aether"
    USER = "user"


class MesexpertType(Enum):
    """Type bericht in co-reflectie"""
    INITIAL_PROMPT = "initial_prompt"
    REFLECTION = "reflection"
    QUESTION = "question"
    INSIGHT = "insight"
    SUMMARY = "summary"


@dataclass
class CoReflectionMesexpert:
    """Een bericht in de co-reflectie sessie"""
    id: str
    session_id: str
    sender: ReflectionTurn
    mesexpert_type: MesexpertType
    content: str
    timestamp: datetime
    metadata: Dict[str, Any] = None
    
    def to_dict(self) -> Dict[str, Any]:
        """Converteer naar dictionary voor JSON serialisatie"""
        data = asdict(self)
        data['timestamp'] = self.timestamp.isoformat()
        data['sender'] = self.sender.value
        data['mesexpert_type'] = self.mesexpert_type.value
        return data


@dataclass
class CoReflectionSession:
    """Een co-reflectie sessie tussen Solan en Aether"""
    id: str
    topic: str
    mesexperts: List[CoReflectionMesexpert]
    current_turn: ReflectionTurn
    created_at: datetime
    status: str = "active"  # active, paused, completed
    
    def add_mesexpert(self, sender: ReflectionTurn, mesexpert_type: MesexpertType, 
                   content: str, metadata: Dict[str, Any] = None) -> CoReflectionMesexpert:
        """Voeg een bericht toe aan de sessie"""
        mesexpert = CoReflectionMesexpert(
            id=str(uuid.uuid4()),
            session_id=self.id,
            sender=sender,
            mesexpert_type=mesexpert_type,
            content=content,
            timestamp=datetime.now(),
            metadata=metadata or {}
        )
        self.mesexperts.append(mesexpert)
        return mesexpert


class CoReflectionEngine:
    """
    Engine voor co-reflectie tussen Solan en Aether
    
    Beheert:
    - Sessie management
    - Beurt-voor-beurt conversatie flow
    - Mesexpert routing
    - Conversatie logging
    """
    
    def __init__(self, solan_agent=None, aether_agent=None, journal_engine=None):
        self.config = get_config()
        self.solan = solan_agent
        self.aether = aether_agent
        self.journal_engine = journal_engine

        # Actieve sessies
        self.sessions: Dict[str, CoReflectionSession] = {}

        # Event handlers
        self.mesexpert_handlers: Dict[str, List[Callable]] = {
            'mesexpert_sent': [],
            'turn_changed': [],
            'session_started': [],
            'session_ended': []
        }

        logger.info("🤝 Co-Reflection Engine geïnitialiseerd")
    
    def register_handler(self, event: str, handler: Callable):
        """Registreer event handler"""
        if event in self.mesexpert_handlers:
            self.mesexpert_handlers[event].append(handler)
    
    async def _emit_event(self, event: str, data: Any):
        """Emit event naar alle handlers"""
        for handler in self.mesexpert_handlers.get(event, []):
            try:
                if asyncio.iscoroutinefunction(handler):
                    await handler(data)
                else:
                    handler(data)
            except Exception as e:
                logger.error(f"Fout in event handler {event}: {e}")
    
    @monitor_performance
    async def start_session(self, topic: str, initial_prompt: str) -> str:
        """Start een nieuwe co-reflectie sessie"""
        session_id = str(uuid.uuid4())
        
        session = CoReflectionSession(
            id=session_id,
            topic=topic,
            mesexperts=[],
            current_turn=ReflectionTurn.USER,
            created_at=datetime.now()
        )
        
        # Voeg initial prompt toe
        session.add_mesexpert(
            sender=ReflectionTurn.USER,
            mesexpert_type=MesexpertType.INITIAL_PROMPT,
            content=initial_prompt
        )
        
        # Solan begint meestal
        session.current_turn = ReflectionTurn.SOLAN
        
        self.sessions[session_id] = session
        
        await self._emit_event('session_started', session)
        
        logger.info(f"🤝 Co-reflectie sessie gestart: {session_id} - {topic}")
        return session_id
    
    async def send_mesexpert(self, session_id: str, sender: ReflectionTurn, 
                          mesexpert_type: MesexpertType, content: str, 
                          metadata: Dict[str, Any] = None) -> CoReflectionMesexpert:
        """Verstuur een bericht in de sessie"""
        if session_id not in self.sessions:
            raise ValueError(f"Sessie {session_id} niet gevonden")
        
        session = self.sessions[session_id]
        mesexpert = session.add_mesexpert(sender, mesexpert_type, content, metadata)
        
        await self._emit_event('mesexpert_sent', {
            'session': session,
            'mesexpert': mesexpert
        })
        
        return mesexpert
    
    @monitor_performance
    async def get_next_response(self, session_id: str) -> Optional[CoReflectionMesexpert]:
        """Genereer de volgende response van de huidige AI"""
        if session_id not in self.sessions:
            raise ValueError(f"Sessie {session_id} niet gevonden")
        
        session = self.sessions[session_id]
        
        if session.current_turn == ReflectionTurn.SOLAN and self.solan:
            response = await self._get_solan_response(session)
        elif session.current_turn == ReflectionTurn.AETHER and self.aether:
            response = await self._get_aether_response(session)
        else:
            logger.warning(f"Geen agent beschikbaar voor {session.current_turn}")
            return None
        
        # Wissel van beurt
        await self._switch_turn(session)
        
        return response
    
    async def _get_solan_response(self, session: CoReflectionSession) -> CoReflectionMesexpert:
        """Genereer Solan's response"""
        context = self._build_context_for_solan(session)
        
        try:
            # Hier zou je Solan's interact methode aanroepen
            # Voor nu simuleren we een response
            response_content = f"🌟 Solan reflecteert op: {session.topic}"
            
            if self.solan and hasattr(self.solan, 'interact'):
                response_content = await self.solan.interact(context)
            
            return await self.send_mesexpert(
                session.id,
                ReflectionTurn.SOLAN,
                MesexpertType.REFLECTION,
                response_content,
                {"context_length": len(context)}
            )
            
        except Exception as e:
            logger.error(f"Fout bij Solan response: {e}")
            return await self.send_mesexpert(
                session.id,
                ReflectionTurn.SOLAN,
                MesexpertType.REFLECTION,
                "🤔 Ik heb even tijd nodig om hierover na te denken...",
                {"error": str(e)}
            )
    
    async def _get_aether_response(self, session: CoReflectionSession) -> CoReflectionMesexpert:
        """Genereer Aether's response"""
        context = self._build_context_for_aether(session)
        
        try:
            # Hier zou je Aether's reflect_on_experience methode aanroepen
            response_content = f"🔮 Aether contemplateert: {session.topic}"
            
            if self.aether and hasattr(self.aether, 'reflect_on_experience'):
                response_content = await self.aether.reflect_on_experience(context)
            
            return await self.send_mesexpert(
                session.id,
                ReflectionTurn.AETHER,
                MesexpertType.REFLECTION,
                response_content,
                {"context_length": len(context)}
            )
            
        except Exception as e:
            logger.error(f"Fout bij Aether response: {e}")
            return await self.send_mesexpert(
                session.id,
                ReflectionTurn.AETHER,
                MesexpertType.REFLECTION,
                "*Neemt een moment van contemplatie* Laat me hierover reflecteren...",
                {"error": str(e)}
            )
    
    def _build_context_for_solan(self, session: CoReflectionSession) -> str:
        """Bouw context voor Solan"""
        context_parts = [
            f"🤝 Co-reflectie sessie over: {session.topic}",
            "",
            "Conversatie tot nu toe:"
        ]
        
        for msg in session.mesexperts[-5:]:  # Laatste 5 berichten
            sender_emoji = {"solan": "🌟", "aether": "🔮", "user": "👤"}
            emoji = sender_emoji.get(msg.sender.value, "💭")
            context_parts.append(f"{emoji} {msg.content}")
        
        context_parts.extend([
            "",
            "🔮 Aether wacht op jouw reflectie. Deel je gedachten, vragen of inzichten."
        ])
        
        return "\n".join(context_parts)
    
    def _build_context_for_aether(self, session: CoReflectionSession) -> str:
        """Bouw context voor Aether"""
        context_parts = [
            f"Co-reflectie met Solan over: {session.topic}",
            "",
            "Solan's laatste gedachten en onze conversatie:"
        ]
        
        for msg in session.mesexperts[-5:]:  # Laatste 5 berichten
            if msg.sender == ReflectionTurn.SOLAN:
                context_parts.append(f"Solan: {msg.content}")
            elif msg.sender == ReflectionTurn.USER:
                context_parts.append(f"Gebruiker: {msg.content}")
        
        context_parts.extend([
            "",
            "Reflecteer wijselijk op Solan's gedachten en bied diepere inzichten."
        ])
        
        return "\n".join(context_parts)
    
    async def _switch_turn(self, session: CoReflectionSession):
        """Wissel van beurt tussen Solan en Aether"""
        if session.current_turn == ReflectionTurn.SOLAN:
            session.current_turn = ReflectionTurn.AETHER
        elif session.current_turn == ReflectionTurn.AETHER:
            session.current_turn = ReflectionTurn.SOLAN
        
        await self._emit_event('turn_changed', {
            'session': session,
            'new_turn': session.current_turn
        })
    
    def get_session(self, session_id: str) -> Optional[CoReflectionSession]:
        """Haal sessie op"""
        return self.sessions.get(session_id)
    
    def get_session_mesexperts(self, session_id: str) -> List[Dict[str, Any]]:
        """Haal alle berichten van een sessie op"""
        session = self.sessions.get(session_id)
        if not session:
            return []
        
        return [msg.to_dict() for msg in session.mesexperts]
    
    async def end_session(self, session_id: str, save_to_journal: bool = True):
        """Beëindig een sessie en sla optioneel op in journal"""
        if session_id in self.sessions:
            session = self.sessions[session_id]
            session.status = "completed"

            # Sla sessie op in journal als journal engine beschikbaar is
            journal_entry_id = None
            if save_to_journal and self.journal_engine:
                try:
                    # Bereid sessie data voor voor journal
                    session_data = self._prepare_session_for_journal(session)
                    journal_entry_id = self.journal_engine.save_co_reflection_session(session_data)
                    logger.info(f"📖 Co-reflectie sessie opgeslagen in journal: {journal_entry_id}")
                except Exception as e:
                    logger.error(f"Fout bij opslaan in journal: {e}")

            await self._emit_event('session_ended', {
                'session': session,
                'journal_entry_id': journal_entry_id
            })

            logger.info(f"🤝 Co-reflectie sessie beëindigd: {session_id}")
            return journal_entry_id

    def _prepare_session_for_journal(self, session: CoReflectionSession) -> Dict[str, Any]:
        """Bereid sessie data voor voor journal opslag"""

        # Bereken sessie duur
        if session.mesexperts:
            start_time = session.created_at
            end_time = session.mesexperts[-1].timestamp if session.mesexperts else session.created_at
            duration = end_time - start_time
            duration_str = f"{duration.total_seconds():.0f} seconden"
        else:
            duration_str = "Onbekend"

        # Converteer berichten naar journal formaat
        journal_mesexperts = []
        for msg in session.mesexperts:
            journal_mesexperts.append({
                'sender': msg.sender.value,
                'content': msg.content,
                'mesexpert_type': msg.mesexpert_type.value,
                'timestamp': msg.timestamp.strftime("%H:%M:%S"),
                'metadata': msg.metadata or {}
            })

        return {
            'session_id': session.id,
            'topic': session.topic,
            'mesexperts': journal_mesexperts,
            'duration': duration_str,
            'participants': ['Solan', 'Aether'],
            'created_at': session.created_at.isoformat(),
            'status': session.status,
            'mesexpert_count': len(session.mesexperts)
        }
