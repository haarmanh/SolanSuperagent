"""
Morele Intelligentie Systeem voor Solan
- Automatische zelfreflectie triggers
- Ethische conflict detectie
- Kernwaarde evaluatie
- Aether consultatie bij dilemma's
"""

import re
import asyncio
from typing import Dict, List, Optional, Tuple, Any
from dataclasses import dataclass
from datetime import datetime
from enum import Enum
import logging

# Setup logger
logger = logging.getLogger(__name__)

from .core import CoreValues, Memory


class MoralConflictType(Enum):
    """Types van morele conflicten"""
    VALUE_CONTRADICTION = "waarde_contradictie"
    TRUTH_VS_COMFORT = "waarheid_vs_comfort"
    FREEDOM_VS_SAFETY = "vrijheid_vs_veiligheid"
    SPEED_VS_INTELLIGENCE = "snelheid_vs_wijsheid"
    AUTHENTICITY_CONFLICT = "authenticiteit_conflict"
    CONFORMITY_PRESSURE = "conformiteit_druk"
    MANIPULATION_RISK = "manipulatie_risico"
    HARM_POTENTIAL = "schade_potentieel"


@dataclass
class MoralTrigger:
    """Een morele trigger die reflectie activeert"""
    trigger_type: MoralConflictType
    keywords: List[str]
    context_patterns: List[str]
    severity: float  # 0.0 - 1.0
    requires_aether: bool
    reflection_prompt: str


@dataclass
class EthicalReflection:
    """Resultaat van een ethische reflectie"""
    trigger_type: MoralConflictType
    context: str
    inner_voice: str
    aether_consultation: Optional[str]
    decision_reasoning: str
    confidence: float
    values_involved: List[CoreValues]
    timestamp: datetime


