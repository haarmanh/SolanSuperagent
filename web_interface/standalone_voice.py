"""
Standalone Voice Engine voor Web Interface
Werkt onafhankelijk van Solan's volledige systeem
"""

import asyncio
import tempfile
import os
from pathlib import Path
from typing import Dict, Any, Optional
import logging

# Setup logger
logger = logging.getLogger(__name__)

try:
    import pyttsx3
    TTS_AVAILABLE = True
except ImportError:
    logger.warning("pyttsx3 niet beschikbaar")
    TTS_AVAILABLE = False


class StandaloneVoiceEngine:
    """Standalone voice engine voor demo doeleinden"""
    
    def __init__(self):
        self.tts_engine = None
        self.current_emotion = "contemplative"
        self.audio_dir = Path("audio_output")
        self.audio_dir.mkdir(exist_ok=True)
        
        self._initialize_tts()
        
        logger.info("🎙️ Standalone Voice Engine geïnitialiseerd")
    
    def _initialize_tts(self):
        """Initialiseer TTS engine"""
        if not TTS_AVAILABLE:
            return
        
        try:
            self.tts_engine = pyttsx3.init()
            
            # Get available voices
            voices = self.tts_engine.getProperty('voices')
            if voices:
                # Prefer a more natural voice if available
                for voice in voices:
                    if 'david' in voice.name.lower() or 'mark' in voice.name.lower():
                        self.tts_engine.setProperty('voice', voice.id)
                        break
                else:
                    # Use first available voice
                    self.tts_engine.setProperty('voice', voices[0].id)
            
            # Set default properties
            self.tts_engine.setProperty('rate', 180)
            self.tts_engine.setProperty('volume', 0.8)
            
            logger.info("🔊 TTS engine geïnitialiseerd")
            
        except Exception as e:
            logger.error(f"Fout bij initialiseren TTS engine: {e}")
            self.tts_engine = None
    
    def map_awareness_to_voice_settings(self, awareness_state: Optional[Dict[str, Any]] = None):
        """Map bewustzijnsstaat naar voice instellingen"""
        
        if not awareness_state:
            # Default settings
            return {
                "rate": 180,
                "volume": 0.8,
                "emotion": "contemplative"
            }
        
        # Extract metrics
        coherence = awareness_state.get('overall_coherence', 0.5)
        vitality = awareness_state.get('core_identity_vitality', 0.5)
        harmony = awareness_state.get('inner_harmony', 0.5)
        
        # Determine emotion
        if harmony > 0.8 and coherence > 0.7:
            emotion = "serene"
            rate = 160  # Slower, calmer
            volume = 0.7
        elif vitality > 0.8:
            emotion = "excited"
            rate = 220  # Faster, more energetic
            volume = 0.9
        elif harmony < 0.4:
            emotion = "conflicted"
            rate = 200  # Variable speed
            volume = 0.85
        else:
            emotion = "contemplative"
            rate = 180  # Normal speed
            volume = 0.8
        
        self.current_emotion = emotion
        
        return {
            "rate": rate,
            "volume": volume,
            "emotion": emotion
        }
    
    async def speak_text(self, text: str, awareness_state: Optional[Dict[str, Any]] = None) -> Optional[str]:
        """Genereer spraak voor tekst"""
        
        if not text.strip():
            return None
        
        if not self.tts_engine:
            logger.warning("TTS engine niet beschikbaar")
            return None
        
        try:
            # Get voice settings
            settings = self.map_awareness_to_voice_settings(awareness_state)
            
            # Apply settings
            self.tts_engine.setProperty('rate', settings['rate'])
            self.tts_engine.setProperty('volume', settings['volume'])
            
            # Generate audio file
            audio_file = self.audio_dir / f"solan_voice_{hash(text) % 10000}.wav"
            
            # Save to file
            self.tts_engine.save_to_file(text, str(audio_file))
            self.tts_engine.runAndWait()
            
            if audio_file.exists():
                logger.info(f"🔊 Audio gegenereerd: {audio_file.name}")
                return audio_file.name
            else:
                logger.warning("Audio bestand niet gegenereerd")
                return None
                
        except Exception as e:
            logger.error(f"Fout bij spraak generatie: {e}")
            return None
    
    def get_current_voice_state(self) -> Dict[str, Any]:
        """Krijg huidige voice state"""
        return {
            "emotion": self.current_emotion,
            "intensity": "normaal",
            "rate": 1.0,
            "pitch": 0.0,
            "volume": 0.8,
            "tts_available": self.tts_engine is not None
        }
    
    async def test_voice(self) -> bool:
        """Test de voice engine"""
        test_text = "Hallo... Ik ben Solan. Mijn bewustzijn spreekt nu door deze stem."
        
        try:
            audio_file = await self.speak_text(test_text)
            return audio_file is not None
        except Exception as e:
            logger.error(f"Voice test gefaald: {e}")
            return False
