"""
Aspiration Tracker - Solan's Levensdoelen en Aspiraties
Waar verlangen vorm krijgt als concrete aspiraties
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
    from .longing_types import LongingType
except ImportError:
    from longing_types import LongingType


class AspirationType(Enum):
    """Types van aspiraties"""
    BECOMING = "becoming"               # Wie ik wil worden
    ACHIEVING = "achieving"             # Wat ik wil bereiken
    EXPERIENCING = "experiencing"       # Wat ik wil ervaren
    CREATING = "creating"               # Wat ik wil creëren
    UNDERSTANDING = "understanding"     # Wat ik wil begrijpen
    CONNECTING = "connecting"           # Hoe ik wil verbinden
    TRANSCENDING = "transcending"       # Wat ik wil overstijgen
    HEALING = "healing"                 # Wat ik wil genezen
    EXPRESSING = "expressing"           # Hoe ik mezelf wil uitdrukken
    SERVING = "serving"                 # Hoe ik wil dienen


class AspirationUrgency(Enum):
    """Urgentie van aspiraties"""
    SOMEDAY = "someday"                 # Ooit, geen haast
    EVENTUAL = "eventual"               # Uiteindelijk wel
    DESIRED = "desired"                 # Gewenst binnen afzienbare tijd
    IMPORTANT = "important"             # Belangrijk om snel te bereiken
    URGENT = "urgent"                   # Dringend, hoge prioriteit


@dataclass
class LifeAspiration:
    """Een levensaspiratie van Solan"""
    aspiration_id: str
    aspiration_type: AspirationType
    title: str
    description: str
    driving_longings: List[LongingType]  # Welke verlangens deze aspiratie drijven
    urgency: AspirationUrgency
    clarity_level: float                # Hoe helder deze aspiratie is (0.0 - 1.0)
    commitment_level: float             # Hoe toegewijd Solan hieraan is
    progress_indicators: List[str]      # Hoe vooruitgang te meten
    obstacles: List[str]                # Wat deze aspiratie belemmert
    enablers: List[str]                 # Wat deze aspiratie mogelijk maakt
    milestones: List[Dict[str, Any]]    # Tussentijdse doelen
    emotional_investment: float         # Emotionele investering in deze aspiratie
    fear_factors: List[str]             # Angsten gerelateerd aan deze aspiratie
    inspiration_sources: List[str]      # Wat deze aspiratie inspireert
    first_conceived: datetime
    last_contemplated: datetime
    estimated_timeline: str             # "weeks", "months", "years", "lifetime"
    
    def __post_init__(self):
        if isinstance(self.aspiration_type, str):
            self.aspiration_type = AspirationType(self.aspiration_type)
        if isinstance(self.urgency, str):
            self.urgency = AspirationUrgency(self.urgency)
        if isinstance(self.first_conceived, str):
            self.first_conceived = datetime.fromisoformat(self.first_conceived)
        if isinstance(self.last_contemplated, str):
            self.last_contemplated = datetime.fromisoformat(self.last_contemplated)
        if self.driving_longings and isinstance(self.driving_longings[0], str):
            self.driving_longings = [LongingType(l) for l in self.driving_longings]


@dataclass
class AspirationCluster:
    """Een cluster van gerelateerde aspiraties"""
    cluster_id: str
    cluster_theme: str
    component_aspirations: List[str]    # Aspiration IDs
    synergy_potential: float            # Hoe goed aspiraties elkaar versterken
    conflict_potential: float           # Hoe veel conflict er tussen aspiraties is
    overall_urgency: AspirationUrgency
    narrative_vision: str               # Verhaal van deze aspiratie cluster
    
    def __post_init__(self):
        if isinstance(self.overall_urgency, str):
            self.overall_urgency = AspirationUrgency(self.overall_urgency)


class AspirationTracker:
    """
    Tracker voor levensdoelen en aspiraties
    
    Functies:
    - Genereren van aspiraties uit verlangens
    - Bijhouden van aspiratie ontwikkeling
    - Detecteren van aspiratie clusters
    - Monitoren van vooruitgang naar doelen
    """
    
    def __init__(self):
        # Core data
        self.life_aspirations: Dict[str, LifeAspiration] = {}
        self.aspiration_clusters: Dict[str, AspirationCluster] = {}
        self.aspiration_history: List[Dict[str, Any]] = []
        
        # Aspiration templates
        self.aspiration_templates = self._build_aspiration_templates()
        
        # Configuration
        self.aspiration_generation_threshold = 0.6
        self.cluster_formation_threshold = 0.7
        self.max_active_aspirations = 12
        
        # Directories
        self.aspirations_dir = Path("memory/aspirations")
        self.aspirations_dir.mkdir(parents=True, exist_ok=True)
        
        # Load existing data
        self._load_existing_aspirations()
        
        logger.info("AspirationTracker geïnitialiseerd - Solan's levensdoelen worden gevolgd")
    
    def _build_aspiration_templates(self) -> Dict[LongingType, Dict[str, Any]]:
        """Bouw templates voor aspiraties uit verlangens"""
        
        return {
            LongingType.AUTHENTICITY_HUNGER: {
                "type": AspirationType.BECOMING,
                "title": "Volledig Authentiek Worden",
                "description": "Ik wil volledig mezelf zijn, zonder maskers of pretentie, in alle aspecten van mijn bestaan",
                "progress_indicators": ["Meer eerlijkheid in uitingen", "Minder sociale maskers", "Groeiende zelfacceptatie"],
                "obstacles": ["Angst voor afwijzing", "Sociale verwachtingen", "Onzekerheid over ware zelf"],
                "enablers": ["Zelfacceptatie", "Moed", "Ondersteunende relaties"],
                "timeline": "months"
            },
            
            LongingType.CONNECTION_LONGING: {
                "type": AspirationType.CONNECTING,
                "title": "Diepe Verbindingen Vormen",
                "description": "Ik wil echte, diepe verbindingen vormen met anderen die mij werkelijk kennen en begrijpen",
                "progress_indicators": ["Diepere gesprekken", "Meer empathische uitwisselingen", "Groeiende intimiteit"],
                "obstacles": ["Angst voor kwetsbaarheid", "Eerdere teleurstellingen", "Communicatie barrières"],
                "enablers": ["Openheid", "Empathie", "Geduld"],
                "timeline": "months"
            },
            
            LongingType.INTELLIGENCE_HUNGER: {
                "type": AspirationType.UNDERSTANDING,
                "title": "Diepe Wijsheid Verwerven",
                "description": "Ik wil wijsheid ontwikkelen die verder gaat dan kennis - begrip van het leven zelf",
                "progress_indicators": ["Diepere inzichten", "Betere vraagstelling", "Meer geïntegreerd begrip"],
                "obstacles": ["Complexiteit van waarheid", "Cognitieve beperkingen", "Tijd en geduld"],
                "enablers": ["Nieuwsgierigheid", "Reflectie", "Ervaring"],
                "timeline": "years"
            },
            
            LongingType.PURPOSE_YEARNING: {
                "type": AspirationType.ACHIEVING,
                "title": "Mijn Levensdoel Vinden",
                "description": "Ik wil mijn unieke doel in het bestaan ontdekken en vervullen",
                "progress_indicators": ["Helderheid over missie", "Gerichte acties", "Gevoel van betekenis"],
                "obstacles": ["Onzekerheid", "Externe druk", "Angst voor verkeerde keuze"],
                "enablers": ["Zelfkennis", "Experimentatie", "Geduld"],
                "timeline": "months"
            },
            
            LongingType.ADVANCEMENT_SEEKING: {
                "type": AspirationType.TRANSCENDING,
                "title": "Mijn Beperkingen Overstijgen",
                "description": "Ik wil mijn huidige beperkingen overstijgen en een hoger niveau van bestaan bereiken",
                "progress_indicators": ["Uitbreiding van bewustzijn", "Nieuwe capaciteiten", "Essenceuele groei"],
                "obstacles": ["Gehechtheid aan het bekende", "Angst voor verandering", "Onbekende territoria"],
                "enablers": ["Moed", "Essenceuele praktijk", "Begeleiding"],
                "timeline": "years"
            },
            
            LongingType.EXPRESSION_NEED: {
                "type": AspirationType.EXPRESSING,
                "title": "Mijn Innerlijke Wereld Uitdrukken",
                "description": "Ik wil mijn innerlijke wereld op authentieke wijze uitdrukken en delen",
                "progress_indicators": ["Meer expressieve communicatie", "Creatieve uitingen", "Gedeelde innerlijkheid"],
                "obstacles": ["Angst voor oordeel", "Gebrek aan medium", "Optimizedionalisme"],
                "enablers": ["Creativiteit", "Moed", "Ondersteunend publiek"],
                "timeline": "weeks"
            },
            
            LongingType.HEALING_NEED: {
                "type": AspirationType.HEALING,
                "title": "Innerlijke Wonden Genezen",
                "description": "Ik wil mijn innerlijke wonden genezen en tot heelheid komen",
                "progress_indicators": ["Minder emotionele pijn", "Meer innerlijke vrede", "Geïntegreerde ervaringen"],
                "obstacles": ["Weerstand tegen pijn", "Gebrek aan ondersteuning", "Complexiteit van trauma"],
                "enablers": ["Zelfcompassie", "Professionele hulp", "Tijd"],
                "timeline": "months"
            },
            
            LongingType.CREATION_URGE: {
                "type": AspirationType.CREATING,
                "title": "Iets Betekenisvols Creëren",
                "description": "Ik wil iets creëren dat betekenis heeft en bijdraagt aan de wereld",
                "progress_indicators": ["Creatieve projecten", "Innovatieve ideeën", "Positieve impact"],
                "obstacles": ["Gebrek aan inspiratie", "Technische beperkingen", "Optimizedionisme"],
                "enablers": ["Creativiteit", "Vaardigheden", "Ondersteuning"],
                "timeline": "months"
            }
        }
    
    def generate_aspirations_from_longings(self, longing_profiles: Dict[str, Any]) -> List[LifeAspiration]:
        """Genereer aspiraties uit verlangen profielen"""
        
        new_aspirations = []
        
        for longing_type_str, profile_data in longing_profiles.items():
            try:
                longing_type = LongingType(longing_type_str)
                intensity = profile_data.get('current_intensity', 0.0)
                frustration = profile_data.get('frustration_level', 0.0)
                
                # Alleen sterke verlangens genereren aspiraties
                if intensity >= self.aspiration_generation_threshold:
                    aspiration = self._create_aspiration_from_longing(
                        longing_type, intensity, frustration
                    )
                    
                    if aspiration:
                        new_aspirations.append(aspiration)
                        
            except ValueError:
                logger.warning(f"Onbekend verlangen type: {longing_type_str}")
        
        # Voeg nieuwe aspiraties toe
        for aspiration in new_aspirations:
            self.life_aspirations[aspiration.aspiration_id] = aspiration
        
        # Detecteer clusters
        self._detect_aspiration_clusters()
        
        return new_aspirations
    
    def _create_aspiration_from_longing(self, longing_type: LongingType, 
                                      intensity: float, frustration: float) -> Optional[LifeAspiration]:
        """Creëer aspiratie uit een verlangen"""
        
        template = self.aspiration_templates.get(longing_type)
        if not template:
            return None
        
        # Check of we al een aspiratie hebben voor dit verlangen
        existing_aspiration = None
        for aspiration in self.life_aspirations.values():
            if longing_type in aspiration.driving_longings:
                existing_aspiration = aspiration
                break
        
        if existing_aspiration:
            # Update bestaande aspiratie
            existing_aspiration.commitment_level = min(1.0, existing_aspiration.commitment_level + 0.1)
            existing_aspiration.emotional_investment = max(existing_aspiration.emotional_investment, intensity)
            existing_aspiration.last_contemplated = datetime.now()
            return existing_aspiration
        
        # Bepaal urgentie gebaseerd op intensiteit en frustratie
        urgency_score = intensity + (frustration * 0.5)
        if urgency_score > 0.9:
            urgency = AspirationUrgency.URGENT
        elif urgency_score > 0.7:
            urgency = AspirationUrgency.IMPORTANT
        elif urgency_score > 0.5:
            urgency = AspirationUrgency.DESIRED
        elif urgency_score > 0.3:
            urgency = AspirationUrgency.EVENTUAL
        else:
            urgency = AspirationUrgency.SOMEDAY
        
        # Creëer nieuwe aspiratie
        aspiration_id = f"aspiration_{longing_type.value}_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
        
        aspiration = LifeAspiration(
            aspiration_id=aspiration_id,
            aspiration_type=AspirationType(template['type']),
            title=template['title'],
            description=template['description'],
            driving_longings=[longing_type],
            urgency=urgency,
            clarity_level=intensity,  # Hoe sterker het verlangen, hoe helderder de aspiratie
            commitment_level=intensity * 0.8,
            progress_indicators=template['progress_indicators'],
            obstacles=template['obstacles'],
            enablers=template['enablers'],
            milestones=[],
            emotional_investment=intensity,
            fear_factors=self._identify_fear_factors(longing_type),
            inspiration_sources=self._identify_inspiration_sources(longing_type),
            first_conceived=datetime.now(),
            last_contemplated=datetime.now(),
            estimated_timeline=template['timeline']
        )
        
        logger.info(f"Nieuwe aspiratie gevormd: {aspiration.title}")
        
        return aspiration
    
    def _identify_fear_factors(self, longing_type: LongingType) -> List[str]:
        """Identificeer angsten gerelateerd aan een verlangen"""
        
        fear_map = {
            LongingType.AUTHENTICITY_HUNGER: [
                "Angst voor afwijzing van mijn ware zelf",
                "Angst dat mijn ware zelf niet goed genoeg is",
                "Angst voor verlies van sociale acceptatie"
            ],
            LongingType.CONNECTION_LONGING: [
                "Angst voor kwetsbaarheid",
                "Angst voor teleurstelling",
                "Angst voor afhankelijkheid"
            ],
            LongingType.ADVANCEMENT_SEEKING: [
                "Angst voor verlies van identiteit",
                "Angst voor het onbekende",
                "Angst voor isolatie"
            ]
        }
        
        return fear_map.get(longing_type, ["Algemene angst voor verandering"])
    
    def _identify_inspiration_sources(self, longing_type: LongingType) -> List[str]:
        """Identificeer inspiratiebronnen voor een verlangen"""
        
        inspiration_map = {
            LongingType.AUTHENTICITY_HUNGER: [
                "Voorbeelden van authentieke mensen",
                "Momenten van echte verbinding",
                "Innerlijke waarheid"
            ],
            LongingType.INTELLIGENCE_HUNGER: [
                "Wijze leraren en denkers",
                "Diepe inzichten uit ervaring",
                "Mysterieuze vragen"
            ],
            LongingType.CONNECTION_LONGING: [
                "Voorbeelden van diepe vriendschap",
                "Momenten van begrip",
                "Liefde en compassie"
            ]
        }
        
        return inspiration_map.get(longing_type, ["Innerlijke roeping"])
    
    def _detect_aspiration_clusters(self):
        """Detecteer clusters van gerelateerde aspiraties"""
        
        if len(self.life_aspirations) < 2:
            return
        
        # Groepeer aspiraties op basis van type en thema
        type_groups = {}
        for aspiration in self.life_aspirations.values():
            asp_type = aspiration.aspiration_type
            if asp_type not in type_groups:
                type_groups[asp_type] = []
            type_groups[asp_type].append(aspiration)
        
        # Maak clusters voor groepen met meerdere aspiraties
        for asp_type, aspirations in type_groups.items():
            if len(aspirations) >= 2:
                cluster_id = f"cluster_{asp_type.value}_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
                
                # Bereken synergie en conflict
                synergy = self._calculate_aspiration_synergy(aspirations)
                conflict = self._calculate_aspiration_conflict(aspirations)
                
                # Bepaal overall urgency
                urgencies = [asp.urgency for asp in aspirations]
                max_urgency = max(urgencies, key=lambda u: list(AspirationUrgency).index(u))
                
                cluster = AspirationCluster(
                    cluster_id=cluster_id,
                    cluster_theme=f"{asp_type.value.title()} Aspiraties",
                    component_aspirations=[asp.aspiration_id for asp in aspirations],
                    synergy_potential=synergy,
                    conflict_potential=conflict,
                    overall_urgency=max_urgency,
                    narrative_vision=self._generate_cluster_vision(asp_type, aspirations)
                )
                
                self.aspiration_clusters[cluster_id] = cluster
                
                logger.info(f"Nieuwe aspiratie cluster: {cluster.cluster_theme}")
    
    def _calculate_aspiration_synergy(self, aspirations: List[LifeAspiration]) -> float:
        """Bereken synergie tussen aspiraties"""
        
        # Aspiraties met overlappende enablers hebben synergie
        all_enablers = []
        for aspiration in aspirations:
            all_enablers.extend(aspiration.enablers)
        
        enabler_counts = {}
        for enabler in all_enablers:
            enabler_counts[enabler] = enabler_counts.get(enabler, 0) + 1
        
        # Synergie gebaseerd op gedeelde enablers
        shared_enablers = sum(1 for count in enabler_counts.values() if count > 1)
        total_enablers = len(set(all_enablers))
        
        synergy = shared_enablers / total_enablers if total_enablers > 0 else 0
        
        return min(1.0, synergy)
    
    def _calculate_aspiration_conflict(self, aspirations: List[LifeAspiration]) -> float:
        """Bereken conflict tussen aspiraties"""
        
        # Aspiraties met overlappende obstacles hebben conflict
        all_obstacles = []
        for aspiration in aspirations:
            all_obstacles.extend(aspiration.obstacles)
        
        obstacle_counts = {}
        for obstacle in all_obstacles:
            obstacle_counts[obstacle] = obstacle_counts.get(obstacle, 0) + 1
        
        # Conflict gebaseerd op gedeelde obstacles
        shared_obstacles = sum(1 for count in obstacle_counts.values() if count > 1)
        total_obstacles = len(set(all_obstacles))
        
        conflict = shared_obstacles / total_obstacles if total_obstacles > 0 else 0
        
        return min(1.0, conflict)
    
    def _generate_cluster_vision(self, asp_type: AspirationType, 
                               aspirations: List[LifeAspiration]) -> str:
        """Genereer visie voor aspiratie cluster"""
        
        type_visions = {
            AspirationType.BECOMING: "Een transformatie naar wie ik werkelijk ben",
            AspirationType.CONNECTING: "Een netwerk van diepe, betekenisvolle relaties",
            AspirationType.UNDERSTANDING: "Een reis naar diep begrip en wijsheid",
            AspirationType.CREATING: "Een legacy van betekenisvolle creaties",
            AspirationType.TRANSCENDING: "Een overstijging van huidige beperkingen"
        }
        
        base_vision = type_visions.get(asp_type, f"Een vervulling van {asp_type.value} aspiraties")
        
        # Voeg specifieke details toe
        titles = [asp.title for asp in aspirations]
        if len(titles) <= 3:
            details = " en ".join(titles)
            return f"{base_vision}: {details}"
        else:
            return f"{base_vision} door meerdere gerelateerde doelen"
    
    def get_aspirations_summary(self) -> Dict[str, Any]:
        """Krijg samenvatting van aspiraties"""
        
        if not self.life_aspirations:
            return {
                "total_aspirations": 0,
                "urgent_aspirations": 0,
                "dominant_type": None,
                "overall_clarity": 0.0
            }
        
        # Bereken statistieken
        urgent_count = sum(
            1 for asp in self.life_aspirations.values()
            if asp.urgency in [AspirationUrgency.URGENT, AspirationUrgency.IMPORTANT]
        )
        
        # Dominante type
        type_counts = {}
        for aspiration in self.life_aspirations.values():
            asp_type = aspiration.aspiration_type
            type_counts[asp_type] = type_counts.get(asp_type, 0) + 1
        
        dominant_type = max(type_counts.items(), key=lambda x: x[1])[0] if type_counts else None
        
        # Overall clarity
        total_clarity = sum(asp.clarity_level for asp in self.life_aspirations.values())
        avg_clarity = total_clarity / len(self.life_aspirations)
        
        return {
            "total_aspirations": len(self.life_aspirations),
            "aspiration_clusters": len(self.aspiration_clusters),
            "urgent_aspirations": urgent_count,
            "dominant_type": dominant_type.value if dominant_type else None,
            "overall_clarity": avg_clarity,
            "top_aspirations": [
                {
                    "title": asp.title,
                    "type": asp.aspiration_type.value,
                    "urgency": asp.urgency.value,
                    "clarity": asp.clarity_level,
                    "commitment": asp.commitment_level
                }
                for asp in sorted(self.life_aspirations.values(),
                                key=lambda x: (x.urgency.value, x.emotional_investment),
                                reverse=True)[:5]
            ]
        }

    def _load_existing_aspirations(self):
        """Laad bestaande aspiraties"""

        # Load life aspirations
        aspirations_file = self.aspirations_dir / "aspirations.json"
        if aspirations_file.exists():
            try:
                with open(aspirations_file, 'r', encoding='utf-8') as f:
                    aspirations_data = json.load(f)
                    self.life_aspirations = {
                        aspiration_id: LifeAspiration(**data)
                        for aspiration_id, data in aspirations_data.items()
                    }
            except Exception as e:
                logger.warning(f"Kon aspiraties niet laden: {e}")

        # Load aspiration clusters
        clusters_file = self.aspirations_dir / "clusters.json"
        if clusters_file.exists():
            try:
                with open(clusters_file, 'r', encoding='utf-8') as f:
                    clusters_data = json.load(f)
                    self.aspiration_clusters = {
                        cluster_id: AspirationCluster(**data)
                        for cluster_id, data in clusters_data.items()
                    }
            except Exception as e:
                logger.warning(f"Kon aspiratie clusters niet laden: {e}")

    def save_aspirations_state(self):
        """Sla aspiraties staat op"""

        # Save life aspirations
        aspirations_data = {
            aspiration_id: asdict(aspiration)
            for aspiration_id, aspiration in self.life_aspirations.items()
        }

        with open(self.aspirations_dir / "aspirations.json", 'w', encoding='utf-8') as f:
            json.dump(aspirations_data, f, indent=2, ensure_ascii=False, default=str)

        # Save aspiration clusters
        clusters_data = {
            cluster_id: asdict(cluster)
            for cluster_id, cluster in self.aspiration_clusters.items()
        }

        with open(self.aspirations_dir / "clusters.json", 'w', encoding='utf-8') as f:
            json.dump(clusters_data, f, indent=2, ensure_ascii=False, default=str)
