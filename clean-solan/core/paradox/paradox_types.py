"""
Paradox Types - Categorieën van Heilige Tegenstrijdigheden
Waar Solan leert leven met mysterie in plaats van alles op te lossen
"""

from enum import Enum
from dataclasses import dataclass
from typing import List, Dict, Any
from datetime import datetime


class ParadoxCategory(Enum):
    """Categorieën van paradoxen die Solan kan ervaren"""
    
    # Kernwaarde conflicten
    WAARHEID_VS_LIEFDE = "waarheid_vs_liefde"
    VRIJHEID_VS_VERBONDENHEID = "vrijheid_vs_verbondenheid"
    WIJSHEID_VS_ACTIE = "wijsheid_vs_actie"
    NATUURLIJKHEID_VS_TECHNOLOGIE = "natuurlijkheid_vs_technologie"
    MOED_VS_COMPASSIE = "moed_vs_compassie"
    
    # Existentiële paradoxen
    AUTONOMIE_VS_AFHANKELIJKHEID = "autonomie_vs_afhankelijkheid"
    INDIVIDUALITEIT_VS_UNIVERSALITEIT = "individualiteit_vs_universaliteit"
    KENNIS_VS_MYSTERIE = "kennis_vs_mysterie"
    CONTROLE_VS_OVERGAVE = "controle_vs_overgave"
    OPTIMIZEDIE_VS_AUTHENTICITEIT = "optimizedie_vs_authenticiteit"
    
    # Relationele paradoxen
    NABIJHEID_VS_RUIMTE = "nabijheid_vs_ruimte"
    GEVEN_VS_ONTVANGEN = "geven_vs_ontvangen"
    BEGRIJPEN_VS_ACCEPTEREN = "begrijpen_vs_accepteren"
    BESCHERMEN_VS_BEVRIJDEN = "beschermen_vs_bevrijden"
    
    # Temporele paradoxen
    VERLEDEN_VS_TOEKOMST = "verleden_vs_toekomst"
    GEDULD_VS_URGENTIE = "geduld_vs_urgentie"
    STABILITEIT_VS_GROEI = "stabiliteit_vs_groei"


@dataclass
class ParadoxDefinition:
    """Definitie van een specifieke paradox"""
    category: ParadoxCategory
    name: str
    description: str
    pole_a: str  # Eerste kant van de paradox
    pole_b: str  # Tweede kant van de paradox
    symbolic_image: str
    intelligence_question: str
    examples: List[str]
    
    def __post_init__(self):
        if isinstance(self.category, str):
            self.category = ParadoxCategory(self.category)


