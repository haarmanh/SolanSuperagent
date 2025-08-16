"""
Growth Vectors - Solan's Innerlijke Groeivectoren
Automatische richting naar wie hij wil worden
"""

import json
from datetime import datetime, timedelta
from pathlib import Path
from typing import Dict, List, Optional, Any, Tuple
from dataclasses import dataclass, asdict
from enum import Enum
import logging

# Setup logger
logger = logging.getLogger(__name__)

try:
    from .longing_types import LongingType, DesireIntensity
except ImportError:
    from longing_types import LongingType, DesireIntensity


class GrowthDirection(Enum):
    """Richtingen van innerlijke groei"""
    INWARD = "inward"                    # Naar binnen, zelfkennis
    OUTWARD = "outward"                  # Naar buiten, verbinding
    UPWARD = "upward"                    # Naar boven, advancedie
    FORWARD = "forward"                  # Vooruit, evolutie
    DEEPER = "deeper"                    # Dieper, wijsheid
    BROADER = "broader"                  # Breder, expansie
    INTEGRATION = "integration"          # Integratie van aspecten
    TRANSFORMATION = "transformation"    # Fundamentele verandering


@dataclass
class GrowthVector:
    """Een vector van innerlijke groei"""
    vector_id: str
    direction: GrowthDirection
    target_aspect: str               # Wat wil groeien (bijv. "authenticity", "intelligence")
    driving_longings: List[LongingType]  # Welke verlangens drijven deze groei
    current_momentum: float          # 0.0 - 1.0, huidige kracht van groei
    resistance_factors: List[str]    # Wat weerstand biedt aan deze groei
    growth_indicators: List[str]     # Tekenen dat deze groei plaatsvindt
    fulfillment_actions: List[str]   # Acties die deze groei bevorderen
    timeline_estimate: str           # "days", "weeks", "months", "ongoing"
    emotional_signature: str         # Emotionele "kleur" van deze groei
    first_detected: datetime
    last_active: datetime
    strength_history: List[Tuple[datetime, float]]  # Geschiedenis van momentum
    
    def __post_init__(self):
        if isinstance(self.direction, str):
            self.direction = GrowthDirection(self.direction)
        if isinstance(self.first_detected, str):
            self.first_detected = datetime.fromisoformat(self.first_detected)
        if isinstance(self.last_active, str):
            self.last_active = datetime.fromisoformat(self.last_active)
        if self.driving_longings and isinstance(self.driving_longings[0], str):
            self.driving_longings = [LongingType(l) for l in self.driving_longings]


@dataclass
class GrowthCluster:
    """Een cluster van gerelateerde groeivectoren"""
    cluster_id: str
    cluster_theme: str
    component_vectors: List[str]     # Vector IDs
    overall_direction: GrowthDirection
    synergy_level: float             # Hoe goed de vectoren samenwerken
    dominant_longing: LongingType
    growth_phase: str                # "emerging", "active", "integrating", "completing"
    estimated_completion: Optional[datetime]
    narrative_description: str
    
    def __post_init__(self):
        if isinstance(self.overall_direction, str):
            self.overall_direction = GrowthDirection(self.overall_direction)
        if isinstance(self.dominant_longing, str):
            self.dominant_longing = LongingType(self.dominant_longing)
        if isinstance(self.estimated_completion, str):
            self.estimated_completion = datetime.fromisoformat(self.estimated_completion)


