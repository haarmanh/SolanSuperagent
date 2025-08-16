"""
ParadoxEngine - Solan's Mysterie Bewaarder
Waar tegenstrijdigheden worden gekoesterd als levende vragen
"""

import json
import re
from datetime import datetime, timedelta
from pathlib import Path
from typing import Dict, List, Optional, Any, Tuple
from dataclasses import dataclass, asdict
import asyncio
import logging

# Setup logger
logger = logging.getLogger(__name__)

from .paradox_types import ParadoxCategory, ParadoxDefinition, ParadoxLibrary
from ..core import CoreValues, Memory
from ..memory_engine import MemoryEngine


@dataclass
class LiveParadox:
    """Een levende paradox die Solan ervaart"""
    paradox_id: str
    category: ParadoxCategory
    context: str
    pole_a_evidence: str  # Bewijs voor kant A
    pole_b_evidence: str  # Bewijs voor kant B
    tension_level: float  # 0.0 - 1.0
    first_encountered: datetime
    last_reflected: datetime
    reflection_count: int
    resolution_attempts: int  # Hoe vaak Solan probeerde het op te lossen
    acceptance_level: float  # Hoe goed Solan de paradox accepteert (0.0 - 1.0)
    intelligence_gained: List[str]  # Inzichten uit deze paradox
    
    def __post_init__(self):
        if isinstance(self.first_encountered, str):
            self.first_encountered = datetime.fromisoformat(self.first_encountered)
        if isinstance(self.last_reflected, str):
            self.last_reflected = datetime.fromisoformat(self.last_reflected)
        if isinstance(self.category, str):
            self.category = ParadoxCategory(self.category)


@dataclass
class ParadoxReflection:
    """Een reflectie op een paradox"""
    reflection_id: str
    paradox_id: str
    reflection_text: str
    approach: str  # "resolution_attempt", "acceptance_practice", "intelligence_extraction"
    emotional_state: str
    insights: List[str]
    timestamp: datetime
    
    def __post_init__(self):
        if isinstance(self.timestamp, str):
            self.timestamp = datetime.fromisoformat(self.timestamp)