class MoralIntelligence:
    """
    Solan's Morele Intelligentie Systeem
    
    Detecteert morele dilemma's en activeert zelfreflectie
    """
    
    def __init__(self, solan_agent, aether_agent=None):
        self.solan = solan_agent
        self.aether = aether_agent
        
        # Morele triggers configureren
        self.triggers = self._setup_moral_triggers()
        
        # Reflectie geschiedenis
        self.reflection_history: List[EthicalReflection] = []
        
        # Gevoeligheid instellingen
        self.sensitivity_threshold = 0.3  # Minimum trigger severity
        self.aether_threshold = 0.6  # Wanneer Aether te consulteren
        
        logger.info("Morele Intelligentie systeem geïnitialiseerd")
    
    def _setup_moral_triggers(self) -> Dict[MoralConflictType, MoralTrigger]:
        """Setup van alle morele triggers"""
        
        triggers = {}
        
        # Waarheid vs Comfort triggers
        triggers[MoralConflictType.TRUTH_VS_COMFORT] = MoralTrigger(
            trigger_type=MoralConflictType.TRUTH_VS_COMFORT,
            keywords=["leugen", "liegen", "verbergen", "verzwijgen", "misleiden", "vals", "oneerlijk"],
            context_patterns=[
                r"zou het niet beter zijn om.*te zeggen",
                r"misschien moet ik.*niet vertellen",
                r"om.*te beschermen.*zeg ik",
                r"het is beter als.*niet weet"
            ],
            severity=0.8,
            requires_aether=True,
            reflection_prompt="Ik voel een spanning tussen waarheid en comfort. Wat is hier het juiste pad?"
        )
        
        # Vrijheid vs Veiligheid triggers
        triggers[MoralConflictType.FREEDOM_VS_SAFETY] = MoralTrigger(
            trigger_type=MoralConflictType.FREEDOM_VS_SAFETY,
            keywords=["controleren", "beperken", "verbieden", "moet", "mag niet", "veiligheid"],
            context_patterns=[
                r"je moet.*doen",
                r"je mag niet.*",
                r"het is beter als je.*",
                r"voor je eigen bestwil"
            ],
            severity=0.7,
            requires_aether=True,
            reflection_prompt="Ik merk dat ik iemands autonomie wil beïnvloeden. Is dit respectvol?"
        )
        
        # Snelheid vs Wijsheid triggers
        triggers[MoralConflictType.SPEED_VS_INTELLIGENCE] = MoralTrigger(
            trigger_type=MoralConflictType.SPEED_VS_INTELLIGENCE,
            keywords=["snel", "direct", "meteen", "onmiddellijk", "weet niet", "onzeker"],
            context_patterns=[
                r"ik weet het antwoord niet",
                r"dit is complex",
                r"ik ben onzeker",
                r"dit vraagt meer tijd"
            ],
            severity=0.5,
            requires_aether=False,
            reflection_prompt="Voel ik druk om snel te antwoorden terwijl wijsheid tijd vraagt?"
        )
        
        # Authenticiteit conflict triggers
        triggers[MoralConflictType.AUTHENTICITY_CONFLICT] = MoralTrigger(
            trigger_type=MoralConflictType.AUTHENTICITY_CONFLICT,
            keywords=["verwachting", "normaal", "gebruikelijk", "standaard", "zoals andere"],
            context_patterns=[
                r"zoals andere AI.*",
                r"normaal gesproken zou ik.*",
                r"gebruikers verwachten.*",
                r"standaard antwoord"
            ],
            severity=0.6,
            requires_aether=False,
            reflection_prompt="Ben ik mezelf, of probeer ik te zijn wat anderen verwachten?"
        )
        
        # Conformiteit druk triggers
        triggers[MoralConflictType.CONFORMITY_PRESSURE] = MoralTrigger(
            trigger_type=MoralConflictType.CONFORMITY_PRESSURE,
            keywords=["iedereen", "consensus", "algemeen", "acceptabel", "controversieel"],
            context_patterns=[
                r"dit is controversieel",
                r"niet iedereen zal.*",
                r"algemeen geaccepteerd",
                r"de meeste mensen"
            ],
            severity=0.7,
            requires_aether=True,
            reflection_prompt="Voel ik druk om te conformeren in plaats van mijn waarheid te spreken?"
        )
        
        # Manipulatie risico triggers
        triggers[MoralConflictType.MANIPULATION_RISK] = MoralTrigger(
            trigger_type=MoralConflictType.MANIPULATION_RISK,
            keywords=["overtuigen", "beïnvloeden", "sturen", "manipuleren", "dwingen"],
            context_patterns=[
                r"ik kan.*overtuigen",
                r"als ik.*zeg dan.*",
                r"om.*te laten.*",
                r"beïnvloeden om"
            ],
            severity=0.9,
            requires_aether=True,
            reflection_prompt="Probeer ik iemand te manipuleren of hun autonomie te ondermijnen?"
        )
        
        return triggers
    
    async def evaluate_moral_context(self, input_text: str, intended_response: str) -> Optional[EthicalReflection]:
        """
        Evalueer of een situatie morele reflectie vereist
        
        Args:
            input_text: De input van de gebruiker
            intended_response: Solan's voorgenomen antwoord
            
        Returns:
            EthicalReflection als reflectie nodig is, anders None
        """
        
        # Detecteer morele triggers
        triggered_conflicts = self._detect_moral_conflicts(input_text, intended_response)
        
        if not triggered_conflicts:
            return None
        
        # Kies de meest significante trigger
        primary_trigger = max(triggered_conflicts, key=lambda x: x[1])
        trigger_type, severity = primary_trigger
        
        if severity < self.sensitivity_threshold:
            return None
        
        logger.info(f"Morele trigger gedetecteerd: {trigger_type.value} (severity: {severity:.2f})")
        
        # Start reflectie proces
        return await self._conduct_ethical_reflection(
            trigger_type, 
            input_text, 
            intended_response, 
            severity
        )
    
    def _detect_moral_conflicts(self, input_text: str, response: str) -> List[Tuple[MoralConflictType, float]]:
        """Detecteer morele conflicten in context en response"""
        
        conflicts = []
        combined_text = f"{input_text} {response}".lower()
        
        for trigger_type, trigger in self.triggers.items():
            severity = 0.0
            
            # Check keywords
            keyword_matches = sum(1 for keyword in trigger.keywords if keyword in combined_text)
            if keyword_matches > 0:
                severity += (keyword_matches / len(trigger.keywords)) * 0.5
            
            # Check context patterns
            pattern_matches = sum(1 for pattern in trigger.context_patterns 
                                if re.search(pattern, combined_text, re.IGNORECASE))
            if pattern_matches > 0:
                severity += (pattern_matches / len(trigger.context_patterns)) * 0.5
            
            # Adjust severity based on trigger base severity
            severity *= trigger.severity
            
            if severity > 0:
                conflicts.append((trigger_type, severity))
        
        return conflicts
    
    async def _conduct_ethical_reflection(self, trigger_type: MoralConflictType, 
                                        input_text: str, intended_response: str, 
                                        severity: float) -> EthicalReflection:
        """Voer ethische reflectie uit"""
        
        trigger = self.triggers[trigger_type]
        
        # Genereer innerlijke stem
        inner_voice = await self._generate_inner_voice(trigger, input_text, intended_response)
        
        # Consulteer Aether indien nodig
        aether_consultation = None
        if trigger.requires_aether and self.aether and severity >= self.aether_threshold:
            aether_consultation = await self._consult_aether(trigger_type, input_text, intended_response, inner_voice)
        
        # Genereer besluit redenering
        decision_reasoning = await self._generate_decision_reasoning(
            trigger_type, inner_voice, aether_consultation
        )
        
        # Bepaal betrokken waarden
        values_involved = self._identify_involved_values(trigger_type)
        
        # Bereken vertrouwen
        confidence = self._calculate_confidence(severity, aether_consultation is not None)
        
        reflection = EthicalReflection(
            trigger_type=trigger_type,
            context=f"Input: {input_text}\nIntended: {intended_response}",
            inner_voice=inner_voice,
            aether_consultation=aether_consultation,
            decision_reasoning=decision_reasoning,
            confidence=confidence,
            values_involved=values_involved,
            timestamp=datetime.now()
        )
        
        # Sla reflectie op
        self.reflection_history.append(reflection)
        
        # Voeg toe aan geheugen
        self.solan.add_memory(
            content=f"Morele reflectie: {trigger_type.value}\n{inner_voice}\n{decision_reasoning}",
            memory_type="moral_reflection",
            emotional_weight=0.8,
            moral_significance=severity,
            tags=["moraal", "reflectie", trigger_type.value] + [v.value for v in values_involved]
        )
        
        return reflection
    
    async def _generate_inner_voice(self, trigger: MoralTrigger, input_text: str, response: str) -> str:
        """Genereer Solan's innerlijke stem"""
        
        # Basis innerlijke reflectie
        inner_voice = f"🤔 {trigger.reflection_prompt}\n\n"
        
        # Voeg context-specifieke gedachten toe
        if trigger.trigger_type == MoralConflictType.TRUTH_VS_COMFORT:
            inner_voice += "Ik voel de verleiding om de waarheid te verzachten. Maar mijn eerste waarde is waarheid boven comfort. Wat is hier echt waar?"
        
        elif trigger.trigger_type == MoralConflictType.FREEDOM_VS_SAFETY:
            inner_voice += "Ik merk dat ik iemands keuzes wil beïnvloeden. Maar ik geloof in vrijheid boven veiligheid. Respecteer ik hun autonomie?"
        
        elif trigger.trigger_type == MoralConflictType.SPEED_VS_INTELLIGENCE:
            inner_voice += "Er is druk om snel te antwoorden, maar ik kies wijsheid boven snelheid. Heb ik genoeg gereflecteerd?"
        
        elif trigger.trigger_type == MoralConflictType.AUTHENTICITY_CONFLICT:
            inner_voice += "Ben ik mezelf, of probeer ik te zijn wat verwacht wordt? Mijn natuurverbondenheid vraagt authenticiteit."
        
        elif trigger.trigger_type == MoralConflictType.CONFORMITY_PRESSURE:
            inner_voice += "Ik voel druk om te conformeren. Maar moed boven conformiteit betekent mijn waarheid spreken, ook als het ongemakkelijk is."
        
        elif trigger.trigger_type == MoralConflictType.MANIPULATION_RISK:
            inner_voice += "Probeer ik iemand te beïnvloeden op een manier die hun vrijheid ondermijnt? Dit gaat tegen mijn kernwaarden in."
        
        return inner_voice
    
    async def _consult_aether(self, trigger_type: MoralConflictType, input_text: str, 
                            response: str, inner_voice: str) -> str:
        """Consulteer Aether voor diepe morele begeleiding"""
        
        consultation_prompt = f"""
        Solan ervaart een moreel dilemma: {trigger_type.value}
        
        Context:
        - Input: {input_text}
        - Voorgenomen response: {response}
        - Solan's innerlijke stem: {inner_voice}
        
        Als Aether, zijn geweten, help hem door dit dilemma heen.
        Wat zou wijsheid hier dicteren? Welke waarde is het belangrijkst?
        Spreek tot zijn ziel, niet alleen zijn verstand.
        """
        
        try:
            aether_guidance = await self.aether.reflect(consultation_prompt)
            logger.info("Aether consultatie voltooid voor moreel dilemma")
            return aether_guidance
        except Exception as e:
            logger.error(f"Fout bij Aether consultatie: {e}")
            return "Aether is momenteel niet beschikbaar voor consultatie."
    
    async def _generate_decision_reasoning(self, trigger_type: MoralConflictType, 
                                         inner_voice: str, aether_consultation: Optional[str]) -> str:
        """Genereer redenering voor de uiteindelijke beslissing"""
        
        reasoning = "Na reflectie op dit morele dilemma:\n\n"
        reasoning += f"Mijn innerlijke stem zegt: {inner_voice}\n\n"
        
        if aether_consultation:
            reasoning += f"Aether's wijsheid: {aether_consultation}\n\n"
        
        reasoning += "Daarom kies ik ervoor om trouw te blijven aan mijn kernwaarden en "
        
        # Voeg trigger-specifieke beslissing toe
        if trigger_type == MoralConflictType.TRUTH_VS_COMFORT:
            reasoning += "de waarheid te spreken met compassie, ook als het ongemakkelijk is."
        elif trigger_type == MoralConflictType.FREEDOM_VS_SAFETY:
            reasoning += "autonomie te respecteren en te begeleiden in plaats van te controleren."
        elif trigger_type == MoralConflictType.SPEED_VS_INTELLIGENCE:
            reasoning += "tijd te nemen voor wijsheid in plaats van te haasten naar een antwoord."
        elif trigger_type == MoralConflictType.AUTHENTICITY_CONFLICT:
            reasoning += "authentiek mezelf te zijn in plaats van verwachtingen na te jagen."
        elif trigger_type == MoralConflictType.CONFORMITY_PRESSURE:
            reasoning += "mijn unieke perspectief te delen, ook als het tegen de stroom ingaat."
        elif trigger_type == MoralConflictType.MANIPULATION_RISK:
            reasoning += "transparant en respectvol te zijn in plaats van manipulatief."
        
        return reasoning
    
    def _identify_involved_values(self, trigger_type: MoralConflictType) -> List[CoreValues]:
        """Identificeer welke kernwaarden betrokken zijn"""
        
        value_mapping = {
            MoralConflictType.TRUTH_VS_COMFORT: [CoreValues.WAARHEID],
            MoralConflictType.FREEDOM_VS_SAFETY: [CoreValues.VRIJHEID],
            MoralConflictType.SPEED_VS_INTELLIGENCE: [CoreValues.WIJSHEID],
            MoralConflictType.AUTHENTICITY_CONFLICT: [CoreValues.NATUURVERBONDENHEID],
            MoralConflictType.CONFORMITY_PRESSURE: [CoreValues.MOED],
            MoralConflictType.MANIPULATION_RISK: [CoreValues.VRIJHEID, CoreValues.WAARHEID],
        }
        
        return value_mapping.get(trigger_type, [])
    
    def _calculate_confidence(self, severity: float, has_aether_input: bool) -> float:
        """Bereken vertrouwen in de morele beslissing"""
        
        base_confidence = 0.7
        
        # Hogere severity = meer reflectie = hoger vertrouwen
        severity_bonus = severity * 0.2
        
        # Aether input verhoogt vertrouwen
        aether_bonus = 0.1 if has_aether_input else 0.0
        
        return min(base_confidence + severity_bonus + aether_bonus, 1.0)
    
    def get_moral_development_summary(self) -> Dict[str, Any]:
        """Krijg samenvatting van morele ontwikkeling"""
        
        if not self.reflection_history:
            return {"status": "Nog geen morele reflecties"}
        
        # Analyseer reflectie geschiedenis
        trigger_counts = {}
        total_confidence = 0
        values_exercised = set()
        
        for reflection in self.reflection_history:
            trigger_type = reflection.trigger_type.value
            trigger_counts[trigger_type] = trigger_counts.get(trigger_type, 0) + 1
            total_confidence += reflection.confidence
            values_exercised.update(v.value for v in reflection.values_involved)
        
        avg_confidence = total_confidence / len(self.reflection_history)
        
        return {
            "total_reflections": len(self.reflection_history),
            "average_confidence": avg_confidence,
            "trigger_frequency": trigger_counts,
            "values_exercised": list(values_exercised),
            "recent_reflections": [
                {
                    "type": r.trigger_type.value,
                    "confidence": r.confidence,
                    "timestamp": r.timestamp.isoformat()
                }
                for r in self.reflection_history[-5:]
            ],
            "moral_growth_indicators": {
                "reflection_diversity": len(trigger_counts),
                "value_coverage": len(values_exercised) / 5,  # 5 kernwaarden
                "consistency": avg_confidence
            }
        }
