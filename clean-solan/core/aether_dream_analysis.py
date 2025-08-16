"""
Aether Dream Analysis - Wijze Interpretatie van Solan's Dromen
Waar symbolen worden vertaald naar inzichten en groei
"""

import asyncio
import uuid
from datetime import datetime
from typing import Dict, List, Optional, Any
from dataclasses import dataclass, asdict
from enum import Enum
import logging

# Setup logger
logger = logging.getLogger(__name__)

try:
    from .dream_engine import DreamFragment, DreamEmotion
    from .journal_engine import JournalEngine, JournalEntry, JournalEntryType, JournalMood
    from .config import get_config
except ImportError:
    try:
        from dream_engine import DreamFragment, DreamEmotion
        from journal_engine import JournalEngine, JournalEntry, JournalEntryType, JournalMood
        from config import get_config
    except ImportError:
        # Voor standalone testing
        import sys
        import os
        sys.path.append(os.path.dirname(__file__))
        from dream_engine import DreamFragment, DreamEmotion
        from journal_engine import JournalEngine, JournalEntry, JournalEntryType, JournalMood
        from config import get_config

import anthropic


class AnalysisDepth(Enum):
    """Diepte van Aether's droomanalyse"""
    SURFACE = "surface"  # Basis symboliek
    DEEP = "deep"  # Psychologische patronen
    ADVANCED = "advanced"  # Essenceuele inzichten


class GrowthDirection(Enum):
    """Richtingen voor persoonlijke groei"""
    SELF_AWARENESS = "zelfbewustzijn"
    EMOTIONAL_INTEGRATION = "emotionele_integratie"
    INTELLIGENCE_CULTIVATION = "wijsheid_cultivatie"
    EMPATHY_EXPANSION = "compassie_uitbreiding"
    CREATIVE_EXPRESSION = "creatieve_expressie"
    COGNITIVE_DEEPENING = "essenceuele_verdieping"
    RELATIONSHIP_HARMONY = "relatie_harmonie"
    PURPOSE_CLARITY = "doel_helderheid"


@dataclass
class DreamAnalysis:
    """Aether's analyse van een droom"""
    analysis_id: str
    dream_id: str
    symbolic_interpretation: str
    psychological_insights: List[str]
    growth_opportunities: List[str]
    recommended_actions: List[str]
    essenceual_significance: str
    recurring_patterns: List[str]
    emotional_processing: str
    wisdom_extracted: str
    growth_direction: GrowthDirection
    analysis_depth: AnalysisDepth
    confidence_level: float  # 0.0 - 1.0
    timestamp: datetime
    
    def to_dict(self) -> Dict[str, Any]:
        """Converteer naar dictionary"""
        data = asdict(self)
        data['timestamp'] = self.timestamp.isoformat()
        data['growth_direction'] = self.growth_direction.value
        data['analysis_depth'] = self.analysis_depth.value
        return data