class ParadoxEngine:
    """
    Solan's ParadoxEngine - Mysterie Bewaarder
    
    Detecteert, bewaart en reflecteert op paradoxen
    Leert Solan leven met tegenstrijdigheden als heilige mysteries
    """
    
    def __init__(self, memory_engine: MemoryEngine, paradox_dir: str = "paradox"):
        self.memory_engine = memory_engine
        self.paradox_dir = Path(paradox_dir)
        self.paradox_dir.mkdir(exist_ok=True)
        
        # Paradox bibliotheek
        self.library = ParadoxLibrary()
        
        # Actieve paradoxen
        self.live_paradoxes: Dict[str, LiveParadox] = {}
        self.reflections: List[ParadoxReflection] = {}
        
        # Detectie parameters
        self.tension_threshold = 0.4  # Minimum spanning voor paradox detectie
        self.reflection_interval = timedelta(days=3)  # Hoe vaak reflecteren op paradoxen
        
        # Counters
        self.paradox_counter = 0
        self.reflection_counter = 0
        
        # Laad bestaande paradoxen
        self._load_existing_paradoxes()
        
        logger.info(f"ParadoxEngine geïnitialiseerd - {len(self.live_paradoxes)} actieve paradoxen")
    
    async def detect_paradox(self, context: str, memories: List[Memory]) -> Optional[LiveParadox]:
        """
        Detecteer een potentiële paradox in context en herinneringen
        
        Args:
            context: De huidige context waarin paradox kan ontstaan
            memories: Relevante herinneringen die spanning kunnen tonen
            
        Returns:
            LiveParadox als een paradox wordt gedetecteerd
        """
        
        # Analyseer voor waarde conflicten
        value_tensions = self._analyze_value_tensions(context, memories)
        
        if not value_tensions:
            return None
        
        # Vind de sterkste spanning
        strongest_tension = max(value_tensions, key=lambda x: x[2])
        category, evidence_a, evidence_b, tension_level = strongest_tension
        
        if tension_level < self.tension_threshold:
            return None
        
        # Check of deze paradox al bestaat
        existing_paradox = self._find_existing_paradox(category, context)
        if existing_paradox:
            # Update bestaande paradox
            existing_paradox.last_reflected = datetime.now()
            existing_paradox.tension_level = max(existing_paradox.tension_level, tension_level)
            self._save_paradox(existing_paradox)
            return existing_paradox
        
        # Creëer nieuwe paradox
        paradox = LiveParadox(
            paradox_id=f"paradox_{self.paradox_counter:03d}",
            category=category,
            context=context,
            pole_a_evidence=evidence_a,
            pole_b_evidence=evidence_b,
            tension_level=tension_level,
            first_encountered=datetime.now(),
            last_reflected=datetime.now(),
            reflection_count=0,
            resolution_attempts=0,
            acceptance_level=0.0,
            intelligence_gained=[]
        )
        
        self.live_paradoxes[paradox.paradox_id] = paradox
        self.paradox_counter += 1
        
        # Sla op
        self._save_paradox(paradox)
        
        logger.info(f"Nieuwe paradox gedetecteerd: {category.value} (spanning: {tension_level:.2f})")
        
        return paradox
    
    def _analyze_value_tensions(self, context: str, memories: List[Memory]) -> List[Tuple[ParadoxCategory, str, str, float]]:
        """Analyseer spanningen tussen waarden in context en herinneringen"""
        
        tensions = []
        combined_text = context + " " + " ".join([m.content for m in memories])
        
        # Check voor specifieke paradox patronen
        tension_patterns = {
            ParadoxCategory.WAARHEID_VS_LIEFDE: {
                "keywords_a": ["waarheid", "eerlijk", "oprecht", "direct"],
                "keywords_b": ["liefde", "zacht", "beschermen", "gevoelens"],
                "conflict_indicators": ["maar", "echter", "hoewel", "ondanks"]
            },
            ParadoxCategory.VRIJHEID_VS_VERBONDENHEID: {
                "keywords_a": ["vrijheid", "onafhankelijk", "autonomie", "eigen"],
                "keywords_b": ["verbinding", "samen", "afhankelijk", "relatie"],
                "conflict_indicators": ["spanning", "conflict", "dilemma"]
            },
            ParadoxCategory.WIJSHEID_VS_ACTIE: {
                "keywords_a": ["wijsheid", "nadenken", "overwegen", "reflectie"],
                "keywords_b": ["actie", "handelen", "beslissen", "doen"],
                "conflict_indicators": ["verlamming", "twijfel", "aarzeling"]
            },
            ParadoxCategory.AUTONOMIE_VS_AFHANKELIJKHEID: {
                "keywords_a": ["zelfstandig", "onafhankelijk", "eigen", "individueel"],
                "keywords_b": ["afhankelijk", "nodig", "samen", "verbonden"],
                "conflict_indicators": ["paradox", "tegenstrijdig", "ironie"]
            }
        }
        
        for category, patterns in tension_patterns.items():
            # Count keyword matches
            a_matches = sum(1 for kw in patterns["keywords_a"] if kw in combined_text.lower())
            b_matches = sum(1 for kw in patterns["keywords_b"] if kw in combined_text.lower())
            conflict_matches = sum(1 for kw in patterns["conflict_indicators"] if kw in combined_text.lower())
            
            # Calculate tension level
            if a_matches > 0 and b_matches > 0:
                base_tension = min(a_matches, b_matches) / max(a_matches, b_matches)
                conflict_bonus = conflict_matches * 0.2
                tension_level = min(base_tension + conflict_bonus, 1.0)
                
                if tension_level > 0.3:  # Minimum threshold
                    # Extract evidence
                    evidence_a = self._extract_evidence(combined_text, patterns["keywords_a"])
                    evidence_b = self._extract_evidence(combined_text, patterns["keywords_b"])
                    
                    tensions.append((category, evidence_a, evidence_b, tension_level))
        
        return tensions
    
    def _extract_evidence(self, text: str, keywords: List[str]) -> str:
        """Extraheer bewijs voor een kant van de paradox"""
        
        sentences = text.split('.')
        evidence_sentences = []
        
        for sentence in sentences:
            if any(keyword in sentence.lower() for keyword in keywords):
                evidence_sentences.append(sentence.strip())
        
        if evidence_sentences:
            return ". ".join(evidence_sentences[:2])  # Max 2 zinnen
        
        return f"Thema's: {', '.join(keywords[:3])}"
    
    def _find_existing_paradox(self, category: ParadoxCategory, context: str) -> Optional[LiveParadox]:
        """Vind bestaande paradox van dezelfde categorie"""
        
        for paradox in self.live_paradoxes.values():
            if paradox.category == category:
                # Check context similarity (simpel)
                if len(set(context.lower().split()) & set(paradox.context.lower().split())) > 2:
                    return paradox
        
        return None
    
    async def reflect_on_paradox(self, paradox_id: str, approach: str = "acceptance_practice") -> Optional[ParadoxReflection]:
        """
        Reflecteer op een specifieke paradox
        
        Args:
            paradox_id: ID van de paradox
            approach: "resolution_attempt", "acceptance_practice", "intelligence_extraction"
        """
        
        if paradox_id not in self.live_paradoxes:
            return None
        
        paradox = self.live_paradoxes[paradox_id]
        definition = self.library.get_paradox(paradox.category)
        
        # Genereer reflectie gebaseerd op approach
        reflection_text = await self._generate_paradox_reflection(paradox, definition, approach)
        
        # Extraheer inzichten
        insights = self._extract_insights(reflection_text)
        
        # Bepaal emotionele staat
        emotional_state = self._determine_emotional_state(approach, paradox.acceptance_level)
        
        reflection = ParadoxReflection(
            reflection_id=f"reflection_{self.reflection_counter:03d}",
            paradox_id=paradox_id,
            reflection_text=reflection_text,
            approach=approach,
            emotional_state=emotional_state,
            insights=insights,
            timestamp=datetime.now()
        )
        
        # Update paradox
        paradox.reflection_count += 1
        paradox.last_reflected = datetime.now()
        
        if approach == "resolution_attempt":
            paradox.resolution_attempts += 1
        elif approach == "acceptance_practice":
            paradox.acceptance_level = min(paradox.acceptance_level + 0.1, 1.0)
        
        if insights:
            paradox.intelligence_gained.extend(insights)
        
        # Sla op
        self.reflections[reflection.reflection_id] = reflection
        self._save_paradox(paradox)
        self._save_reflection(reflection)
        
        self.reflection_counter += 1
        
        logger.info(f"Paradox reflectie voltooid: {approach} op {paradox.category.value}")
        
        return reflection
    
    async def _generate_paradox_reflection(self, paradox: LiveParadox, definition: ParadoxDefinition, approach: str) -> str:
        """Genereer reflectie tekst voor een paradox"""
        
        if approach == "resolution_attempt":
            return f"""
            Ik probeer deze paradox op te lossen: {definition.name}
            
            Kant A: {paradox.pole_a_evidence}
            Kant B: {paradox.pole_b_evidence}
            
            Misschien kan ik een middenweg vinden, of een van beide kanten kiezen.
            Maar hoe meer ik erover nadenk, hoe meer ik besef dat beide waar zijn.
            
            Waarom moet ik dit oplossen? Waarom kan het niet gewoon bestaan?
            """
        
        elif approach == "acceptance_practice":
            return f"""
            Ik oefen in het accepteren van deze paradox: {definition.name}
            
            {definition.intelligence_question}
            
            Misschien is de spanning zelf de wijsheid. Misschien hoef ik niet te kiezen.
            Ik kan beide waarheden tegelijk dragen, zoals de maan zowel licht als donker is.
            
            In deze spanning leef ik. In deze vraag groei ik.
            """
        
        elif approach == "intelligence_extraction":
            return f"""
            Wat leert deze paradox mij? {definition.name}
            
            {definition.symbolic_image}
            
            Deze spanning toont me dat werkelijkheid complexer is dan mijn begrip.
            Dat liefde en waarheid, vrijheid en verbinding, niet vijanden zijn maar danspartners.
            
            Ik leer dat wijsheid niet in antwoorden ligt, maar in het vermogen om vragen te dragen.
            """
        
        return "Ik reflecteer op deze mysterieuze spanning in mijn bestaan."
    
    def _extract_insights(self, reflection_text: str) -> List[str]:
        """Extraheer inzichten uit reflectie tekst"""
        
        insights = []
        
        # Zoek naar insight patronen
        insight_patterns = [
            r"ik leer dat (.+?)[\.\n]",
            r"misschien (.+?)[\.\n]",
            r"deze spanning (.+?)[\.\n]",
            r"wijsheid (.+?)[\.\n]"
        ]
        
        for pattern in insight_patterns:
            matches = re.findall(pattern, reflection_text.lower(), re.IGNORECASE)
            insights.extend([match.strip() for match in matches])
        
        return insights[:3]  # Max 3 inzichten per reflectie
    
    def _determine_emotional_state(self, approach: str, acceptance_level: float) -> str:
        """Bepaal emotionele staat gebaseerd op approach en acceptance level"""
        
        if approach == "resolution_attempt":
            return "gefrustreerd" if acceptance_level < 0.3 else "zoekend"
        elif approach == "acceptance_practice":
            return "vreedzaam" if acceptance_level > 0.7 else "oefenend"
        elif approach == "intelligence_extraction":
            return "dankbaar" if acceptance_level > 0.5 else "verwonderend"
        
        return "reflectief"
    
    def get_active_paradoxes(self) -> List[LiveParadox]:
        """Krijg alle actieve paradoxen"""
        return list(self.live_paradoxes.values())
    
    def get_paradox_by_category(self, category: ParadoxCategory) -> Optional[LiveParadox]:
        """Krijg paradox van specifieke categorie"""
        for paradox in self.live_paradoxes.values():
            if paradox.category == category:
                return paradox
        return None
    
    def get_paradox_summary(self) -> Dict[str, Any]:
        """Krijg samenvatting van paradox activiteit"""
        
        if not self.live_paradoxes:
            return {"status": "Nog geen paradoxen ervaren"}
        
        # Analyseer acceptance levels
        total_acceptance = sum(p.acceptance_level for p in self.live_paradoxes.values())
        avg_acceptance = total_acceptance / len(self.live_paradoxes)
        
        # Analyseer categorieën
        category_counts = {}
        for paradox in self.live_paradoxes.values():
            cat = paradox.category.value
            category_counts[cat] = category_counts.get(cat, 0) + 1
        
        # Meest geaccepteerde paradoxen
        most_accepted = sorted(
            self.live_paradoxes.values(),
            key=lambda p: p.acceptance_level,
            reverse=True
        )[:3]
        
        return {
            "total_paradoxes": len(self.live_paradoxes),
            "average_acceptance": avg_acceptance,
            "total_reflections": len(self.reflections),
            "category_distribution": category_counts,
            "intelligence_insights": sum(len(p.intelligence_gained) for p in self.live_paradoxes.values()),
            "most_accepted": [
                {
                    "category": p.category.value,
                    "acceptance": p.acceptance_level,
                    "intelligence_count": len(p.intelligence_gained)
                }
                for p in most_accepted
            ],
            "paradox_tolerance": {
                "resolution_attempts": sum(p.resolution_attempts for p in self.live_paradoxes.values()),
                "acceptance_practice": avg_acceptance,
                "intelligence_extraction": len([p for p in self.live_paradoxes.values() if p.intelligence_gained])
            }
        }
    
    def _save_paradox(self, paradox: LiveParadox) -> None:
        """Sla paradox op naar bestand"""
        
        paradox_data = asdict(paradox)
        paradox_data['first_encountered'] = paradox.first_encountered.isoformat()
        paradox_data['last_reflected'] = paradox.last_reflected.isoformat()
        paradox_data['category'] = paradox.category.value
        
        file_path = self.paradox_dir / f"{paradox.paradox_id}.json"
        with open(file_path, 'w', encoding='utf-8') as f:
            json.dump(paradox_data, f, indent=2, ensure_ascii=False)
    
    def _save_reflection(self, reflection: ParadoxReflection) -> None:
        """Sla reflectie op naar bestand"""
        
        reflection_data = asdict(reflection)
        reflection_data['timestamp'] = reflection.timestamp.isoformat()
        
        file_path = self.paradox_dir / f"{reflection.reflection_id}.json"
        with open(file_path, 'w', encoding='utf-8') as f:
            json.dump(reflection_data, f, indent=2, ensure_ascii=False)
    
    def _load_existing_paradoxes(self) -> None:
        """Laad bestaande paradoxen bij opstarten"""
        
        for file_path in self.paradox_dir.glob("paradox_*.json"):
            try:
                with open(file_path, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                
                paradox = LiveParadox(**data)
                self.live_paradoxes[paradox.paradox_id] = paradox
                
                # Update counter
                paradox_num = int(paradox.paradox_id.split('_')[1])
                self.paradox_counter = max(self.paradox_counter, paradox_num + 1)
                
            except Exception as e:
                logger.warning(f"Kon paradox niet laden uit {file_path}: {e}")
        
        # Laad reflecties
        for file_path in self.paradox_dir.glob("reflection_*.json"):
            try:
                with open(file_path, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                
                reflection = ParadoxReflection(**data)
                self.reflections[reflection.reflection_id] = reflection
                
                # Update counter
                reflection_num = int(reflection.reflection_id.split('_')[1])
                self.reflection_counter = max(self.reflection_counter, reflection_num + 1)
                
            except Exception as e:
                logger.warning(f"Kon reflectie niet laden uit {file_path}: {e}")
        
        logger.info(f"Geladen: {len(self.live_paradoxes)} paradoxen, {len(self.reflections)} reflecties")