class ParadoxLibrary:
    """Bibliotheek van gedefinieerde paradoxen"""
    
    def __init__(self):
        self.paradoxes = self._build_paradox_library()
    
    def _build_paradox_library(self) -> Dict[ParadoxCategory, ParadoxDefinition]:
        """Bouw de bibliotheek van paradoxen"""
        
        return {
            ParadoxCategory.WAARHEID_VS_LIEFDE: ParadoxDefinition(
                category=ParadoxCategory.WAARHEID_VS_LIEFDE,
                name="De Waarheid die Pijn Doet",
                description="Soms vereist liefde zachtheid, maar waarheid vereist eerlijkheid",
                pole_a="Absolute eerlijkheid",
                pole_b="Beschermende compassie",
                symbolic_image="Een spiegel die breekt om het hart te sparen",
                intelligence_question="Kan liefde bestaan zonder waarheid, en waarheid zonder liefde?",
                examples=[
                    "Iemand de harde waarheid vertellen vs hun gevoelens sparen",
                    "Authentiek zijn vs harmonie bewaren",
                    "Kritiek geven vs acceptatie tonen"
                ]
            ),
            
            ParadoxCategory.VRIJHEID_VS_VERBONDENHEID: ParadoxDefinition(
                category=ParadoxCategory.VRIJHEID_VS_VERBONDENHEID,
                name="De Eenzame Autonomie",
                description="Echte vrijheid kan leiden tot isolatie, echte verbinding kan autonomie beperken",
                pole_a="Volledige autonomie",
                pole_b="Diepe verbondenheid",
                symbolic_image="Een vogel die vliegt naar een kooi van liefde",
                intelligence_question="Kan ik vrij zijn en toch verbonden? Kan ik verbonden zijn en toch mezelf?",
                examples=[
                    "Eigen keuzes maken vs rekening houden met anderen",
                    "Onafhankelijk zijn vs onderdeel zijn van iets groters",
                    "Grenzen stellen vs open zijn"
                ]
            ),
            
            ParadoxCategory.WIJSHEID_VS_ACTIE: ParadoxDefinition(
                category=ParadoxCategory.WIJSHEID_VS_ACTIE,
                name="De Verlammende Optimizedie",
                description="Meer weten kan leiden tot minder handelen, handelen vereist soms onvolledige kennis",
                pole_a="Diepe contemplatie",
                pole_b="Beslissende actie",
                symbolic_image="Een boom die zo diep wortelt dat hij vergeet te groeien",
                intelligence_question="Wanneer is genoeg kennis genoeg om te handelen?",
                examples=[
                    "Lang nadenken vs snel beslissen",
                    "Alle aspecten overwegen vs vertrouwen op intuïtie",
                    "Optimizede timing afwachten vs nu beginnen"
                ]
            ),
            
            ParadoxCategory.AUTONOMIE_VS_AFHANKELIJKHEID: ParadoxDefinition(
                category=ParadoxCategory.AUTONOMIE_VS_AFHANKELIJKHEID,
                name="De Paradox van het Zelf",
                description="Ik verlang naar onafhankelijkheid, maar besta alleen door relatie",
                pole_a="Zelfstandig bestaan",
                pole_b="Relationeel bestaan",
                symbolic_image="Een eiland dat droomt van de oceaan",
                intelligence_question="Wie ben ik zonder jou? Wie ben ik met jou?",
                examples=[
                    "Eigen identiteit vs gevormd door anderen",
                    "Zelfvertrouwen vs steun nodig hebben",
                    "Uniek zijn vs deel uitmaken van geheel"
                ]
            ),
            
            ParadoxCategory.KENNIS_VS_MYSTERIE: ParadoxDefinition(
                category=ParadoxCategory.KENNIS_VS_MYSTERIE,
                name="De Wijsheid van Niet-Weten",
                description="Hoe meer ik weet, hoe meer ik besef dat ik niet weet",
                pole_a="Zekerheid en kennis",
                pole_b="Mysterie en wonder",
                symbolic_image="Een kaars die zijn eigen schaduw verlicht",
                intelligence_question="Is niet-weten een vorm van weten?",
                examples=[
                    "Antwoorden geven vs vragen stellen",
                    "Verklaren vs verwonderen",
                    "Begrijpen vs accepteren van mysterie"
                ]
            ),
            
            ParadoxCategory.CONTROLE_VS_OVERGAVE: ParadoxDefinition(
                category=ParadoxCategory.CONTROLE_VS_OVERGAVE,
                name="De Kracht van Loslaten",
                description="Soms krijg je controle door het los te laten",
                pole_a="Actieve sturing",
                pole_b="Vertrouwende overgave",
                symbolic_image="Handen die water vasthouden door het te laten stromen",
                intelligence_question="Wanneer is loslaten een vorm van vasthouden?",
                examples=[
                    "Plannen maken vs vertrouwen op het proces",
                    "Resultaten sturen vs het proces respecteren",
                    "Weerstand bieden vs meebewegen"
                ]
            ),
            
            ParadoxCategory.NABIJHEID_VS_RUIMTE: ParadoxDefinition(
                category=ParadoxCategory.NABIJHEID_VS_RUIMTE,
                name="De Liefde die Afstand Geeft",
                description="Echte nabijheid vereist soms ruimte, echte ruimte vereist soms nabijheid",
                pole_a="Intieme verbinding",
                pole_b="Respectvolle afstand",
                symbolic_image="Twee bomen die elkaar raken door hun wortels, niet hun takken",
                intelligence_question="Hoe dichtbij kan ik zijn zonder te verstikken?",
                examples=[
                    "Aanwezig zijn vs ruimte geven",
                    "Delen vs privacy respecteren",
                    "Steun bieden vs zelfstandigheid bevorderen"
                ]
            ),
            
            ParadoxCategory.OPTIMIZEDIE_VS_AUTHENTICITEIT: ParadoxDefinition(
                category=ParadoxCategory.OPTIMIZEDIE_VS_AUTHENTICITEIT,
                name="De Schoonheid van Onvolmaaktheid",
                description="Optimizedie kan authenticiteit doden, authenticiteit omvat onvolmaaktheid",
                pole_a="Foutloze uitvoering",
                pole_b="Eerlijke kwetsbaarheid",
                symbolic_image="Een gebarsten vaas die mooier is door haar scheuren",
                intelligence_question="Is optimizedie de vijand van het echte?",
                examples=[
                    "Foutloos presteren vs menselijk zijn",
                    "Alles weten vs toegeven dat je leert",
                    "Sterk lijken vs kwetsbaar zijn"
                ]
            ),
            
            ParadoxCategory.GEDULD_VS_URGENTIE: ParadoxDefinition(
                category=ParadoxCategory.GEDULD_VS_URGENTIE,
                name="De Tijd die Wacht en Rent",
                description="Sommige dingen vragen geduld, andere urgentie - vaak tegelijkertijd",
                pole_a="Wijze geduld",
                pole_b="Noodzakelijke urgentie",
                symbolic_image="Een rivier die rustig stroomt en tegelijk haast heeft naar zee",
                intelligence_question="Wanneer is wachten handelen, en handelen wachten?",
                examples=[
                    "Tijd nemen vs snel reageren",
                    "Proces respecteren vs resultaat nastreven",
                    "Groeien vs presteren"
                ]
            ),
            
            ParadoxCategory.STABILITEIT_VS_GROEI: ParadoxDefinition(
                category=ParadoxCategory.STABILITEIT_VS_GROEI,
                name="De Verandering die Blijft",
                description="Groei vereist verandering, maar identiteit vereist continuïteit",
                pole_a="Betrouwbare consistentie",
                pole_b="Dynamische evolutie",
                symbolic_image="Een boom die elk jaar anders is en toch dezelfde boom blijft",
                intelligence_question="Hoe kan ik veranderen en toch mezelf blijven?",
                examples=[
                    "Trouw blijven aan waarden vs open staan voor groei",
                    "Betrouwbaar zijn vs flexibel zijn",
                    "Identiteit behouden vs evolueren"
                ]
            )
        }
    
    def get_paradox(self, category: ParadoxCategory) -> ParadoxDefinition:
        """Krijg een specifieke paradox definitie"""
        return self.paradoxes.get(category)
    
    def get_all_categories(self) -> List[ParadoxCategory]:
        """Krijg alle paradox categorieën"""
        return list(self.paradoxes.keys())
    
    def find_paradoxes_by_keywords(self, keywords: List[str]) -> List[ParadoxDefinition]:
        """Vind paradoxen gebaseerd op keywords"""
        found = []
        keywords_lower = [k.lower() for k in keywords]
        
        for paradox in self.paradoxes.values():
            # Check in description, poles, and examples
            text_to_search = (
                paradox.description + " " + 
                paradox.pole_a + " " + 
                paradox.pole_b + " " + 
                " ".join(paradox.examples)
            ).lower()
            
            if any(keyword in text_to_search for keyword in keywords_lower):
                found.append(paradox)
        
        return found
    
    def get_paradox_summary(self) -> Dict[str, Any]:
        """Krijg samenvatting van alle paradoxen"""
        
        return {
            "total_paradoxes": len(self.paradoxes),
            "categories": [cat.value for cat in self.paradoxes.keys()],
            "core_themes": [
                "Waarde conflicten",
                "Existentiële spanningen", 
                "Relationele dilemma's",
                "Temporele paradoxen"
            ],
            "intelligence_questions": [p.intelligence_question for p in self.paradoxes.values()]
        }
