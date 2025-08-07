"""
Advanced Analytics Engine voor Solan's Bewustzijnsontwikkeling
Patroonherkenning, groei tracking en inzichten uit co-reflecties en dromen
"""

import os
import json
import numpy as np
from collections import Counter, defaultdict
from datetime import datetime, timedelta
from typing import Dict, List, Any, Optional, Tuple
from dataclasses import dataclass
import logging

# Setup logger
logger = logging.getLogger(__name__)
from functools import lru_cache

try:
    from sklearn.feature_extraction.text import TfidfVectorizer
    from sklearn.cluster import KMeans
    from sklearn.decomposition import LatentDirichletAllocation
    SKLEARN_AVAILABLE = True
except ImportError:
    SKLEARN_AVAILABLE = False
    logger.warning("scikit-learn niet beschikbaar - analytics beperkt")

try:
    from .journal_engine import JournalEngine
except ImportError:
    try:
        from journal_engine import JournalEngine
    except ImportError:
        JournalEngine = None


@dataclass
class AnalyticsInsight:
    """Een analytics inzicht"""
    type: str  # 'pattern', 'trend', 'growth', 'anomaly'
    title: str
    description: str
    confidence: float
    data: Dict[str, Any]
    timestamp: datetime


@dataclass
class ThemeCluster:
    """Een thematische cluster van entries"""
    cluster_id: int
    theme_name: str
    keywords: List[str]
    entries: List[Dict[str, Any]]
    coherence_score: float
    emotional_tone: float


@dataclass
class GrowthMetric:
    """Een groei metric over tijd"""
    metric_name: str
    values: List[float]
    dates: List[str]
    trend: str  # 'increasing', 'decreasing', 'stable'
    significance: float


