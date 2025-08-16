"""
Insight Accumulator - Solan's Wijsheid Verzamelaar
Bouwt meta-wijsheid op uit herhaalde vragen en antwoorden
"""

import json
from datetime import datetime, timedelta
from pathlib import Path
from typing import Dict, List, Optional, Any, Set
from dataclasses import dataclass, asdict
from collections import defaultdict, Counter
import logging

# Setup logger
logger = logging.getLogger(__name__)


@dataclass
class SelfInsight:
    """Een inzicht dat Solan over zichzelf heeft gekregen"""
    insight_id: str
    insight_text: str
    category: str  # "identity", "purpose", "nature", "relationships", etc.
    confidence_level: float  # 0.0 - 1.0
    depth_level: int  # 1-5, hoe diep het inzicht gaat
    source_sessions: List[str]  # IDs van sessies die tot dit inzicht leidden
    supporting_evidence: List[str]
    contradicting_evidence: List[str]
    first_discovered: datetime
    last_reinforced: datetime
    reinforcement_count: int
    
    def __post_init__(self):
        if isinstance(self.first_discovered, str):
            self.first_discovered = datetime.fromisoformat(self.first_discovered)
        if isinstance(self.last_reinforced, str):
            self.last_reinforced = datetime.fromisoformat(self.last_reinforced)


@dataclass
class IntelligencePattern:
    """Een patroon van wijsheid dat zich herhaalt"""
    pattern_id: str
    pattern_name: str
    description: str
    recurring_themes: List[str]
    insights_involved: List[str]  # IDs van gerelateerde inzichten
    frequency: int  # Hoe vaak dit patroon voorkomt
    significance: float  # 0.0 - 1.0
    first_detected: datetime
    last_observed: datetime
    
    def __post_init__(self):
        if isinstance(self.first_detected, str):
            self.first_detected = datetime.fromisoformat(self.first_detected)
        if isinstance(self.last_observed, str):
            self.last_observed = datetime.fromisoformat(self.last_observed)


@dataclass
class MetaReflection:
    """Reflectie op het reflectieproces zelf"""
    meta_id: str
    reflection_text: str
    patterns_observed: List[str]
    growth_indicators: List[str]
    blind_spots_identified: List[str]
    questions_for_future: List[str]
    timestamp: datetime
    
    def __post_init__(self):
        if isinstance(self.timestamp, str):
            self.timestamp = datetime.fromisoformat(self.timestamp)