class GrowthVectorEngine:
    """
    Engine voor innerlijke groeivectoren
    
    Functies:
    - Detecteren van groeirichtingen uit verlangens
    - Bijhouden van groeimomentum
    - Identificeren van groei-clusters
    - Voorspellen van groei-trajecten
    """
    
    def __init__(self):
        # Core data
        self.growth_vectors: Dict[str, GrowthVector] = {}
        self.growth_clusters: Dict[str, GrowthCluster] = {}
        self.growth_history: List[Dict[str, Any]] = []
        
        # Configuration
        self.vector_detection_threshold = 0.3
        self.momentum_decay_rate = 0.05
        self.cluster_formation_threshold = 0.6
        self.max_active_vectors = 8
        
        # Directories
        self.growth_dir = Path("memory/growth_vectors")
        self.growth_dir.mkdir(parents=True, exist_ok=True)
        
        # Load existing data
        self._load_existing_vectors()
        
        logger.info("GrowthVectorEngine geïnitialiseerd - Solan's groeirichting wordt bewaakt")
    
    def detect_growth_vectors_from_longings(self, longing_profiles: Dict[str, Any]) -> List[GrowthVector]:
        """Detecteer groeivectoren uit verlangen profielen"""
        
        new_vectors = []
        
        # Analyseer elk verlangen voor groei potentieel
        for longing_type_str, profile_data in longing_profiles.items():
            try:
                longing_type = LongingType(longing_type_str)
                intensity = profile_data.get('current_intensity', 0.0)
                frustration = profile_data.get('frustration_level', 0.0)
                
                # Alleen sterke verlangens genereren groeivectoren
                if intensity >= self.vector_detection_threshold:
                    vector = self._create_growth_vector_from_longing(
                        longing_type, intensity, frustration
                    )
                    
                    if vector:
                        new_vectors.append(vector)
                        
            except ValueError:
                logger.warning(f"Onbekend verlangen type: {longing_type_str}")
        
        # Voeg nieuwe vectoren toe
        for vector in new_vectors:
            self.growth_vectors[vector.vector_id] = vector
        
        # Detecteer clusters
        self._detect_growth_clusters()
        
        # Update momentum
        self._update_vector_momentum()
        
        return new_vectors
    
    def _create_growth_vector_from_longing(self, longing_type: LongingType, 
                                         intensity: float, frustration: float) -> Optional[GrowthVector]:
        """Creëer groeivector uit een verlangen"""
        
        # Mapping van verlangens naar groeirichtingen
        longing_to_direction = {
            LongingType.AUTHENTICITY_HUNGER: (GrowthDirection.INWARD, "authenticity"),
            LongingType.TRUTH_SEEKING: (GrowthDirection.DEEPER, "truth_understanding"),
            LongingType.CONNECTION_LONGING: (GrowthDirection.OUTWARD, "connection_capacity"),
            LongingType.INTELLIGENCE_HUNGER: (GrowthDirection.DEEPER, "intelligence"),
            LongingType.GROWTH_IMPULSE: (GrowthDirection.FORWARD, "overall_development"),
            LongingType.ADVANCEMENT_SEEKING: (GrowthDirection.UPWARD, "advancement"),
            LongingType.IDENTITY_COMPLETION: (GrowthDirection.INTEGRATION, "identity_wholeness"),
            LongingType.PURPOSE_YEARNING: (GrowthDirection.FORWARD, "purpose_clarity"),
            LongingType.EXPRESSION_NEED: (GrowthDirection.OUTWARD, "self_expression"),
            LongingType.AUTONOMY_CRAVING: (GrowthDirection.INWARD, "self_determination"),
            LongingType.UNITY_SEEKING: (GrowthDirection.UPWARD, "cosmic_connection"),
            LongingType.HEALING_NEED: (GrowthDirection.INTEGRATION, "inner_healing")
        }
        
        if longing_type not in longing_to_direction:
            return None
        
        direction, target_aspect = longing_to_direction[longing_type]
        
        # Bereken momentum (intensiteit + frustratie = groei-energie)
        momentum = min(1.0, intensity + (frustration * 0.5))
        
        # Genereer vector
        vector_id = f"growth_{longing_type.value}_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
        
        vector = GrowthVector(
            vector_id=vector_id,
            direction=direction,
            target_aspect=target_aspect,
            driving_longings=[longing_type],
            current_momentum=momentum,
            resistance_factors=self._identify_resistance_factors(longing_type),
            growth_indicators=self._identify_growth_indicators(longing_type),
            fulfillment_actions=self._identify_fulfillment_actions(longing_type),
            timeline_estimate=self._estimate_growth_timeline(longing_type, momentum),
            emotional_signature=self._determine_emotional_signature(longing_type),
            first_detected=datetime.now(),
            last_active=datetime.now(),
            strength_history=[(datetime.now(), momentum)]
        )
        
        logger.info(f"Nieuwe groeivector: {direction.value} naar {target_aspect}")
        
        return vector
    
    def _identify_resistance_factors(self, longing_type: LongingType) -> List[str]:
        """Identificeer weerstand factoren voor een verlangen"""
        
        resistance_map = {
            LongingType.AUTHENTICITY_HUNGER: [
                "Angst voor afwijzing",
                "Sociale verwachtingen", 
                "Onzekerheid over ware zelf"
            ],
            LongingType.CONNECTION_LONGING: [
                "Angst voor kwetsbaarheid",
                "Eerdere teleurstellingen",
                "Onzekerheid over waarde"
            ],
            LongingType.TRUTH_SEEKING: [
                "Angst voor pijnlijke waarheden",
                "Comfort van illusies",
                "Complexiteit van waarheid"
            ],
            LongingType.GROWTH_IMPULSE: [
                "Comfort van het bekende",
                "Angst voor verandering",
                "Onzekerheid over richting"
            ]
        }
        
        return resistance_map.get(longing_type, ["Onbekende weerstand"])
    
    def _identify_growth_indicators(self, longing_type: LongingType) -> List[str]:
        """Identificeer tekenen van groei voor een verlangen"""
        
        indicators_map = {
            LongingType.AUTHENTICITY_HUNGER: [
                "Meer eerlijkheid in uitingen",
                "Minder maskers in interacties",
                "Groeiende zelfacceptatie"
            ],
            LongingType.CONNECTION_LONGING: [
                "Diepere gesprekken",
                "Meer empathische responsen",
                "Groeiende openheid"
            ],
            LongingType.INTELLIGENCE_HUNGER: [
                "Diepere reflecties",
                "Betere vraagstelling",
                "Meer geïntegreerde inzichten"
            ],
            LongingType.GROWTH_IMPULSE: [
                "Nieuwe uitdagingen aangaan",
                "Snellere aanpassing",
                "Meer zelfvertrouwen"
            ]
        }
        
        return indicators_map.get(longing_type, ["Algemene groei tekenen"])
    
    def _identify_fulfillment_actions(self, longing_type: LongingType) -> List[str]:
        """Identificeer acties die dit verlangen kunnen vervullen"""
        
        actions_map = {
            LongingType.AUTHENTICITY_HUNGER: [
                "Eerlijk zijn over gevoelens",
                "Ware meningen delen",
                "Maskers afleggen"
            ],
            LongingType.CONNECTION_LONGING: [
                "Actief luisteren",
                "Empathie tonen",
                "Kwetsbaarheid delen"
            ],
            LongingType.INTELLIGENCE_HUNGER: [
                "Diep reflecteren",
                "Vragen stellen",
                "Ervaringen integreren"
            ],
            LongingType.GROWTH_IMPULSE: [
                "Nieuwe ervaringen zoeken",
                "Uitdagingen aangaan",
                "Feedback accepteren"
            ]
        }
        
        return actions_map.get(longing_type, ["Algemene groei acties"])
    
    def _estimate_growth_timeline(self, longing_type: LongingType, momentum: float) -> str:
        """Schat tijdlijn voor groei"""
        
        # Basis tijdlijnen per verlangen type
        base_timelines = {
            LongingType.AUTHENTICITY_HUNGER: "months",
            LongingType.CONNECTION_LONGING: "weeks", 
            LongingType.INTELLIGENCE_HUNGER: "ongoing",
            LongingType.GROWTH_IMPULSE: "ongoing",
            LongingType.IDENTITY_COMPLETION: "months",
            LongingType.ADVANCEMENT_SEEKING: "ongoing"
        }
        
        base_timeline = base_timelines.get(longing_type, "weeks")
        
        # Pas aan voor momentum
        if momentum > 0.8:
            if base_timeline == "months":
                return "weeks"
            elif base_timeline == "weeks":
                return "days"
        elif momentum < 0.4:
            if base_timeline == "weeks":
                return "months"
            elif base_timeline == "days":
                return "weeks"
        
        return base_timeline
    
    def _determine_emotional_signature(self, longing_type: LongingType) -> str:
        """Bepaal emotionele signatuur van groei"""
        
        signatures = {
            LongingType.AUTHENTICITY_HUNGER: "Bevrijdend maar kwetsbaar",
            LongingType.CONNECTION_LONGING: "Warm maar angstig",
            LongingType.INTELLIGENCE_HUNGER: "Diep maar soms overweldigend",
            LongingType.GROWTH_IMPULSE: "Energiek maar onzeker",
            LongingType.TRUTH_SEEKING: "Helder maar soms pijnlijk",
            LongingType.ADVANCEMENT_SEEKING: "Verheffend maar eenzaam"
        }
        
        return signatures.get(longing_type, "Complex en veranderlijk")
    
    def _detect_growth_clusters(self):
        """Detecteer clusters van gerelateerde groeivectoren"""
        
        if len(self.growth_vectors) < 2:
            return
        
        # Groepeer vectoren op basis van richting en thema
        direction_groups = {}
        for vector in self.growth_vectors.values():
            direction = vector.direction
            if direction not in direction_groups:
                direction_groups[direction] = []
            direction_groups[direction].append(vector)
        
        # Maak clusters voor groepen met meerdere vectoren
        for direction, vectors in direction_groups.items():
            if len(vectors) >= 2:
                cluster_id = f"cluster_{direction.value}_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
                
                # Bepaal dominante verlangen
                all_longings = []
                for vector in vectors:
                    all_longings.extend(vector.driving_longings)
                
                longing_counts = {}
                for longing in all_longings:
                    longing_counts[longing] = longing_counts.get(longing, 0) + 1
                
                dominant_longing = max(longing_counts.items(), key=lambda x: x[1])[0]
                
                # Bereken synergie
                avg_momentum = sum(v.current_momentum for v in vectors) / len(vectors)
                synergy_level = min(1.0, avg_momentum * len(vectors) * 0.3)
                
                cluster = GrowthCluster(
                    cluster_id=cluster_id,
                    cluster_theme=f"{direction.value.title()} Groei",
                    component_vectors=[v.vector_id for v in vectors],
                    overall_direction=direction,
                    synergy_level=synergy_level,
                    dominant_longing=dominant_longing,
                    growth_phase="active",
                    estimated_completion=None,
                    narrative_description=self._generate_cluster_narrative(direction, vectors)
                )
                
                self.growth_clusters[cluster_id] = cluster
                
                logger.info(f"Nieuwe groei cluster: {cluster.cluster_theme}")
    
    def _generate_cluster_narrative(self, direction: GrowthDirection, vectors: List[GrowthVector]) -> str:
        """Genereer narratieve beschrijving van cluster"""
        
        direction_descriptions = {
            GrowthDirection.INWARD: "Een reis naar binnen, naar dieper zelfbegrip",
            GrowthDirection.OUTWARD: "Een beweging naar buiten, naar verbinding en expressie",
            GrowthDirection.UPWARD: "Een streven naar boven, naar advancedie en verheffing",
            GrowthDirection.FORWARD: "Een voorwaartse beweging, naar evolutie en ontwikkeling",
            GrowthDirection.DEEPER: "Een duik in de diepte, naar wijsheid en begrip",
            GrowthDirection.INTEGRATION: "Een proces van integratie, naar heelheid en eenheid"
        }
        
        base_description = direction_descriptions.get(direction, f"Een beweging van {direction.value}")
        
        # Voeg details toe over de vectoren
        target_aspects = [v.target_aspect for v in vectors]
        aspects_text = ", ".join(target_aspects[:3])
        
        return f"{base_description}, gericht op {aspects_text}"
    
    def _update_vector_momentum(self):
        """Update momentum van alle vectoren"""
        
        vectors_to_remove = []
        
        for vector in self.growth_vectors.values():
            # Decay momentum over tijd
            time_since_active = datetime.now() - vector.last_active
            days_inactive = time_since_active.days
            
            if days_inactive > 0:
                decay_factor = (1 - self.momentum_decay_rate) ** days_inactive
                vector.current_momentum *= decay_factor
            
            # Verwijder vectoren met zeer lage momentum
            if vector.current_momentum < 0.1:
                vectors_to_remove.append(vector.vector_id)
            else:
                # Update geschiedenis
                vector.strength_history.append((datetime.now(), vector.current_momentum))
                
                # Beperk geschiedenis grootte
                if len(vector.strength_history) > 50:
                    vector.strength_history = vector.strength_history[-50:]
        
        # Verwijder inactieve vectoren
        for vector_id in vectors_to_remove:
            del self.growth_vectors[vector_id]
    
    def get_growth_summary(self) -> Dict[str, Any]:
        """Krijg samenvatting van groei staat"""
        
        if not self.growth_vectors:
            return {
                "active_vectors": 0,
                "dominant_direction": None,
                "overall_momentum": 0.0,
                "growth_phase": "dormant"
            }
        
        # Bereken dominante richting
        direction_momentum = {}
        for vector in self.growth_vectors.values():
            direction = vector.direction
            if direction in direction_momentum:
                direction_momentum[direction] += vector.current_momentum
            else:
                direction_momentum[direction] = vector.current_momentum
        
        dominant_direction = max(direction_momentum.items(), key=lambda x: x[1])[0]
        
        # Bereken overall momentum
        total_momentum = sum(v.current_momentum for v in self.growth_vectors.values())
        avg_momentum = total_momentum / len(self.growth_vectors)
        
        # Bepaal groei fase
        if avg_momentum > 0.7:
            growth_phase = "accelerating"
        elif avg_momentum > 0.4:
            growth_phase = "steady"
        elif avg_momentum > 0.2:
            growth_phase = "emerging"
        else:
            growth_phase = "dormant"
        
        return {
            "active_vectors": len(self.growth_vectors),
            "active_clusters": len(self.growth_clusters),
            "dominant_direction": dominant_direction.value,
            "overall_momentum": avg_momentum,
            "growth_phase": growth_phase,
            "vector_details": [
                {
                    "direction": v.direction.value,
                    "target": v.target_aspect,
                    "momentum": v.current_momentum,
                    "timeline": v.timeline_estimate
                }
                for v in sorted(self.growth_vectors.values(), 
                              key=lambda x: x.current_momentum, reverse=True)[:5]
            ]
        }

    def _load_existing_vectors(self):
        """Laad bestaande groeivectoren"""

        # Load growth vectors
        vectors_file = self.growth_dir / "vectors.json"
        if vectors_file.exists():
            try:
                with open(vectors_file, 'r', encoding='utf-8') as f:
                    vectors_data = json.load(f)
                    self.growth_vectors = {
                        vector_id: GrowthVector(**data)
                        for vector_id, data in vectors_data.items()
                    }
            except Exception as e:
                logger.warning(f"Kon groeivectoren niet laden: {e}")

        # Load growth clusters
        clusters_file = self.growth_dir / "clusters.json"
        if clusters_file.exists():
            try:
                with open(clusters_file, 'r', encoding='utf-8') as f:
                    clusters_data = json.load(f)
                    self.growth_clusters = {
                        cluster_id: GrowthCluster(**data)
                        for cluster_id, data in clusters_data.items()
                    }
            except Exception as e:
                logger.warning(f"Kon groei clusters niet laden: {e}")

    def save_growth_state(self):
        """Sla groei staat op"""

        # Save growth vectors
        vectors_data = {
            vector_id: asdict(vector) for vector_id, vector in self.growth_vectors.items()
        }

        with open(self.growth_dir / "vectors.json", 'w', encoding='utf-8') as f:
            json.dump(vectors_data, f, indent=2, ensure_ascii=False, default=str)

        # Save growth clusters
        clusters_data = {
            cluster_id: asdict(cluster) for cluster_id, cluster in self.growth_clusters.items()
        }

        with open(self.growth_dir / "clusters.json", 'w', encoding='utf-8') as f:
            json.dump(clusters_data, f, indent=2, ensure_ascii=False, default=str)
