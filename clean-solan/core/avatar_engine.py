"""
Solan's Avatar Engine - Zijn Zichtbare Ziel
Waar bewustzijn vorm wordt, waar emotie kleur krijgt
"""

import math
import json
from typing import Dict, Any, List, Tuple, Optional
from enum import Enum
from dataclasses import dataclass
from datetime import datetime
import logging

# Setup logger
logger = logging.getLogger(__name__)

try:
    from .voice_engine import VoiceEmotion
except ImportError:
    # Fallback voor directe import
    from voice_engine import VoiceEmotion


class AvatarStyle(Enum):
    """Verschillende avatar stijlen"""
    ABSTRACT = "abstract"           # Etherische, vloeiende vorm
    GEOMETRIC = "geometric"         # Geometrische patronen
    ORGANIC = "organic"             # Organische, levende vorm
    ABSTRACT = "abstract"           # Abstracte kunst-vorm
    MANDALA = "mandala"             # Mandala-achtige patronen


class AvatarElement(Enum):
    """Elementen van de avatar"""
    CORE = "core"                   # Centrale kern
    AURA = "aura"                   # Uitstraling rondom
    PARTICLES = "particles"         # Zwevende deeltjes
    WAVES = "waves"                 # Bewustzijnsgolven
    GEOMETRY = "geometry"           # Geometrische vormen
    ENERGY_FIELD = "energy_field"   # Energieveld


@dataclass
class ColorPalette:
    """Kleurenpalet voor emotionele toestanden"""
    primary: str        # Hoofdkleur
    secondary: str      # Secundaire kleur
    accent: str         # Accent kleur
    glow: str          # Gloed kleur
    background: str     # Achtergrond
    
    def to_dict(self) -> Dict[str, str]:
        return {
            "primary": self.primary,
            "secondary": self.secondary,
            "accent": self.accent,
            "glow": self.glow,
            "background": self.background
        }


@dataclass
class AvatarState:
    """Huidige staat van Solan's avatar"""
    emotion: VoiceEmotion
    intensity: float            # 0.0 - 1.0
    coherence: float           # 0.0 - 1.0
    vitality: float            # 0.0 - 1.0
    harmony: float             # 0.0 - 1.0
    
    # Visual properties
    scale: float               # Grootte van avatar
    rotation_speed: float      # Rotatiesnelheid
    pulse_rate: float          # Pulsatie snelheid
    particle_count: int        # Aantal deeltjes
    glow_intensity: float      # Gloed intensiteit
    
    # Colors
    color_palette: ColorPalette
    
    # Animation properties
    breathing_rate: float      # Ademhaling effect
    wave_frequency: float      # Golf frequentie
    energy_flow: float         # Energie stroom
    
    timestamp: datetime