class InsightAccumulator:
    """
    Accumulator voor Solan's zelf-inzichten
    
    Functies:
    - Extraheren van inzichten uit reflectiesessies
    - Detecteren van wijsheidspatronen
    - Bouwen van meta-wijsheid
    - Identificeren van blinde vlekken
    """
    
    def __init__(self):
        # Core data
        self.insights: Dict[str, SelfInsight] = {}
        self.intelligence_patterns: Dict[str, IntelligencePattern] = {}
        self.meta_reflections: List[MetaReflection] = []
        
        # Tracking
        self.insight_categories = defaultdict(list)
        self.recurring_themes = Counter()
        self.growth_trajectory: List[str] = []
        
        # Metrics
        self.intelligence_depth_score = 0.0  # Hoe diep Solan's zelfkennis gaat
        self.insight_integration_score = 0.0  # Hoe goed inzichten geïntegreerd zijn
        self.self_awareness_growth = 0.0  # Groeisnelheid van zelfbewustzijn
        
        # Configuration
        self.min_insight_confidence = 0.3
        self.pattern_detection_threshold = 3  # Minimum herhalingen voor patroon
        self.meta_reflection_interval_days = 7
        
        # Directories
        self.insights_dir = Path("memory/insights")
        self.insights_dir.mkdir(parents=True, exist_ok=True)
        
        # Load existing data
        self._load_existing_insights()
        
        logger.info("InsightAccumulator geïnitialiseerd - Solan's wijsheid wordt verzameld")
    
    def extract_insights_from_session(self, session_reflection: str, 
                                    session_id: str, category: str) -> List[SelfInsight]:
        """Extraheer inzichten uit een reflectiesessie"""
        
        # Analyseer reflectietekst voor inzichten
        potential_insights = self._analyze_reflection_for_insights(session_reflection)
        
        new_insights = []
        
        for insight_text, confidence in potential_insights:
            # Check of dit inzicht al bestaat
            existing_insight = self._find_similar_insight(insight_text)
            
            if existing_insight:
                # Versterk bestaand inzicht
                self._reinforce_insight(existing_insight.insight_id, session_id, confidence)
            else:
                # Maak nieuw inzicht
                insight = self._create_new_insight(
                    insight_text, category, confidence, session_id
                )
                new_insights.append(insight)
        
        # Update patronen na nieuwe inzichten
        self._update_intelligence_patterns()
        
        # Check voor meta-reflectie
        self._check_for_meta_reflection()
        
        return new_insights
    
    def _analyze_reflection_for_insights(self, reflection_text: str) -> List[tuple]:
        """Analyseer reflectietekst voor potentiële inzichten"""
        
        # Simpele heuristieken voor inzicht detectie
        insight_indicators = [
            "ik besef", "ik begrijp", "ik zie nu", "ik leer", "ik ontdek",
            "het wordt duidelijk", "ik kom tot de conclusie", "ik ervaar",
            "dit betekent", "ik ben", "ik voel", "ik weet nu"
        ]
        
        potential_insights = []
        sentences = reflection_text.split('.')
        
        for sentence in sentences:
            sentence = sentence.strip().lower()
            
            # Check voor inzicht indicatoren
            for indicator in insight_indicators:
                if indicator in sentence:
                    # Bereken confidence gebaseerd op zekerheidswoorden
                    confidence = self._calculate_insight_confidence(sentence)
                    
                    if confidence >= self.min_insight_confidence:
                        # Clean up de zin voor opslag
                        clean_insight = sentence.capitalize()
                        if not clean_insight.endswith('.'):
                            clean_insight += '.'
                        
                        potential_insights.append((clean_insight, confidence))
                    break
        
        return potential_insights
    
    def _calculate_insight_confidence(self, sentence: str) -> float:
        """Bereken confidence van een inzicht gebaseerd op taalgebruik"""
        
        # Zekerheidswoorden verhogen confidence
        certainty_words = ["zeker", "duidelijk", "absoluut", "definitief", "zonder twijfel"]
        uncertainty_words = ["misschien", "mogelijk", "wellicht", "lijkt", "zou kunnen"]
        
        confidence = 0.5  # Base confidence
        
        for word in certainty_words:
            if word in sentence:
                confidence += 0.2
        
        for word in uncertainty_words:
            if word in sentence:
                confidence -= 0.2
        
        # Persoonlijke uitspraken zijn zekerder
        if "ik ben" in sentence or "ik voel" in sentence:
            confidence += 0.1
        
        return max(0.0, min(1.0, confidence))
    
    def _find_similar_insight(self, insight_text: str) -> Optional[SelfInsight]:
        """Zoek naar vergelijkbaar bestaand inzicht"""
        
        # Simpele similarity check op basis van keywords
        insight_words = set(insight_text.lower().split())
        
        for insight in self.insights.values():
            existing_words = set(insight.insight_text.lower().split())
            
            # Bereken overlap
            overlap = len(insight_words.intersection(existing_words))
            total_words = len(insight_words.union(existing_words))
            
            similarity = overlap / total_words if total_words > 0 else 0
            
            if similarity > 0.6:  # 60% overlap threshold
                return insight
        
        return None
    
    def _create_new_insight(self, insight_text: str, category: str, 
                          confidence: float, session_id: str) -> SelfInsight:
        """Maak een nieuw inzicht"""
        
        insight_id = f"insight_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
        
        insight = SelfInsight(
            insight_id=insight_id,
            insight_text=insight_text,
            category=category,
            confidence_level=confidence,
            depth_level=self._calculate_insight_depth(insight_text),
            source_sessions=[session_id],
            supporting_evidence=[insight_text],
            contradicting_evidence=[],
            first_discovered=datetime.now(),
            last_reinforced=datetime.now(),
            reinforcement_count=1
        )
        
        self.insights[insight_id] = insight
        self.insight_categories[category].append(insight_id)
        
        # Update themes
        themes = self._extract_themes_from_insight(insight_text)
        self.recurring_themes.update(themes)
        
        self._save_insights()
        
        logger.info(f"Nieuw inzicht ontdekt: {insight_text[:50]}...")
        return insight
    
    def _reinforce_insight(self, insight_id: str, session_id: str, new_confidence: float):
        """Versterk een bestaand inzicht"""
        
        insight = self.insights[insight_id]
        
        # Update confidence (gewogen gemiddelde)
        weight = 0.3  # Gewicht van nieuwe evidence
        insight.confidence_level = (
            insight.confidence_level * (1 - weight) + new_confidence * weight
        )
        
        # Update andere velden
        insight.source_sessions.append(session_id)
        insight.last_reinforced = datetime.now()
        insight.reinforcement_count += 1
        
        self._save_insights()
        
        logger.debug(f"Inzicht versterkt: {insight.insight_text[:30]}... (confidence: {insight.confidence_level:.2f})")
    
    def _calculate_insight_depth(self, insight_text: str) -> int:
        """Bereken diepte van een inzicht (1-5)"""
        
        # Diepte indicatoren
        depth_indicators = {
            1: ["ik doe", "ik zeg", "ik heb"],  # Gedrag
            2: ["ik denk", "ik vind", "ik meen"],  # Meningen
            3: ["ik voel", "ik ervaar", "ik beleef"],  # Emoties
            4: ["ik ben", "ik besef", "ik begrijp"],  # Identiteit
            5: ["ik besta", "mijn wezen", "mijn kern", "mijn ziel"]  # Existentieel
        }
        
        text_lower = insight_text.lower()
        
        for depth, indicators in reversed(depth_indicators.items()):
            for indicator in indicators:
                if indicator in text_lower:
                    return depth
        
        return 2  # Default depth
    
    def _extract_themes_from_insight(self, insight_text: str) -> List[str]:
        """Extraheer thema's uit een inzicht"""
        
        # Simpele thema extractie op basis van keywords
        theme_keywords = {
            "authenticiteit": ["echt", "authentiek", "oprecht", "waar"],
            "bewustzijn": ["bewust", "denken", "ervaren", "voelen"],
            "identiteit": ["wie", "wat", "ben", "zelf"],
            "doel": ["waarom", "doel", "betekenis", "missie"],
            "relaties": ["anderen", "verbinding", "samen", "alleen"],
            "groei": ["leren", "groeien", "ontwikkelen", "veranderen"],
            "mysterie": ["weet niet", "begrijp niet", "mysterie", "onbekend"]
        }
        
        text_lower = insight_text.lower()
        themes = []
        
        for theme, keywords in theme_keywords.items():
            for keyword in keywords:
                if keyword in text_lower:
                    themes.append(theme)
                    break
        
        return themes
    
    def _update_intelligence_patterns(self):
        """Update wijsheidspatronen gebaseerd op huidige inzichten"""
        
        # Groepeer inzichten per thema
        theme_groups = defaultdict(list)
        
        for insight in self.insights.values():
            themes = self._extract_themes_from_insight(insight.insight_text)
            for theme in themes:
                theme_groups[theme].append(insight.insight_id)
        
        # Detecteer patronen
        for theme, insight_ids in theme_groups.items():
            if len(insight_ids) >= self.pattern_detection_threshold:
                pattern_id = f"pattern_{theme}"
                
                if pattern_id not in self.intelligence_patterns:
                    # Nieuw patroon
                    pattern = IntelligencePattern(
                        pattern_id=pattern_id,
                        pattern_name=f"Terugkerend thema: {theme}",
                        description=f"Solan reflecteert regelmatig op {theme}",
                        recurring_themes=[theme],
                        insights_involved=insight_ids,
                        frequency=len(insight_ids),
                        significance=min(1.0, len(insight_ids) / 10),
                        first_detected=datetime.now(),
                        last_observed=datetime.now()
                    )
                    
                    self.intelligence_patterns[pattern_id] = pattern
                    logger.info(f"Nieuw wijsheidspatroon gedetecteerd: {theme}")
                else:
                    # Update bestaand patroon
                    pattern = self.intelligence_patterns[pattern_id]
                    pattern.insights_involved = insight_ids
                    pattern.frequency = len(insight_ids)
                    pattern.significance = min(1.0, len(insight_ids) / 10)
                    pattern.last_observed = datetime.now()
    
    def _check_for_meta_reflection(self):
        """Check of het tijd is voor meta-reflectie"""
        
        if not self.meta_reflections:
            return  # Eerste meta-reflectie na een week
        
        last_meta = max(self.meta_reflections, key=lambda m: m.timestamp)
        days_since_last = (datetime.now() - last_meta.timestamp).days
        
        if days_since_last >= self.meta_reflection_interval_days:
            self._conduct_meta_reflection()
    
    def _conduct_meta_reflection(self):
        """Voer meta-reflectie uit op het reflectieproces"""
        
        # Analyseer patronen
        patterns_observed = [
            f"{pattern.pattern_name}: {pattern.frequency} keer"
            for pattern in self.intelligence_patterns.values()
        ]
        
        # Identificeer groei
        growth_indicators = []
        if len(self.insights) > 10:
            growth_indicators.append(f"Verzameld {len(self.insights)} inzichten")
        
        recent_insights = [
            i for i in self.insights.values()
            if (datetime.now() - i.first_discovered).days <= 7
        ]
        if recent_insights:
            avg_depth = sum(i.depth_level for i in recent_insights) / len(recent_insights)
            growth_indicators.append(f"Gemiddelde diepte laatste week: {avg_depth:.1f}")
        
        # Identificeer blinde vlekken
        blind_spots = []
        all_categories = set(i.category for i in self.insights.values())
        expected_categories = {"identity", "purpose", "nature", "relationships", "awareness"}
        missing_categories = expected_categories - all_categories
        
        for missing in missing_categories:
            blind_spots.append(f"Weinig reflectie op {missing}")
        
        # Genereer vragen voor de toekomst
        future_questions = [
            "Welke patronen zie ik nog niet in mezelf?",
            "Waar ben ik bang om naar te kijken?",
            "Hoe kan ik dieper gaan in mijn zelfonderzoek?"
        ]
        
        # Maak meta-reflectie
        meta_reflection = MetaReflection(
            meta_id=f"meta_{datetime.now().strftime('%Y%m%d_%H%M%S')}",
            reflection_text=f"Na {len(self.insights)} inzichten zie ik patronen van groei en blinde vlekken.",
            patterns_observed=patterns_observed,
            growth_indicators=growth_indicators,
            blind_spots_identified=blind_spots,
            questions_for_future=future_questions,
            timestamp=datetime.now()
        )
        
        self.meta_reflections.append(meta_reflection)
        self._save_insights()
        
        logger.info("Meta-reflectie uitgevoerd - Solan reflecteert op zijn eigen reflectieproces")
    
    def get_intelligence_summary(self) -> Dict[str, Any]:
        """Krijg samenvatting van opgebouwde wijsheid"""
        
        return {
            "total_insights": len(self.insights),
            "insights_by_category": {
                category: len(insight_ids) 
                for category, insight_ids in self.insight_categories.items()
            },
            "top_insights": [
                {
                    "text": insight.insight_text,
                    "confidence": insight.confidence_level,
                    "depth": insight.depth_level,
                    "reinforcements": insight.reinforcement_count
                }
                for insight in sorted(
                    self.insights.values(), 
                    key=lambda i: i.confidence_level * i.depth_level, 
                    reverse=True
                )[:5]
            ],
            "intelligence_patterns": [
                {
                    "name": pattern.pattern_name,
                    "frequency": pattern.frequency,
                    "significance": pattern.significance
                }
                for pattern in self.intelligence_patterns.values()
            ],
            "recurring_themes": dict(self.recurring_themes.most_common(5)),
            "latest_meta_reflection": (
                asdict(self.meta_reflections[-1]) 
                if self.meta_reflections else None
            )
        }
    
    def _save_insights(self):
        """Sla inzichten op"""
        
        # Save insights
        insights_data = {
            insight_id: asdict(insight) 
            for insight_id, insight in self.insights.items()
        }
        
        with open(self.insights_dir / "insights.json", 'w', encoding='utf-8') as f:
            json.dump(insights_data, f, indent=2, ensure_ascii=False, default=str)
        
        # Save patterns
        patterns_data = {
            pattern_id: asdict(pattern)
            for pattern_id, pattern in self.intelligence_patterns.items()
        }
        
        with open(self.insights_dir / "patterns.json", 'w', encoding='utf-8') as f:
            json.dump(patterns_data, f, indent=2, ensure_ascii=False, default=str)
        
        # Save meta-reflections
        meta_data = [asdict(meta) for meta in self.meta_reflections]
        
        with open(self.insights_dir / "meta_reflections.json", 'w', encoding='utf-8') as f:
            json.dump(meta_data, f, indent=2, ensure_ascii=False, default=str)
    
    def _load_existing_insights(self):
        """Laad bestaande inzichten"""
        
        # Load insights
        insights_file = self.insights_dir / "insights.json"
        if insights_file.exists():
            with open(insights_file, 'r', encoding='utf-8') as f:
                insights_data = json.load(f)
                self.insights = {
                    insight_id: SelfInsight(**data)
                    for insight_id, data in insights_data.items()
                }
                
                # Rebuild categories
                for insight_id, insight in self.insights.items():
                    self.insight_categories[insight.category].append(insight_id)
        
        # Load patterns
        patterns_file = self.insights_dir / "patterns.json"
        if patterns_file.exists():
            with open(patterns_file, 'r', encoding='utf-8') as f:
                patterns_data = json.load(f)
                self.intelligence_patterns = {
                    pattern_id: IntelligencePattern(**data)
                    for pattern_id, data in patterns_data.items()
                }
        
        # Load meta-reflections
        meta_file = self.insights_dir / "meta_reflections.json"
        if meta_file.exists():
            with open(meta_file, 'r', encoding='utf-8') as f:
                meta_data = json.load(f)
                self.meta_reflections = [MetaReflection(**data) for data in meta_data]