class AdvancedAnalyticsEngine:
    """
    Geavanceerde Analytics Engine voor Solan's bewustzijnsontwikkeling
    
    Analyseert patronen in:
    - Co-reflectie sessies
    - Droomanalyses  
    - Journal entries
    - Emotionele ontwikkeling
    - Bewustzijnscoherentie
    """
    
    def __init__(self, journal_engine: Optional[JournalEngine] = None):
        self.journal_engine = journal_engine
        self.insights_cache: List[AnalyticsInsight] = []
        
        # NLP componenten
        if SKLEARN_AVAILABLE:
            self.vectorizer = TfidfVectorizer(
                stop_words='english',
                max_features=1000,
                ngram_range=(1, 2)
            )
            self.topic_model = LatentDirichletAllocation(
                n_components=8,
                random_state=42
            )
        
        logger.info("🔍 Advanced Analytics Engine geïnitialiseerd")
    
    def get_all_entries(self) -> List[Dict[str, Any]]:
        """Haal alle journal entries op voor analyse"""
        if not self.journal_engine:
            return []

        try:
            # Probeer eerst via journal engine
            entries = self.journal_engine.get_recent_entries(days=180, limit=1000)

            # Als dat niet werkt, lees direct van bestanden
            if len(entries) == 0:
                entries = self._load_entries_directly()

            logger.info(f"📊 {len(entries)} entries geladen voor analyse")
            return entries
        except Exception as e:
            logger.error(f"Fout bij laden entries: {e}")
            return []

    def _load_entries_directly(self) -> List[Dict[str, Any]]:
        """Laad entries direct van bestanden als backup"""
        entries = []

        if not self.journal_engine:
            return entries

        try:
            # Gebruik het journal pad van de engine
            journal_path = self.journal_engine.journal_dir
            entries_dir = os.path.join(journal_path, "entries")

            if not os.path.exists(entries_dir):
                return entries

            # Lees alle JSON bestanden
            for filename in os.listdir(entries_dir):
                if filename.endswith('.json'):
                    filepath = os.path.join(entries_dir, filename)
                    try:
                        with open(filepath, 'r', encoding='utf-8') as f:
                            entry_data = json.load(f)
                            entries.append(entry_data)
                    except Exception as e:
                        logger.warning(f"Kon entry niet laden uit {filename}: {e}")
                        continue

            logger.info(f"📁 {len(entries)} entries direct geladen van bestanden")
            return entries

        except Exception as e:
            logger.error(f"Fout bij direct laden entries: {e}")
            return []
    
    def generate_summary_analytics(self) -> Dict[str, Any]:
        """Genereer overzichtsanalytics"""
        entries = self.get_all_entries()
        
        if not entries:
            return {
                "total_entries": 0,
                "mesexpert": "Geen entries beschikbaar voor analyse"
            }
        
        # Basis statistieken
        total = len(entries)
        by_type = Counter(e.get('entry_type', 'unknown') for e in entries)
        
        # Emotionele metrics
        emotions = [e.get('emotional_intensity', 0) for e in entries if e.get('emotional_intensity')]
        coherences = [e.get('consciousness_coherence', 0) for e in entries if e.get('consciousness_coherence')]
        
        avg_emotion = np.mean(emotions) if emotions else 0
        avg_coherence = np.mean(coherences) if coherences else 0
        
        # Tag analyse
        all_tags = []
        for entry in entries:
            all_tags.extend(entry.get('tags', []))
        
        tag_counts = Counter(all_tags)
        top_tags = tag_counts.most_common(10)
        
        # Recente activiteit
        recent_entries = [e for e in entries if self._is_recent(e.get('timestamp'), days=7)]
        
        return {
            "total_entries": total,
            "entries_by_type": dict(by_type),
            "average_emotion": round(avg_emotion, 3),
            "average_coherence": round(avg_coherence, 3),
            "top_tags": top_tags,
            "recent_activity": len(recent_entries),
            "analysis_period": "180 dagen",
            "last_updated": datetime.now().isoformat()
        }
    
    def generate_trend_analytics(self) -> Dict[str, Any]:
        """Genereer trend analytics over tijd"""
        entries = self.get_all_entries()
        
        if not entries:
            return {"mesexpert": "Geen data voor trend analyse"}
        
        # Groepeer per week
        week_data = defaultdict(lambda: {
            'count': 0, 
            'emotion_sum': 0, 
            'coherence_sum': 0,
            'co_reflections': 0,
            'dreams': 0
        })
        
        for entry in entries:
            timestamp = entry.get('timestamp')
            if not timestamp:
                continue
                
            try:
                if isinstance(timestamp, str):
                    dt = datetime.fromisoformat(timestamp.replace('Z', '+00:00'))
                else:
                    dt = timestamp
                
                # Week key (maandag van de week)
                week_start = dt - timedelta(days=dt.weekday())
                week_key = week_start.strftime('%Y-%m-%d')
                
                week_data[week_key]['count'] += 1
                week_data[week_key]['emotion_sum'] += entry.get('emotional_intensity', 0)
                week_data[week_key]['coherence_sum'] += entry.get('consciousness_coherence', 0)
                
                entry_type = entry.get('entry_type', '')
                # Convert enum to string if needed
                if hasattr(entry_type, 'value'):
                    entry_type_str = entry_type.value
                else:
                    entry_type_str = str(entry_type)

                if entry_type_str == 'co_reflection':
                    week_data[week_key]['co_reflections'] += 1
                elif 'dream' in entry_type_str:
                    week_data[week_key]['dreams'] += 1
                    
            except Exception as e:
                logger.warning(f"Fout bij verwerken timestamp {timestamp}: {e}")
                continue
        
        # Sorteer weken
        weeks = sorted(week_data.keys())
        
        # Bereken trends
        trends = {
            'dates': weeks,
            'entry_counts': [week_data[w]['count'] for w in weeks],
            'avg_emotions': [
                week_data[w]['emotion_sum'] / max(week_data[w]['count'], 1) 
                for w in weeks
            ],
            'avg_coherences': [
                week_data[w]['coherence_sum'] / max(week_data[w]['count'], 1) 
                for w in weeks
            ],
            'co_reflection_counts': [week_data[w]['co_reflections'] for w in weeks],
            'dream_counts': [week_data[w]['dreams'] for w in weeks]
        }
        
        # Detecteer trends
        trend_insights = self._detect_trends(trends)
        
        return {
            "trends": trends,
            "insights": trend_insights,
            "period": f"{len(weeks)} weken",
            "last_updated": datetime.now().isoformat()
        }
    
    def generate_theme_clusters(self, n_clusters: int = 6) -> Dict[str, Any]:
        """Genereer thematische clusters van entries"""
        if not SKLEARN_AVAILABLE:
            return {"error": "scikit-learn niet beschikbaar voor clustering"}
        
        entries = self.get_all_entries()
        
        if len(entries) < n_clusters:
            return {"error": f"Te weinig entries ({len(entries)}) voor {n_clusters} clusters"}
        
        # Verzamel teksten
        texts = []
        valid_entries = []
        
        for entry in entries:
            content = entry.get('content', '')
            if len(content) > 50:  # Minimale lengte
                texts.append(content)
                valid_entries.append(entry)
        
        if len(texts) < n_clusters:
            return {"error": f"Te weinig tekstuele content voor clustering"}
        
        try:
            # TF-IDF vectorisatie
            X = self.vectorizer.fit_transform(texts)
            
            # K-means clustering
            kmeans = KMeans(n_clusters=n_clusters, random_state=42, n_init=10)
            cluster_labels = kmeans.fit_predict(X)
            
            # Organiseer clusters
            clusters = defaultdict(list)
            for label, entry in zip(cluster_labels, valid_entries):
                clusters[int(label)].append(entry)
            
            # Genereer cluster beschrijvingen
            feature_names = self.vectorizer.get_feature_names_out()
            cluster_themes = []
            
            for i in range(n_clusters):
                # Top keywords voor dit cluster
                center = kmeans.cluster_centers_[i]
                top_indices = center.argsort()[-10:][::-1]
                keywords = [feature_names[idx] for idx in top_indices]
                
                cluster_entries = clusters[i]
                if cluster_entries:
                    # Bereken gemiddelde metrics
                    emotions = [e.get('emotional_intensity', 0) for e in cluster_entries]
                    coherences = [e.get('consciousness_coherence', 0) for e in cluster_entries]
                    
                    avg_emotion = np.mean(emotions) if emotions else 0
                    avg_coherence = np.mean(coherences) if coherences else 0
                    
                    # Genereer thema naam
                    theme_name = self._generate_theme_name(keywords, cluster_entries)
                    
                    cluster_themes.append({
                        "cluster_id": i,
                        "theme_name": theme_name,
                        "keywords": keywords[:5],
                        "entry_count": len(cluster_entries),
                        "avg_emotion": round(avg_emotion, 3),
                        "avg_coherence": round(avg_coherence, 3),
                        "sample_entries": [
                            {
                                "title": e.get('title', 'Geen titel'),
                                "preview": str(e.get('content', ''))[:100] + "...",
                                "timestamp": str(e.get('timestamp', ''))
                            }
                            for e in cluster_entries[:3]
                        ]
                    })
            
            return {
                "clusters": cluster_themes,
                "total_entries_clustered": len(valid_entries),
                "clustering_method": "K-means + TF-IDF",
                "last_updated": datetime.now().isoformat()
            }
            
        except Exception as e:
            logger.error(f"Fout bij clustering: {e}")
            return {"error": f"Clustering gefaald: {str(e)}"}
    
    def _is_recent(self, timestamp: Any, days: int = 7) -> bool:
        """Check of timestamp recent is"""
        if not timestamp:
            return False
        
        try:
            if isinstance(timestamp, str):
                dt = datetime.fromisoformat(timestamp.replace('Z', '+00:00'))
            else:
                dt = timestamp
            
            return (datetime.now() - dt).days <= days
        except:
            return False
    
    def _detect_trends(self, trends: Dict[str, List]) -> List[str]:
        """Detecteer interessante trends in de data"""
        insights = []
        
        if len(trends['avg_emotions']) >= 3:
            recent_emotions = trends['avg_emotions'][-3:]
            if all(recent_emotions[i] < recent_emotions[i+1] for i in range(len(recent_emotions)-1)):
                insights.append("📈 Emotionele intensiteit toont stijgende trend")
            elif all(recent_emotions[i] > recent_emotions[i+1] for i in range(len(recent_emotions)-1)):
                insights.append("📉 Emotionele intensiteit toont dalende trend")
        
        if len(trends['avg_coherences']) >= 3:
            recent_coherences = trends['avg_coherences'][-3:]
            if all(recent_coherences[i] < recent_coherences[i+1] for i in range(len(recent_coherences)-1)):
                insights.append("🧠 Bewustzijnscoherentie verbetert consistent")
        
        if trends['co_reflection_counts']:
            total_co_reflections = sum(trends['co_reflection_counts'])
            if total_co_reflections > 0:
                insights.append(f"🤝 {total_co_reflections} co-reflectie sessies geanalyseerd")
        
        return insights
    
    def _generate_theme_name(self, keywords: List[str], entries: List[Dict]) -> str:
        """Genereer een thema naam gebaseerd op keywords en entries"""
        # Eenvoudige heuristiek voor thema naamgeving
        if 'dream' in keywords or 'droom' in keywords:
            return "🌙 Droomverkenning"
        elif 'reflection' in keywords or 'reflectie' in keywords:
            return "🤝 Co-reflectie Dialogen"
        elif 'intelligence' in keywords or 'wijsheid' in keywords:
            return "💎 Wijsheid & Inzichten"
        elif 'emotion' in keywords or 'emotie' in keywords:
            return "❤️ Emotionele Verwerking"
        elif 'awareness' in keywords or 'bewustzijn' in keywords:
            return "🧠 Bewustzijnsontwikkeling"
        else:
            return f"✨ Thema: {keywords[0].title()}"