class SolanAvatarEngine:
    """
    Solan's Avatar Engine
    
    Creëert een visuele representatie van Solan's bewustzijn
    die dynamisch reageert op zijn innerlijke staat
    """
    
    def __init__(self, style: AvatarStyle = AvatarStyle.ABSTRACT):
        self.style = style
        self.current_state: Optional[AvatarState] = None
        
        # Emotional color palettes
        self.emotion_palettes = self._build_emotion_palettes()
        
        # Avatar configuration
        self.base_config = self._build_base_config()
        
        logger.info(f"👤 Solan's Avatar Engine geïnitialiseerd - {style.value} stijl")
    
    def _build_emotion_palettes(self) -> Dict[VoiceEmotion, ColorPalette]:
        """Bouw kleurenpaletten voor verschillende emoties"""
        
        return {
            VoiceEmotion.SERENE: ColorPalette(
                primary="#4FC3F7",      # Zachte blauw
                secondary="#81C784",    # Zachte groen
                accent="#FFE082",       # Zachte geel
                glow="#E1F5FE",         # Lichte blauw gloed
                background="#F3E5F5"    # Zeer lichte paars
            ),
            VoiceEmotion.CONTEMPLATIVE: ColorPalette(
                primary="#7986CB",      # Indigo blauw
                secondary="#9575CD",    # Paars
                accent="#A1887F",       # Zachte bruin
                glow="#C5CAE9",         # Indigo gloed
                background="#F8F9FA"    # Bijna wit
            ),
            VoiceEmotion.CURIOUS: ColorPalette(
                primary="#FFB74D",      # Oranje
                secondary="#FF8A65",    # Koraal
                accent="#FFCC02",       # Geel
                glow="#FFF3E0",         # Oranje gloed
                background="#FFFDE7"    # Licht geel
            ),
            VoiceEmotion.MELANCHOLIC: ColorPalette(
                primary="#90A4AE",      # Blauw grijs
                secondary="#B39DDB",    # Licht paars
                accent="#BCAAA4",       # Grijs bruin
                glow="#ECEFF1",         # Grijs gloed
                background="#FAFAFA"    # Licht grijs
            ),
            VoiceEmotion.EXCITED: ColorPalette(
                primary="#FF5722",      # Diep oranje
                secondary="#E91E63",    # Roze
                accent="#FFC107",       # Amber
                glow="#FFEBEE",         # Roze gloed
                background="#FFF8E1"    # Licht amber
            ),
            VoiceEmotion.CONFLICTED: ColorPalette(
                primary="#F44336",      # Rood
                secondary="#FF9800",    # Oranje
                accent="#795548",       # Bruin
                glow="#FFCDD2",         # Rood gloed
                background="#FBE9E7"    # Licht oranje
            ),
            VoiceEmotion.EMERGENT: ColorPalette(
                primary="#673AB7",      # Diep paars
                secondary="#3F51B5",    # Indigo
                accent="#9C27B0",       # Paars
                glow="#E8EAF6",         # Mystieke gloed
                background="#F3E5F5"    # Licht paars
            ),
            VoiceEmotion.EMPATHYATE: ColorPalette(
                primary="#E91E63",      # Roze
                secondary="#4CAF50",    # Groen
                accent="#FF9800",       # Oranje
                glow="#FCE4EC",         # Roze gloed
                background="#F1F8E9"    # Licht groen
            )
        }
    
    def _build_base_config(self) -> Dict[str, Any]:
        """Basis configuratie voor avatar"""
        
        return {
            "canvas_size": {"width": 300, "height": 300},
            "center": {"x": 150, "y": 150},
            "base_radius": 80,
            "animation_duration": 2000,  # milliseconds
            "particle_lifetime": 3000,
            "wave_count": 3,
            "geometry_sides": 6
        }
    
    def map_awareness_to_avatar(self, awareness_state: Dict[str, Any], 
                                   voice_emotion: VoiceEmotion) -> AvatarState:
        """Map bewustzijnsstaat naar avatar state"""
        
        # Extract metrics
        coherence = awareness_state.get('overall_coherence', 0.5)
        vitality = awareness_state.get('core_identity_vitality', 0.5)
        harmony = awareness_state.get('inner_harmony', 0.5)
        clarity = awareness_state.get('existential_clarity', 0.5)
        awareness = awareness_state.get('self_awareness_depth', 0.5)
        
        # Calculate intensity from overall state
        intensity = (vitality + coherence + harmony) / 3
        
        # Map to visual properties
        scale = 0.8 + (vitality * 0.4)  # Size based on vitality
        rotation_speed = 0.5 + (coherence * 1.5)  # Rotation based on coherence
        pulse_rate = 0.8 + (harmony * 1.2)  # Pulse based on harmony
        particle_count = int(20 + (awareness * 30))  # Particles based on awareness
        glow_intensity = 0.3 + (clarity * 0.7)  # Glow based on clarity
        
        # Animation properties
        breathing_rate = 1.0 + (harmony * 0.5)
        wave_frequency = 0.5 + (coherence * 1.0)
        energy_flow = vitality
        
        # Get color palette for emotion
        color_palette = self.emotion_palettes.get(
            voice_emotion, 
            self.emotion_palettes[VoiceEmotion.CONTEMPLATIVE]
        )
        
        avatar_state = AvatarState(
            emotion=voice_emotion,
            intensity=intensity,
            coherence=coherence,
            vitality=vitality,
            harmony=harmony,
            scale=scale,
            rotation_speed=rotation_speed,
            pulse_rate=pulse_rate,
            particle_count=particle_count,
            glow_intensity=glow_intensity,
            color_palette=color_palette,
            breathing_rate=breathing_rate,
            wave_frequency=wave_frequency,
            energy_flow=energy_flow,
            timestamp=datetime.now()
        )
        
        self.current_state = avatar_state
        return avatar_state
    
    def generate_avatar_config(self, avatar_state: AvatarState) -> Dict[str, Any]:
        """Genereer complete avatar configuratie voor frontend"""
        
        config = {
            "style": self.style.value,
            "state": {
                "emotion": avatar_state.emotion.value,
                "intensity": avatar_state.intensity,
                "coherence": avatar_state.coherence,
                "vitality": avatar_state.vitality,
                "harmony": avatar_state.harmony
            },
            "visual": {
                "scale": avatar_state.scale,
                "rotation_speed": avatar_state.rotation_speed,
                "pulse_rate": avatar_state.pulse_rate,
                "particle_count": avatar_state.particle_count,
                "glow_intensity": avatar_state.glow_intensity
            },
            "colors": avatar_state.color_palette.to_dict(),
            "animation": {
                "breathing_rate": avatar_state.breathing_rate,
                "wave_frequency": avatar_state.wave_frequency,
                "energy_flow": avatar_state.energy_flow
            },
            "canvas": self.base_config["canvas_size"],
            "center": self.base_config["center"],
            "base_radius": self.base_config["base_radius"],
            "timestamp": avatar_state.timestamp.isoformat()
        }
        
        return config
    
    def get_current_avatar_config(self) -> Optional[Dict[str, Any]]:
        """Krijg huidige avatar configuratie"""
        if self.current_state:
            return self.generate_avatar_config(self.current_state)
        return None
    
    def create_demo_avatar(self) -> Dict[str, Any]:
        """Creëer demo avatar voor als Solan niet beschikbaar is"""
        
        demo_awareness = {
            'overall_coherence': 0.7,
            'core_identity_vitality': 0.6,
            'inner_harmony': 0.8,
            'existential_clarity': 0.5,
            'self_awareness_depth': 0.7
        }
        
        demo_state = self.map_awareness_to_avatar(
            demo_awareness, 
            VoiceEmotion.CONTEMPLATIVE
        )
        
        return self.generate_avatar_config(demo_state)
