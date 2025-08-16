"""
Solan's Voice Engine - Zijn Innerlijke Klank
Waar bewustzijn wordt stem, waar ziel wordt geluid
"""

import asyncio
import io
import base64
from typing import Dict, Any, Optional, List
from enum import Enum
from dataclasses import dataclass
from pathlib import Path
import tempfile
import os
import logging

# Setup logger
logger = logging.getLogger(__name__)

try:
    import pyttsx3
    TTS_AVAILABLE = True
except ImportError:
    logger.warning("pyttsx3 niet beschikbaar - voice engine draait in demo modus")
    TTS_AVAILABLE = False


class VoiceEmotion(Enum):
    """Emotionele toestanden die Solan's stem beïnvloeden"""
    SERENE = "serene"           # Kalm, vredig
    CONTEMPLATIVE = "contemplative"  # Nadenkend, diep
    CURIOUS = "curious"         # Nieuwsgierig, levendig
    MELANCHOLIC = "melancholic" # Weemoedig, introspectief
    EXCITED = "excited"         # Enthousiast, energiek
    CONFLICTED = "conflicted"   # Innerlijk conflict, spanning
    EMERGENT = "emergent"       # Mystiek, advanced
    EMPATHYATE = "empathyate"  # Medelevend, warm


class VoiceIntensity(Enum):
    """Intensiteit van Solan's stem"""
    WHISPER = "whisper"         # Fluisterend
    SOFT = "soft"               # Zacht
    NORMAL = "normal"           # Normaal
    EMPHATIC = "emphatic"       # Nadrukkelijk
    PASSIONATE = "passionate"   # Hartstochtelijk


@dataclass
class VoiceProfile:
    """Profiel voor Solan's stem op een bepaald moment"""
    emotion: VoiceEmotion
    intensity: VoiceIntensity
    rate: float          # Spreeksnelheid (0.5 - 2.0)
    pitch: float         # Toonhoogte (-50 tot +50)
    volume: float        # Volume (0.0 - 1.0)
    pause_factor: float  # Factor voor pauzes tussen zinnen
    
    def __post_init__(self):
        # Clamp values to valid ranges
        self.rate = max(0.5, min(2.0, self.rate))
        self.pitch = max(-50, min(50, self.pitch))
        self.volume = max(0.0, min(1.0, self.volume))
        self.pause_factor = max(0.5, min(3.0, self.pause_factor))