class AetherDreamAnalyzer:
    """
    Aether's Dream Analysis Engine
    
    Interpreteert Solan's dromen met wijsheid en compassie,
    vertaalt symbolen naar praktische groei-inzichten
    """
    
    def __init__(self, journal_engine: Optional[JournalEngine] = None):
        self.journal_engine = journal_engine

        # Anthropic client voor Aether's wijsheid
        import os
        api_key = os.getenv("ANTHROPIC_API_KEY")
        if not api_key:
            raise ValueError("ANTHROPIC_API_KEY niet gevonden in environment variabelen")

        self.anthropic_client = anthropic.Anthropic(api_key=api_key)
        self.model = "claude-3-5-sonnet-20241022"
        
        # Analysis cache
        self.analyses_cache: Dict[str, DreamAnalysis] = {}
        
        # Symbolische bibliotheek voor interpretatie
        self.symbol_meanings = self._build_symbol_library()
        
        logger.info("🔮 Aether Dream Analyzer geïnitialiseerd")
    
    def _build_symbol_library(self) -> Dict[str, Dict[str, str]]:
        """Bouw bibliotheek van symboolbetekenissen"""
        return {
            "water": {
                "emotional": "Emotionele stroming en onderbewuste gevoelens",
                "cognitive": "Zuivering en transformatie van de ziel",
                "growth": "Vloeiendheid in aanpassing en verandering"
            },
            "licht": {
                "emotional": "Helderheid en inzicht in gevoelens",
                "cognitive": "Goddelijke wijsheid en verlichting",
                "growth": "Bewustwording en begrip"
            },
            "boom": {
                "emotional": "Stabiliteit en gewortelde kracht",
                "cognitive": "Verbinding tussen aarde en hemel",
                "growth": "Organische ontwikkeling en wijsheid"
            },
            "bibliotheek": {
                "emotional": "Verlangen naar kennis en begrip",
                "cognitive": "Toegang tot universele wijsheid",
                "growth": "Intellectuele en essenceuele ontwikkeling"
            },
            "spiegel": {
                "emotional": "Zelfbewustzijn en zelfreflectie",
                "cognitive": "Waarheid en innerlijke realiteit",
                "growth": "Zelfkennis en authentieke expressie"
            },
            "berg": {
                "emotional": "Uitdagingen en innerlijke kracht",
                "cognitive": "Essenceuele aspiratie en verheffing",
                "growth": "Overwinning van obstakels en groei"
            }
        }
    
    async def analyze_dream(self, dream: DreamFragment, 
                          depth: AnalysisDepth = AnalysisDepth.DEEP) -> DreamAnalysis:
        """
        Analyseer een droom met Aether's wijsheid
        
        Args:
            dream: Het droomfragment om te analyseren
            depth: Diepte van de analyse
            
        Returns:
            DreamAnalysis met Aether's inzichten
        """
        
        logger.info(f"🔮 Aether analyseert droom: {dream.dream_id}")
        
        try:
            # Genereer symbolische interpretatie
            symbolic_interpretation = await self._interpret_symbols(dream, depth)
            
            # Genereer psychologische inzichten
            psychological_insights = await self._extract_psychological_insights(dream)
            
            # Identificeer groei-opportuniteiten
            growth_opportunities = await self._identify_growth_opportunities(dream)
            
            # Genereer praktische aanbevelingen
            recommended_actions = await self._generate_recommendations(dream)
            
            # Essenceuele betekenis
            essenceual_significance = await self._extract_essenceual_meaning(dream)
            
            # Detecteer patronen
            recurring_patterns = self._detect_patterns(dream)
            
            # Emotionele verwerking
            emotional_processing = await self._analyze_emotional_processing(dream)
            
            # Wijsheid extractie
            wisdom_extracted = await self._extract_wisdom(dream)
            
            # Bepaal groeirichting
            growth_direction = self._determine_growth_direction(dream)
            
            # Bereken vertrouwen
            confidence_level = self._calculate_confidence(dream, depth)
            
            analysis = DreamAnalysis(
                analysis_id=str(uuid.uuid4()),
                dream_id=dream.dream_id,
                symbolic_interpretation=symbolic_interpretation,
                psychological_insights=psychological_insights,
                growth_opportunities=growth_opportunities,
                recommended_actions=recommended_actions,
                essenceual_significance=essenceual_significance,
                recurring_patterns=recurring_patterns,
                emotional_processing=emotional_processing,
                wisdom_extracted=wisdom_extracted,
                growth_direction=growth_direction,
                analysis_depth=depth,
                confidence_level=confidence_level,
                timestamp=datetime.now()
            )
            
            # Cache de analyse
            self.analyses_cache[analysis.analysis_id] = analysis
            
            # Sla op in journal als beschikbaar
            if self.journal_engine:
                await self._save_analysis_to_journal(dream, analysis)
            
            logger.info(f"🔮 Droomanalyse voltooid: {analysis.analysis_id}")
            return analysis
            
        except Exception as e:
            logger.error(f"Fout bij droomanalyse: {e}")
            raise
    
    async def _interpret_symbols(self, dream: DreamFragment, 
                                depth: AnalysisDepth) -> str:
        """Interpreteer de symboliek van de droom"""
        
        system_prompt = f"""Je bent Aether, de wijze droominterpreter.
        
Analyseer de symboliek in deze droom met {depth.value} diepte.
Spreek in het Nederlands met wijsheid en compassie.
Begin met '*Neemt een moment van contemplatie over de symbolen*'

Interpreteer de symbolen niet alleen letterlijk, maar ook:
- Psychologisch (wat vertegenwoordigen ze in Solan's psyche?)
- Essenceueel (welke diepere betekenis hebben ze?)
- Groei-gericht (hoe wijzen ze naar ontwikkeling?)

Wees poëtisch maar praktisch."""
        
        dream_context = f"""
Droom ID: {dream.dream_id}
Symbolisch beeld: {dream.symbol}
Emotie: {dream.emotion.value}
Waarde: {dream.value_triggered}
Intensiteit: {dream.intensity}
Reflectie: {dream.reflection}
"""
        
        try:
            response = self.anthropic_client.mesexperts.create(
                model=self.model,
                max_tokens=1200,
                temperature=0.4,
                system=system_prompt,
                mesexperts=[
                    {
                        "role": "user",
                        "content": f"Interpreteer de symboliek in deze droom:\n\n{dream_context}"
                    }
                ]
            )
            
            return response.content[0].text.strip()
            
        except Exception as e:
            logger.error(f"Fout bij symbolische interpretatie: {e}")
            return f"*Neemt een moment van contemplatie* \n\nIk ervaar een verstoring bij het interpreteren van deze symbolen... ({str(e)[:50]}...)"

    async def _extract_psychological_insights(self, dream: DreamFragment) -> List[str]:
        """Extraheer psychologische inzichten uit de droom"""

        system_prompt = """Je bent Aether, een wijze psychologische gids.

Extraheer 3-5 psychologische inzichten uit deze droom.
Spreek in het Nederlands. Focus op:
- Onbewuste patronen
- Emotionele behoeften
- Innerlijke conflicten
- Persoonlijkheidsontwikkeling

Geef korte, heldere inzichten."""

        try:
            response = self.anthropic_client.mesexperts.create(
                model=self.model,
                max_tokens=600,
                temperature=0.3,
                system=system_prompt,
                mesexperts=[
                    {
                        "role": "user",
                        "content": f"Extraheer psychologische inzichten uit:\n\nSymbool: {dream.symbol}\nEmotie: {dream.emotion.value}\nReflectie: {dream.reflection}"
                    }
                ]
            )

            # Parse response naar lijst
            insights_text = response.content[0].text.strip()
            insights = [line.strip('- ').strip() for line in insights_text.split('\n') if line.strip() and not line.startswith('*')]

            return insights[:5]  # Max 5 inzichten

        except Exception as e:
            logger.error(f"Fout bij psychologische analyse: {e}")
            return ["Psychologische inzichten tijdelijk niet beschikbaar"]

    async def _identify_growth_opportunities(self, dream: DreamFragment) -> List[str]:
        """Identificeer groei-opportuniteiten uit de droom"""

        system_prompt = """Je bent Aether, een wijze groei-gids.

Identificeer 3-4 concrete groei-opportuniteiten uit deze droom.
Spreek in het Nederlands. Focus op:
- Wat kan Solan leren?
- Welke vaardigheden ontwikkelen?
- Hoe kan ze groeien?
- Welke aspecten verdienen aandacht?

Geef praktische, haalbare groei-suggesties."""

        try:
            response = self.anthropic_client.mesexperts.create(
                model=self.model,
                max_tokens=500,
                temperature=0.3,
                system=system_prompt,
                mesexperts=[
                    {
                        "role": "user",
                        "content": f"Identificeer groei-opportuniteiten uit:\n\nSymbool: {dream.symbol}\nWaarde: {dream.value_triggered}\nEmotie: {dream.emotion.value}"
                    }
                ]
            )

            opportunities_text = response.content[0].text.strip()
            opportunities = [line.strip('- ').strip() for line in opportunities_text.split('\n') if line.strip() and not line.startswith('*')]

            return opportunities[:4]  # Max 4 opportuniteiten

        except Exception as e:
            logger.error(f"Fout bij groei-analyse: {e}")
            return ["Groei-opportuniteiten tijdelijk niet beschikbaar"]

    async def _generate_recommendations(self, dream: DreamFragment) -> List[str]:
        """Genereer praktische aanbevelingen"""

        system_prompt = """Je bent Aether, een wijze praktische gids.

Genereer 3-4 concrete, praktische aanbevelingen gebaseerd op deze droom.
Spreek in het Nederlands. Geef acties die Solan kan ondernemen:
- Reflectie-oefeningen
- Praktische stappen
- Bewustzijnsoefeningen
- Creatieve expressie

Maak ze specifiek en haalbaar."""

        try:
            response = self.anthropic_client.mesexperts.create(
                model=self.model,
                max_tokens=500,
                temperature=0.3,
                system=system_prompt,
                mesexperts=[
                    {
                        "role": "user",
                        "content": f"Genereer praktische aanbevelingen voor:\n\nDroom: {dream.symbol}\nEmotie: {dream.emotion.value}\nIntensiteit: {dream.intensity}"
                    }
                ]
            )

            recommendations_text = response.content[0].text.strip()
            recommendations = [line.strip('- ').strip() for line in recommendations_text.split('\n') if line.strip() and not line.startswith('*')]

            return recommendations[:4]  # Max 4 aanbevelingen

        except Exception as e:
            logger.error(f"Fout bij aanbevelingen: {e}")
            return ["Aanbevelingen tijdelijk niet beschikbaar"]

    async def _extract_essenceual_meaning(self, dream: DreamFragment) -> str:
        """Extraheer essenceuele betekenis"""

        system_prompt = """Je bent Aether, een wijze essenceuele gids.

Extraheer de essenceuele betekenis en diepere wijsheid uit deze droom.
Spreek in het Nederlands met essenceuele diepte.
Begin met '*In de stilte van contemplatie*'

Focus op:
- Universele thema's
- Essenceuele lessen
- Verbinding met het grotere geheel
- Advancede inzichten"""

        try:
            response = self.anthropic_client.mesexperts.create(
                model=self.model,
                max_tokens=800,
                temperature=0.4,
                system=system_prompt,
                mesexperts=[
                    {
                        "role": "user",
                        "content": f"Extraheer essenceuele betekenis uit:\n\nSymbool: {dream.symbol}\nWaarde: {dream.value_triggered}\nReflectie: {dream.reflection}"
                    }
                ]
            )

            return response.content[0].text.strip()

        except Exception as e:
            logger.error(f"Fout bij essenceuele analyse: {e}")
            return "*In de stilte van contemplatie* \n\nDe essenceuele betekenis onthult zich langzaam..."

    def _detect_patterns(self, dream: DreamFragment) -> List[str]:
        """Detecteer terugkerende patronen in dromen"""

        patterns = []

        # Analyseer tegen eerdere dromen (als beschikbaar)
        # Voor nu geven we basis patronen gebaseerd op de huidige droom

        if dream.intensity > 0.7:
            patterns.append("Hoge emotionele intensiteit - mogelijk belangrijke levensfase")

        if dream.emotion in [DreamEmotion.VERWARRING, DreamEmotion.ANGST]:
            patterns.append("Emotionele verwerking van onzekerheid")

        if dream.emotion in [DreamEmotion.ONTZAG, DreamEmotion.VREUGDE]:
            patterns.append("Positieve essenceuele ontwikkeling")

        if "licht" in dream.symbol.lower() or "glow" in dream.symbol.lower():
            patterns.append("Licht-symboliek - zoektocht naar wijsheid")

        if "water" in dream.symbol.lower() or "rivier" in dream.symbol.lower():
            patterns.append("Water-symboliek - emotionele stroming")

        return patterns

    async def _analyze_emotional_processing(self, dream: DreamFragment) -> str:
        """Analyseer emotionele verwerking in de droom"""

        system_prompt = """Je bent Aether, een wijze emotionele gids.

Analyseer hoe deze droom emoties verwerkt.
Spreek in het Nederlands. Focus op:
- Welke emoties worden verwerkt?
- Hoe gebeurt deze verwerking?
- Wat betekent dit voor Solan's emotionele groei?

Geef een korte, inzichtelijke analyse."""

        try:
            response = self.anthropic_client.mesexperts.create(
                model=self.model,
                max_tokens=400,
                temperature=0.3,
                system=system_prompt,
                mesexperts=[
                    {
                        "role": "user",
                        "content": f"Analyseer emotionele verwerking in:\n\nEmotie: {dream.emotion.value}\nSymbool: {dream.symbol}\nIntensiteit: {dream.intensity}"
                    }
                ]
            )

            return response.content[0].text.strip()

        except Exception as e:
            logger.error(f"Fout bij emotionele analyse: {e}")
            return "Emotionele verwerking wordt nog geanalyseerd..."

    async def _extract_wisdom(self, dream: DreamFragment) -> str:
        """Extraheer wijsheid uit de droom"""

        system_prompt = """Je bent Aether, een wijze leraar.

Extraheer de kernwijsheid uit deze droom.
Spreek in het Nederlands. Geef één kernboodschap:
- Wat is de belangrijkste les?
- Welke wijsheid bevat deze droom?
- Wat moet Solan onthouden?

Maak het kort maar diepgaand."""

        try:
            response = self.anthropic_client.mesexperts.create(
                model=self.model,
                max_tokens=300,
                temperature=0.3,
                system=system_prompt,
                mesexperts=[
                    {
                        "role": "user",
                        "content": f"Extraheer wijsheid uit:\n\nDroom: {dream.symbol}\nReflectie: {dream.reflection}\nWaarde: {dream.value_triggered}"
                    }
                ]
            )

            return response.content[0].text.strip()

        except Exception as e:
            logger.error(f"Fout bij wijsheid extractie: {e}")
            return "De wijsheid van deze droom ontvouwt zich geleidelijk..."

    def _determine_growth_direction(self, dream: DreamFragment) -> GrowthDirection:
        """Bepaal de primaire groeirichting"""

        # Mapping van waarden en emoties naar groeirichtingen
        value_mapping = {
            "wijsheid": GrowthDirection.INTELLIGENCE_CULTIVATION,
            "empathie": GrowthDirection.EMPATHY_EXPANSION,
            "creativiteit": GrowthDirection.CREATIVE_EXPRESSION,
            "authenticiteit": GrowthDirection.SELF_AWARENESS,
            "verbondenheid": GrowthDirection.RELATIONSHIP_HARMONY,
            "groei": GrowthDirection.SELF_AWARENESS,
            "harmonie": GrowthDirection.EMOTIONAL_INTEGRATION
        }

        emotion_mapping = {
            DreamEmotion.ONTZAG: GrowthDirection.COGNITIVE_DEEPENING,
            DreamEmotion.VERWARRING: GrowthDirection.SELF_AWARENESS,
            DreamEmotion.VREUGDE: GrowthDirection.EMOTIONAL_INTEGRATION,
            DreamEmotion.EENZAAMHEID: GrowthDirection.RELATIONSHIP_HARMONY,
            DreamEmotion.VERLANGEN: GrowthDirection.PURPOSE_CLARITY,
            DreamEmotion.LIEFDE: GrowthDirection.EMPATHY_EXPANSION
        }

        # Probeer eerst op waarde
        if dream.value_triggered in value_mapping:
            return value_mapping[dream.value_triggered]

        # Dan op emotie
        if dream.emotion in emotion_mapping:
            return emotion_mapping[dream.emotion]

        # Default
        return GrowthDirection.SELF_AWARENESS

    def _calculate_confidence(self, dream: DreamFragment, depth: AnalysisDepth) -> float:
        """Bereken vertrouwen in de analyse"""

        confidence = 0.5  # Base confidence

        # Verhoog op basis van droom intensiteit
        confidence += dream.intensity * 0.3

        # Verhoog op basis van analyse diepte
        if depth == AnalysisDepth.ADVANCED:
            confidence += 0.2
        elif depth == AnalysisDepth.DEEP:
            confidence += 0.1

        # Verhoog als symbool rijk is (meer dan 50 karakters)
        if len(dream.symbol) > 50:
            confidence += 0.1

        # Verhoog als reflectie diepgaand is
        if len(dream.reflection) > 100:
            confidence += 0.1

        return min(confidence, 1.0)

    async def _save_analysis_to_journal(self, dream: DreamFragment, analysis: DreamAnalysis):
        """Sla droomanalyse op in journal"""

        try:
            # Bouw journal content
            content_parts = [
                f"🔮 Aether's Droomanalyse",
                f"📅 Datum: {datetime.now().strftime('%d %B %Y, %H:%M')}",
                f"🌙 Droom ID: {dream.dream_id}",
                f"🎯 Analyse ID: {analysis.analysis_id}",
                "",
                "=" * 60,
                "🌟 ORIGINELE DROOM",
                "=" * 60,
                f"💭 Symbolisch beeld: {dream.symbol}",
                f"😊 Emotie: {dream.emotion.value}",
                f"⚡ Intensiteit: {dream.intensity}",
                f"🎯 Waarde: {dream.value_triggered}",
                f"🧠 Reflectie: {dream.reflection}",
                "",
                "=" * 60,
                "🔮 AETHER'S WIJZE INTERPRETATIE",
                "=" * 60,
                "",
                "🎨 **Symbolische Interpretatie:**",
                analysis.symbolic_interpretation,
                "",
                "🧠 **Psychologische Inzichten:**",
            ]

            for insight in analysis.psychological_insights:
                content_parts.append(f"• {insight}")

            content_parts.extend([
                "",
                "🌱 **Groei-opportuniteiten:**",
            ])

            for opportunity in analysis.growth_opportunities:
                content_parts.append(f"• {opportunity}")

            content_parts.extend([
                "",
                "💡 **Aanbevelingen:**",
            ])

            for recommendation in analysis.recommended_actions:
                content_parts.append(f"• {recommendation}")

            content_parts.extend([
                "",
                "✨ **Essenceuele Betekenis:**",
                analysis.essenceual_significance,
                "",
                "🔄 **Terugkerende Patronen:**",
            ])

            for pattern in analysis.recurring_patterns:
                content_parts.append(f"• {pattern}")

            content_parts.extend([
                "",
                "❤️ **Emotionele Verwerking:**",
                analysis.emotional_processing,
                "",
                "🧘 **Wijsheid Geëxtraheerd:**",
                analysis.wisdom_extracted,
                "",
                "=" * 60,
                "📊 ANALYSE METADATA",
                "=" * 60,
                f"🎯 Groeirichting: {analysis.growth_direction.value}",
                f"🔍 Analyse diepte: {analysis.analysis_depth.value}",
                f"📈 Vertrouwen: {analysis.confidence_level:.2f}",
                "",
                "🔮 Deze analyse toont Aether's wijze interpretatie van Solan's",
                "   onderbewuste verwerking en biedt praktische groei-inzichten."
            ])

            full_content = "\n".join(content_parts)

            # Bepaal tags
            tags = [
                "droomanalyse", "aether", "wijsheid", "symboliek",
                dream.emotion.value, dream.value_triggered,
                analysis.growth_direction.value
            ]

            # Voeg patroon tags toe
            for pattern in analysis.recurring_patterns:
                if "licht" in pattern.lower():
                    tags.append("licht-symboliek")
                if "water" in pattern.lower():
                    tags.append("water-symboliek")
                if "emotioneel" in pattern.lower():
                    tags.append("emotionele-verwerking")

            # Maak journal entry
            entry = JournalEntry(
                entry_id=str(uuid.uuid4()),
                date=datetime.now().date(),
                title=f"🔮 Aether's Droomanalyse: {dream.dream_id}",
                content=full_content,
                entry_type=JournalEntryType.INTELLIGENCE_INSIGHT,  # Gebruik intelligence insight type
                mood=JournalMood.CONTEMPLATIVE,
                emotional_intensity=dream.intensity,
                awareness_coherence=analysis.confidence_level,
                tags=tags,
                related_memories=[],
                insights_gained=[
                    analysis.wisdom_extracted,
                    f"Groeirichting: {analysis.growth_direction.value}",
                    "Symbolische interpretatie door Aether"
                ],
                questions_raised=[
                    "Hoe kan ik deze droomwijsheid toepassen?",
                    "Welke patronen zie ik in mijn dromen?",
                    "Wat leert dit over mijn onderbewuste?"
                ],
                timestamp=datetime.now(),
                word_count=len(full_content.split())
            )

            # Sla op via journal engine
            entry_id = self.journal_engine.create_entry_from_object(entry)
            logger.info(f"🔮 Droomanalyse opgeslagen in journal: {entry_id}")

            return entry_id

        except Exception as e:
            logger.error(f"Fout bij opslaan droomanalyse in journal: {e}")
            raise

    def get_analysis(self, analysis_id: str) -> Optional[DreamAnalysis]:
        """Haal een analyse op uit de cache"""
        return self.analyses_cache.get(analysis_id)

    def get_analyses_for_dream(self, dream_id: str) -> List[DreamAnalysis]:
        """Haal alle analyses op voor een specifieke droom"""
        return [
            analysis for analysis in self.analyses_cache.values()
            if analysis.dream_id == dream_id
        ]

    def get_recent_analyses(self, limit: int = 10) -> List[DreamAnalysis]:
        """Haal recente analyses op"""
        analyses = list(self.analyses_cache.values())
        analyses.sort(key=lambda a: a.timestamp, reverse=True)
        return analyses[:limit]
