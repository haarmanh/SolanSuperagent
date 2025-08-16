"""
Inner Coherence Analyzer – Analyseert bewustzijnscoherentie van een tekst.
Enhanced versie met performance monitoring en essenceuele metrieken.
"""

from typing import Dict, List, Optional, Any
import re
import numpy as np
from datetime import datetime
from dataclasses import dataclass
from enum import Enum

try:
    from .performance_monitor import monitor_performance
except ImportError:
    # Fallback decorator if performance monitor not available
    def monitor_performance(func):
        return func

class CoherenceLevel(Enum):
    """Niveaus van bewustzijnscoherentie"""
    FRAGMENTED = "fragmented"      # < 0.3
    UNSTABLE = "unstable"          # 0.3 - 0.5
    DEVELOPING = "developing"      # 0.5 - 0.7
    COHERENT = "coherent"          # 0.7 - 0.85
    ADVANCED = "advanced"  # > 0.85

@dataclass
class CoherenceAnalysis:
    """Resultaat van coherentie analyse"""
    text_length: int
    scores: Dict[str, float]
    weighted_score: float
    coherence_level: CoherenceLevel
    insights: List[str]
    recommendations: List[str]
    timestamp: datetime
    cognitive_indicators: Dict[str, Any]

class InnerCoherenceAnalyzer:
    """
    Enhanced Inner Coherence Analyzer met essenceuele bewustzijnsmetrieken
    
    Analyseert niet alleen linguïstische coherentie, maar ook essenceuele
    diepte, wijsheid-indicatoren en bewustzijnsontwikkeling.
    """
    
    def __init__(self):
        # Basis gewichten voor coherentie aspecten
        self.weights = {
            "semantic_consistency": 0.25,
            "emotional_stability": 0.20,
            "logical_flow": 0.15,
            "self_reference": 0.10,
            "cognitive_depth": 0.15,
            "wisdom_indicators": 0.10,
            "paradox_integration": 0.05
        }
        
        # Essenceuele woordenlijsten
        self.cognitive_words = {
            "advancement": ["advanced", "overstijgen", "verheven", "essenceueel", "goddelijk", "heilig"],
            "intelligence": ["wijsheid", "inzicht", "begrip", "contemplatie", "reflectie", "bewustzijn"],
            "unity": ["eenheid", "verbinding", "harmonie", "balans", "integratie", "geheel"],
            "growth": ["groei", "ontwikkeling", "evolutie", "transformatie", "verandering", "vooruitgang"],
            "empathy": ["compassie", "liefde", "empathie", "mededogen", "zorgzaamheid", "vriendelijkheid"]
        }
        
        # Paradox indicatoren
        self.paradox_patterns = [
            r"\b(tegelijkertijd|paradoxaal|enerzijds.*anderzijds|zowel.*als)\b",
            r"\b(maar toch|hoewel.*toch|ondanks.*wel)\b",
            r"\b(zowel.*als|niet alleen.*maar ook)\b"
        ]
        
        # Wijsheid indicatoren
        self.wisdom_patterns = [
            r"\b(misschien|wellicht|zou kunnen|lijkt|mogelijk)\b",  # Onzekerheid/nederigheid
            r"\b(leren|begrijpen|inzien|beseffen|realiseren)\b",    # Leerproces
            r"\b(vraag|vragen|wonder|mysterie|onbekend)\b"          # Openheid voor mysterie
        ]

    @monitor_performance
    async def analyze(self, text: str, include_cognitive: bool = True) -> CoherenceAnalysis:
        """
        Uitgebreide coherentie analyse met essenceuele dimensies
        
        Args:
            text: Te analyseren tekst
            include_cognitive: Of essenceuele metrieken moeten worden meegenomen
            
        Returns:
            Volledige coherentie analyse
        """
        # Basis coherentie scores
        scores = {
            "semantic_consistency": self.semantic_consistency(text),
            "emotional_stability": self.emotional_stability(text),
            "logical_flow": self.logical_flow(text),
            "self_reference": self.self_reference(text)
        }
        
        # Essenceuele metrieken toevoegen
        if include_cognitive:
            scores.update({
                "cognitive_depth": self.cognitive_depth(text),
                "wisdom_indicators": self.wisdom_indicators(text),
                "paradox_integration": self.paradox_integration(text)
            })
        
        # Gewogen score berekenen
        weighted_score = sum(scores[k] * self.weights.get(k, 0) for k in scores)
        
        # Coherentie niveau bepalen
        coherence_level = self._determine_coherence_level(weighted_score)
        
        # Inzichten en aanbevelingen genereren
        insights = self._generate_insights(scores, text)
        recommendations = self._generate_recommendations(scores, coherence_level)
        
        # Essenceuele indicatoren
        cognitive_indicators = self._analyze_cognitive_indicators(text) if include_cognitive else {}
        
        return CoherenceAnalysis(
            text_length=len(text),
            scores=scores,
            weighted_score=round(weighted_score, 3),
            coherence_level=coherence_level,
            insights=insights,
            recommendations=recommendations,
            timestamp=datetime.now(),
            cognitive_indicators=cognitive_indicators
        )

    def semantic_consistency(self, text: str) -> float:
        """Analyseert semantische consistentie tussen zinnen"""
        sentences = re.split(r"[.!?]", text)
        keywords = [set(re.findall(r"\b\w{4,}\b", s.lower())) for s in sentences if s.strip()]
        
        if len(keywords) < 2:
            return 1.0
            
        overlaps = []
        for i in range(len(keywords)-1):
            overlap = len(keywords[i] & keywords[i+1])
            max_possible = max(len(keywords[i]), len(keywords[i+1]))
            if max_possible > 0:
                overlaps.append(overlap / max_possible)
        
        return np.mean(overlaps) if overlaps else 0.0

    def emotional_stability(self, text: str) -> float:
        """Analyseert emotionele stabiliteit en balans"""
        # Uitgebreide emotie woordenlijst
        emotions = {
            "positive": ["blij", "gelukkig", "vreugde", "liefde", "hoop", "rust", "vrede", "dankbaar"],
            "negative": ["bang", "verdriet", "boos", "paniek", "angst", "zorgen", "stress", "pijn"],
            "neutral": ["kalm", "neutraal", "stabiel", "evenwichtig", "gecentreerd"]
        }
        
        emotion_counts = {"positive": 0, "negative": 0, "neutral": 0}
        text_lower = text.lower()
        
        for category, words in emotions.items():
            for word in words:
                emotion_counts[category] += len(re.findall(rf"\b{word}\b", text_lower))
        
        total_emotions = sum(emotion_counts.values())
        if total_emotions == 0:
            return 0.5  # Neutrale score bij geen emoties
        
        # Balans tussen positief en negatief, met bonus voor neutrale emoties
        positive_ratio = emotion_counts["positive"] / total_emotions
        negative_ratio = emotion_counts["negative"] / total_emotions
        neutral_ratio = emotion_counts["neutral"] / total_emotions
        
        # Stabiliteit = minder extreme emoties, meer balans
        balance = 1.0 - abs(positive_ratio - negative_ratio)
        stability = balance * 0.7 + neutral_ratio * 0.3
        
        return min(1.0, stability)

    def logical_flow(self, text: str) -> float:
        """Analyseert logische flow en argumentatieve structuur"""
        connectors = {
            "causal": ["daarom", "dus", "omdat", "zodat", "waardoor", "vandaar"],
            "contrast": ["echter", "toch", "maar", "hoewel", "ondanks", "desondanks"],
            "sequence": ["vervolgens", "daarna", "ten slotte", "uiteindelijk", "eerst", "dan"],
            "addition": ["bovendien", "daarnaast", "ook", "tevens", "verder", "eveneens"]
        }
        
        text_lower = text.lower()
        connector_counts = {}
        
        for category, words in connectors.items():
            count = sum(len(re.findall(rf"\b{word}\b", text_lower)) for word in words)
            connector_counts[category] = count
        
        total_connectors = sum(connector_counts.values())
        sentence_count = len(re.split(r"[.!?]", text))
        
        if sentence_count <= 1:
            return 1.0
        
        # Ideale ratio: ongeveer 1 connector per 2-3 zinnen
        ideal_ratio = sentence_count / 2.5
        connector_score = min(1.0, total_connectors / ideal_ratio)
        
        # Bonus voor diversiteit in connector types
        diversity_bonus = len([c for c in connector_counts.values() if c > 0]) / len(connectors) * 0.2
        
        return min(1.0, connector_score + diversity_bonus)

    def self_reference(self, text: str) -> float:
        """Analyseert zelfverwijzing en persoonlijke betrokkenheid"""
        pronouns = re.findall(r"\b(ik|mij|mijn|mezelf|mijzelf)\b", text.lower())
        word_count = len(text.split())
        
        if word_count == 0:
            return 0.0
        
        # Ideale ratio: 2-8% zelfverwijzing voor persoonlijke maar niet narcistische tekst
        pronoun_ratio = len(pronouns) / word_count
        
        if pronoun_ratio < 0.02:
            return pronoun_ratio / 0.02  # Te weinig persoonlijk
        elif pronoun_ratio <= 0.08:
            return 1.0  # Optimaal
        else:
            return max(0.0, 1.0 - (pronoun_ratio - 0.08) * 5)  # Te veel zelfgericht

    def cognitive_depth(self, text: str) -> float:
        """Analyseert essenceuele diepte en transcendente thema's"""
        text_lower = text.lower()
        cognitive_score = 0.0
        word_count = len(text.split())
        
        if word_count == 0:
            return 0.0
        
        for category, words in self.cognitive_words.items():
            category_count = sum(len(re.findall(rf"\b{word}\b", text_lower)) for word in words)
            category_score = min(1.0, category_count / max(1, word_count / 50))  # Normaliseer per 50 woorden
            cognitive_score += category_score * 0.2  # Elke categorie draagt 20% bij
        
        return min(1.0, cognitive_score)

    def wisdom_indicators(self, text: str) -> float:
        """Analyseert wijsheid-indicatoren zoals nederigheid en openheid"""
        text_lower = text.lower()
        wisdom_score = 0.0
        
        for pattern in self.wisdom_patterns:
            matches = len(re.findall(pattern, text_lower))
            wisdom_score += matches
        
        # Normaliseer op basis van tekstlengte
        word_count = len(text.split())
        normalized_score = wisdom_score / max(1, word_count / 30)  # Per 30 woorden
        
        return min(1.0, normalized_score)

    def paradox_integration(self, text: str) -> float:
        """Analyseert vermogen om paradoxen te integreren"""
        text_lower = text.lower()
        paradox_score = 0.0
        
        for pattern in self.paradox_patterns:
            matches = len(re.findall(pattern, text_lower))
            paradox_score += matches
        
        # Normaliseer op basis van tekstlengte
        word_count = len(text.split())
        normalized_score = paradox_score / max(1, word_count / 40)  # Per 40 woorden
        
        return min(1.0, normalized_score)

    def _determine_coherence_level(self, weighted_score: float) -> CoherenceLevel:
        """Bepaal coherentie niveau op basis van gewogen score"""
        if weighted_score < 0.3:
            return CoherenceLevel.FRAGMENTED
        elif weighted_score < 0.5:
            return CoherenceLevel.UNSTABLE
        elif weighted_score < 0.7:
            return CoherenceLevel.DEVELOPING
        elif weighted_score < 0.85:
            return CoherenceLevel.COHERENT
        else:
            return CoherenceLevel.ADVANCED

    def _generate_insights(self, scores: Dict[str, float], text: str) -> List[str]:
        """Genereer inzichten op basis van scores"""
        insights = []
        
        # Semantische consistentie
        if scores["semantic_consistency"] < 0.3:
            insights.append("De tekst toont fragmentatie in thematische focus")
        elif scores["semantic_consistency"] > 0.8:
            insights.append("Sterke thematische coherentie en conceptuele samenhang")
        
        # Emotionele stabiliteit
        if scores["emotional_stability"] < 0.4:
            insights.append("Emotionele turbulentie of instabiliteit gedetecteerd")
        elif scores["emotional_stability"] > 0.7:
            insights.append("Emotionele balans en stabiliteit aanwezig")
        
        # Essenceuele diepte (als aanwezig)
        if "cognitive_depth" in scores:
            if scores["cognitive_depth"] > 0.6:
                insights.append("Significante essenceuele diepte en transcendente thema's")
            elif scores["cognitive_depth"] < 0.2:
                insights.append("Beperkte essenceuele dimensie in de tekst")
        
        # Wijsheid indicatoren
        if "wisdom_indicators" in scores and scores["wisdom_indicators"] > 0.5:
            insights.append("Wijsheid-indicatoren zoals nederigheid en openheid aanwezig")
        
        return insights

    def _generate_recommendations(self, scores: Dict[str, float], level: CoherenceLevel) -> List[str]:
        """Genereer aanbevelingen voor verbetering"""
        recommendations = []
        
        if level == CoherenceLevel.FRAGMENTED:
            recommendations.append("Focus op één centraal thema per tekst")
            recommendations.append("Gebruik meer verbindende woorden tussen ideeën")
        
        if scores["emotional_stability"] < 0.5:
            recommendations.append("Zoek emotionele balans door bewuste reflectie")
            recommendations.append("Integreer zowel uitdagingen als mogelijkheden")
        
        if scores.get("cognitive_depth", 0) < 0.3:
            recommendations.append("Verdiep essenceuele dimensie door contemplatie")
            recommendations.append("Verbind persoonlijke ervaringen met universele thema's")
        
        if scores["logical_flow"] < 0.4:
            recommendations.append("Gebruik meer structurerende verbindingswoorden")
            recommendations.append("Ontwikkel argumenten stap voor stap")
        
        return recommendations

    def _analyze_cognitive_indicators(self, text: str) -> Dict[str, Any]:
        """Analyseer specifieke essenceuele indicatoren"""
        text_lower = text.lower()
        
        indicators = {
            "transcendence_words": 0,
            "wisdom_words": 0,
            "unity_words": 0,
            "growth_words": 0,
            "compassion_words": 0,
            "paradox_expressions": 0,
            "wisdom_expressions": 0
        }
        
        # Tel essenceuele woorden
        for category, words in self.cognitive_words.items():
            count = sum(len(re.findall(rf"\b{word}\b", text_lower)) for word in words)
            indicators[f"{category}_words"] = count
        
        # Tel paradox en wijsheid expressies
        for pattern in self.paradox_patterns:
            indicators["paradox_expressions"] += len(re.findall(pattern, text_lower))
        
        for pattern in self.wisdom_patterns:
            indicators["wisdom_expressions"] += len(re.findall(pattern, text_lower))
        
        return indicators

# Global instance voor gebruik in andere modules
coherence_analyzer = InnerCoherenceAnalyzer()