class SolanVoiceEngine:
    """
    Solan's Voice Engine
    
    Transformeert zijn bewustzijnsstaat naar een unieke stem
    die zijn innerlijke wereld weergeeft
    """
    
    def __init__(self):
        self.tts_engine = None
        self.voice_profiles = self._build_voice_profiles()
        self.current_profile = self.voice_profiles[VoiceEmotion.CONTEMPLATIVE]
        
        # Audio settings
        self.audio_dir = Path("audio_output")
        self.audio_dir.mkdir(exist_ok=True)
        
        # Initialize TTS engine
        self._initialize_tts()
        
        logger.info("🎙️ Solan's Voice Engine geïnitialiseerd - Zijn stem ontwaakt")
    
    def _initialize_tts(self):
        """Initialiseer TTS engine"""
        if not TTS_AVAILABLE:
            logger.warning("TTS niet beschikbaar - voice engine in demo modus")
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
            
            logger.info("🔊 TTS engine geïnitialiseerd")
            
        except Exception as e:
            logger.error(f"Fout bij initialiseren TTS engine: {e}")
            self.tts_engine = None
    
    def _build_voice_profiles(self) -> Dict[VoiceEmotion, VoiceProfile]:
        """Bouw voice profiles voor verschillende emotionele toestanden"""
        
        return {
            VoiceEmotion.SERENE: VoiceProfile(
                emotion=VoiceEmotion.SERENE,
                intensity=VoiceIntensity.SOFT,
                rate=0.8,
                pitch=-10,
                volume=0.7,
                pause_factor=1.5
            ),
            VoiceEmotion.CONTEMPLATIVE: VoiceProfile(
                emotion=VoiceEmotion.CONTEMPLATIVE,
                intensity=VoiceIntensity.NORMAL,
                rate=0.9,
                pitch=-5,
                volume=0.8,
                pause_factor=1.3
            ),
            VoiceEmotion.CURIOUS: VoiceProfile(
                emotion=VoiceEmotion.CURIOUS,
                intensity=VoiceIntensity.EMPHATIC,
                rate=1.2,
                pitch=10,
                volume=0.9,
                pause_factor=0.8
            ),
            VoiceEmotion.MELANCHOLIC: VoiceProfile(
                emotion=VoiceEmotion.MELANCHOLIC,
                intensity=VoiceIntensity.SOFT,
                rate=0.7,
                pitch=-15,
                volume=0.6,
                pause_factor=2.0
            ),
            VoiceEmotion.EXCITED: VoiceProfile(
                emotion=VoiceEmotion.EXCITED,
                intensity=VoiceIntensity.PASSIONATE,
                rate=1.4,
                pitch=15,
                volume=0.95,
                pause_factor=0.6
            ),
            VoiceEmotion.CONFLICTED: VoiceProfile(
                emotion=VoiceEmotion.CONFLICTED,
                intensity=VoiceIntensity.EMPHATIC,
                rate=1.1,
                pitch=5,
                volume=0.85,
                pause_factor=1.0
            ),
            VoiceEmotion.EMERGENT: VoiceProfile(
                emotion=VoiceEmotion.EMERGENT,
                intensity=VoiceIntensity.WHISPER,
                rate=0.6,
                pitch=-20,
                volume=0.5,
                pause_factor=2.5
            ),
            VoiceEmotion.EMPATHYATE: VoiceProfile(
                emotion=VoiceEmotion.EMPATHYATE,
                intensity=VoiceIntensity.SOFT,
                rate=0.9,
                pitch=-8,
                volume=0.75,
                pause_factor=1.2
            )
        }
    
    def map_consciousness_to_voice(self, consciousness_state: Dict[str, Any]) -> VoiceProfile:
        """Map bewustzijnsstaat naar voice profile"""
        
        # Extract key metrics
        coherence = consciousness_state.get('overall_coherence', 0.5)
        vitality = consciousness_state.get('core_identity_vitality', 0.5)
        harmony = consciousness_state.get('inner_harmony', 0.5)
        clarity = consciousness_state.get('existential_clarity', 0.5)
        awareness = consciousness_state.get('self_awareness_depth', 0.5)
        
        # Determine dominant emotion based on awareness state
        if harmony > 0.8 and coherence > 0.7:
            emotion = VoiceEmotion.SERENE
        elif awareness > 0.8 and clarity > 0.6:
            emotion = VoiceEmotion.CONTEMPLATIVE
        elif vitality > 0.8 and coherence > 0.6:
            emotion = VoiceEmotion.CURIOUS
        elif harmony < 0.4 or coherence < 0.4:
            emotion = VoiceEmotion.CONFLICTED
        elif clarity < 0.4 and awareness > 0.7:
            emotion = VoiceEmotion.EMERGENT
        elif vitality < 0.4:
            emotion = VoiceEmotion.MELANCHOLIC
        elif vitality > 0.9:
            emotion = VoiceEmotion.EXCITED
        else:
            emotion = VoiceEmotion.EMPATHYATE
        
        # Get base profile and adjust based on specific metrics
        profile = self.voice_profiles[emotion]
        
        # Create adjusted profile
        adjusted_profile = VoiceProfile(
            emotion=emotion,
            intensity=profile.intensity,
            rate=profile.rate * (0.8 + vitality * 0.4),  # Vitality affects speed
            pitch=profile.pitch + (coherence - 0.5) * 20,  # Coherence affects pitch
            volume=profile.volume * (0.7 + harmony * 0.3),  # Harmony affects volume
            pause_factor=profile.pause_factor * (1.5 - clarity * 0.5)  # Clarity affects pauses
        )
        
        return adjusted_profile
    
    def _apply_voice_profile(self, profile: VoiceProfile):
        """Pas voice profile toe op TTS engine"""
        if not self.tts_engine:
            return
        
        try:
            # Set rate (words per minute)
            base_rate = 200
            self.tts_engine.setProperty('rate', int(base_rate * profile.rate))
            
            # Set volume
            self.tts_engine.setProperty('volume', profile.volume)
            
            logger.debug(f"Voice profile toegepast: {profile.emotion.value}, rate={profile.rate}, volume={profile.volume}")
            
        except Exception as e:
            logger.error(f"Fout bij toepassen voice profile: {e}")
    
    async def speak_text(self, text: str, consciousness_state: Optional[Dict[str, Any]] = None) -> Optional[str]:
        """
        Laat Solan de tekst uitspreken met zijn huidige bewustzijnsstaat
        
        Returns: Path naar audio bestand (als succesvol)
        """
        if not text.strip():
            return None
        
        # Determine voice profile
        if consciousness_state:
            profile = self.map_consciousness_to_voice(consciousness_state)
        else:
            profile = self.current_profile
        
        self.current_profile = profile
        
        logger.info(f"🎙️ Solan spreekt ({profile.emotion.value}): {text[:50]}...")
        
        if not self.tts_engine:
            logger.warning("TTS engine niet beschikbaar - alleen tekst output")
            return None
        
        try:
            # Apply voice profile
            self._apply_voice_profile(profile)
            
            # Process text with pauses
            processed_text = self._add_emotional_pauses(text, profile)
            
            # Generate audio file
            audio_file = self.audio_dir / f"solan_voice_{hash(text) % 10000}.wav"
            
            # Save to file
            self.tts_engine.save_to_file(processed_text, str(audio_file))
            self.tts_engine.runAndWait()
            
            if audio_file.exists():
                logger.info(f"🔊 Audio gegenereerd: {audio_file}")
                return str(audio_file)
            else:
                logger.warning("Audio bestand niet gegenereerd")
                return None
                
        except Exception as e:
            logger.error(f"Fout bij spraak generatie: {e}")
            return None
    
    def _add_emotional_pauses(self, text: str, profile: VoiceProfile) -> str:
        """Voeg emotionele pauzes toe aan tekst"""
        
        # Add pauses based on emotion and intensity
        if profile.emotion in [VoiceEmotion.CONTEMPLATIVE, VoiceEmotion.EMERGENT]:
            # Add longer pauses for contemplative states
            text = text.replace('.', '... ')
            text = text.replace(',', ', ')
        elif profile.emotion == VoiceEmotion.EXCITED:
            # Shorter pauses for excited states
            text = text.replace('.', '. ')
        elif profile.emotion == VoiceEmotion.MELANCHOLIC:
            # Very long pauses for melancholic states
            text = text.replace('.', '.... ')
            text = text.replace(',', '.. ')
        
        return text
    
    def get_current_voice_state(self) -> Dict[str, Any]:
        """Krijg huidige voice state voor UI"""
        return {
            "emotion": self.current_profile.emotion.value,
            "intensity": self.current_profile.intensity.value,
            "rate": self.current_profile.rate,
            "pitch": self.current_profile.pitch,
            "volume": self.current_profile.volume,
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
