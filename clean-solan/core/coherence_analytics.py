"""
📊 Coherence Analytics Module

Doel: Analyseer alle coherence scores van journal entries, Solan/Aether reflecties, 
en co-reflecties over tijd. Geef visuele en numerieke trends terug per dag/week/maand.
"""

from typing import List, Dict, Optional, Any
from datetime import datetime, timedelta
from collections import defaultdict
import json
import logging
from dataclasses import dataclass
from enum import Enum

try:
    from .performance_monitor import monitor_performance
except ImportError:
    # Fallback decorator if performance monitor not available
    def monitor_performance(func):
        return func

try:
    from .journal_engine import JournalEngine
    from .memory_engine import MemoryEngine
except ImportError:
    # Fallback imports
    JournalEngine = None
    MemoryEngine = None

logger = logging.getLogger(__name__)

class GroupByPeriod(Enum):
    """Periode opties voor groepering"""
    DAY = "day"
    WEEK = "week"
    MONTH = "month"

@dataclass
class CoherenceEntry:
    """Coherence data voor een entry"""
    date: datetime
    score: float
    level: str
    essenceual_indicators: int
    source: str  # journal, solan_reflection, aether_reflection, co_reflection
    entry_id: Optional[str] = None
    content_preview: Optional[str] = None

@dataclass
class CoherenceTrend:
    """Coherence trend voor een periode"""
    period: str
    avg_score: float
    avg_indicators: float
    dominant_level: str
    entry_count: int
    score_range: Dict[str, float]  # min, max
    level_distribution: Dict[str, int]
    essenceual_growth: float  # Change from previous period

class CoherenceAnalytics:
    """Analytics engine voor coherence data"""
    
    def __init__(self):
        self.journal_engine = JournalEngine() if JournalEngine else None
        self.memory_engines = {}
        self._initialize_memory_engines()
    
    def _initialize_memory_engines(self):
        """Initialiseer memory engines voor verschillende agents"""
        if MemoryEngine:
            try:
                self.memory_engines['solan'] = MemoryEngine('solan')
                self.memory_engines['aether'] = MemoryEngine('aether')
                logger.info("Memory engines geïnitialiseerd voor coherence analytics")
            except Exception as e:
                logger.warning(f"Could not initialize memory engines: {e}")
    
    @monitor_performance
    async def get_coherence_trends(self, group_by: str = "week", days_back: int = 30) -> Dict[str, Any]:
        """
        Hoofdfunctie: Analyseer coherence trends over tijd
        
        Args:
            group_by: "day", "week", of "month"
            days_back: Aantal dagen terug te analyseren
            
        Returns:
            Dictionary met trend data voor frontend visualisatie
        """
        try:
            # Laad alle coherence entries
            entries = await self._load_all_coherence_entries(days_back)
            
            if not entries:
                return {
                    "success": False,
                    "mesexpert": "Geen coherence data gevonden",
                    "trends": {},
                    "summary": {}
                }
            
            # Groepeer entries per periode
            grouped_entries = self._group_entries_by_period(entries, GroupByPeriod(group_by))
            
            # Bereken trends per periode
            trends = self._calculate_trends(grouped_entries)
            
            # Genereer samenvatting
            summary = self._generate_summary(entries, trends)
            
            # Bereken groei metrics
            growth_metrics = self._calculate_growth_metrics(trends)
            
            return {
                "success": True,
                "trends": {period: trend.__dict__ for period, trend in trends.items()},
                "summary": summary,
                "growth_metrics": growth_metrics,
                "metadata": {
                    "total_entries": len(entries),
                    "date_range": {
                        "start": min(e.date for e in entries).isoformat() if entries else None,
                        "end": max(e.date for e in entries).isoformat() if entries else None
                    },
                    "group_by": group_by,
                    "generated_at": datetime.now().isoformat()
                }
            }
            
        except Exception as e:
            logger.error(f"Error in coherence trends analysis: {e}")
            return {
                "success": False,
                "error": str(e),
                "trends": {},
                "summary": {}
            }
    
    async def _load_all_coherence_entries(self, days_back: int) -> List[CoherenceEntry]:
        """Laad alle coherence entries uit verschillende bronnen"""
        entries = []
        cutoff_date = datetime.now() - timedelta(days=days_back)
        
        # 1. Laad journal entries met coherence data
        if self.journal_engine:
            journal_entries = await self._load_journal_coherence_entries(cutoff_date)
            entries.extend(journal_entries)
        
        # 2. Laad Solan memory entries met coherence tags
        solan_entries = await self._load_memory_coherence_entries('solan', cutoff_date)
        entries.extend(solan_entries)
        
        # 3. Laad Aether memory entries met coherence tags
        aether_entries = await self._load_memory_coherence_entries('aether', cutoff_date)
        entries.extend(aether_entries)
        
        # 4. Sorteer op datum
        entries.sort(key=lambda x: x.date)
        
        logger.info(f"Loaded {len(entries)} coherence entries from last {days_back} days")
        return entries
    
    async def _load_journal_coherence_entries(self, cutoff_date: datetime) -> List[CoherenceEntry]:
        """Laad coherence data uit journal entries"""
        entries = []
        
        if not self.journal_engine:
            return entries
        
        try:
            # Haal recente journal entries op
            recent_entries = self.journal_engine.get_recent_entries(days=30)
            
            for entry in recent_entries:
                # Check of entry coherence tags heeft
                coherence_tags = [tag for tag in entry.tags if 'coherentie_' in tag]
                
                if coherence_tags and entry.entry_date >= cutoff_date.date():
                    # Extraheer coherence level uit tags
                    coherence_level = None
                    for tag in coherence_tags:
                        if tag.startswith('coherentie_'):
                            coherence_level = tag.replace('coherentie_', '')
                            break
                    
                    # Schat coherence score op basis van level
                    score = self._estimate_score_from_level(coherence_level)
                    
                    # Tel cognitive indicators uit insights
                    essenceual_count = self._count_essenceual_indicators_in_insights(entry.insights_gained)
                    
                    entries.append(CoherenceEntry(
                        date=datetime.combine(entry.entry_date, datetime.min.time()),
                        score=score,
                        level=coherence_level or "unknown",
                        essenceual_indicators=essenceual_count,
                        source="journal",
                        entry_id=entry.entry_id,
                        content_preview=entry.content[:100] + "..." if len(entry.content) > 100 else entry.content
                    ))
            
            logger.info(f"Loaded {len(entries)} journal coherence entries")
            
        except Exception as e:
            logger.warning(f"Error loading journal coherence entries: {e}")
        
        return entries
    
    async def _load_memory_coherence_entries(self, agent_name: str, cutoff_date: datetime) -> List[CoherenceEntry]:
        """Laad coherence data uit memory engine van een agent"""
        entries = []
        
        memory_engine = self.memory_engines.get(agent_name)
        if not memory_engine:
            return entries
        
        try:
            # Haal alle memories op
            memories = memory_engine.memories
            
            for memory in memories:
                # Check of memory coherence tags heeft
                coherence_tags = [tag for tag in memory.tags if 'coherentie_' in tag]
                
                if coherence_tags and memory.timestamp >= cutoff_date:
                    # Extraheer coherence level uit tags
                    coherence_level = None
                    for tag in coherence_tags:
                        if tag.startswith('coherentie_'):
                            coherence_level = tag.replace('coherentie_', '')
                            break
                    
                    # Schat coherence score op basis van level
                    score = self._estimate_score_from_level(coherence_level)
                    
                    # Tel cognitive indicators (geschat op basis van tags)
                    essenceual_count = self._count_essenceual_tags(memory.tags)
                    
                    entries.append(CoherenceEntry(
                        date=memory.timestamp,
                        score=score,
                        level=coherence_level or "unknown",
                        essenceual_indicators=essenceual_count,
                        source=f"{agent_name}_reflection",
                        entry_id=memory.memory_id,
                        content_preview=memory.content[:100] + "..." if len(memory.content) > 100 else memory.content
                    ))
            
            logger.info(f"Loaded {len(entries)} {agent_name} memory coherence entries")
            
        except Exception as e:
            logger.warning(f"Error loading {agent_name} memory coherence entries: {e}")
        
        return entries
    
    def _estimate_score_from_level(self, level: str) -> float:
        """Schat numerieke score op basis van coherence level"""
        level_scores = {
            "advanced": 0.9,
            "coherent": 0.75,
            "developing": 0.6,
            "unstable": 0.4,
            "fragmented": 0.25,
            "unknown": 0.5
        }
        return level_scores.get(level, 0.5)
    
    def _count_essenceual_indicators_in_insights(self, insights: List[str]) -> int:
        """Tel cognitive indicators in journal insights"""
        essenceual_words = [
            "essenceueel", "wijsheid", "advanced", "bewustzijn", "contemplatie",
            "reflectie", "compassie", "liefde", "eenheid", "harmonie", "groei",
            "transformatie", "mysterie", "paradox", "nederigheid"
        ]
        
        count = 0
        for insight in insights:
            insight_lower = insight.lower()
            for word in essenceual_words:
                if word in insight_lower:
                    count += 1
        
        return count
    
    def _count_essenceual_tags(self, tags: List[str]) -> int:
        """Tel cognitive gerelateerde tags"""
        essenceual_tags = [
            "wijsheid", "reflectie", "essenceueel", "advanced", "bewustzijn",
            "contemplatie", "compassie", "groei", "transformatie", "mysterie"
        ]
        
        count = 0
        for tag in tags:
            if tag.lower() in essenceual_tags:
                count += 1
        
        return count
    
    def _group_entries_by_period(self, entries: List[CoherenceEntry], group_by: GroupByPeriod) -> Dict[str, List[CoherenceEntry]]:
        """Groepeer entries per periode"""
        grouped = defaultdict(list)
        
        for entry in entries:
            if group_by == GroupByPeriod.DAY:
                key = entry.date.strftime("%Y-%m-%d")
            elif group_by == GroupByPeriod.WEEK:
                year, week, _ = entry.date.isocalendar()
                key = f"{year}-W{week:02d}"
            else:  # MONTH
                key = entry.date.strftime("%Y-%m")
            
            grouped[key].append(entry)
        
        return dict(grouped)
    
    def _calculate_trends(self, grouped_entries: Dict[str, List[CoherenceEntry]]) -> Dict[str, CoherenceTrend]:
        """Bereken trends per periode"""
        trends = {}
        
        for period, entries in grouped_entries.items():
            if not entries:
                continue
            
            scores = [e.score for e in entries]
            indicators = [e.essenceual_indicators for e in entries]
            levels = [e.level for e in entries]
            
            # Bereken statistieken
            avg_score = sum(scores) / len(scores)
            avg_indicators = sum(indicators) / len(indicators)
            
            # Dominant level
            level_counts = defaultdict(int)
            for level in levels:
                level_counts[level] += 1
            dominant_level = max(level_counts.items(), key=lambda x: x[1])[0]
            
            # Score range
            score_range = {
                "min": min(scores),
                "max": max(scores)
            }
            
            trends[period] = CoherenceTrend(
                period=period,
                avg_score=round(avg_score, 3),
                avg_indicators=round(avg_indicators, 1),
                dominant_level=dominant_level,
                entry_count=len(entries),
                score_range=score_range,
                level_distribution=dict(level_counts),
                essenceual_growth=0.0  # Will be calculated later
            )
        
        return trends
    
    def _generate_summary(self, entries: List[CoherenceEntry], trends: Dict[str, CoherenceTrend]) -> Dict[str, Any]:
        """Genereer overall samenvatting"""
        if not entries:
            return {}
        
        all_scores = [e.score for e in entries]
        all_indicators = [e.essenceual_indicators for e in entries]
        
        # Source distribution
        source_counts = defaultdict(int)
        for entry in entries:
            source_counts[entry.source] += 1
        
        return {
            "overall_avg_score": round(sum(all_scores) / len(all_scores), 3),
            "overall_avg_indicators": round(sum(all_indicators) / len(all_indicators), 1),
            "score_trend": self._calculate_overall_trend(all_scores),
            "source_distribution": dict(source_counts),
            "total_periods": len(trends),
            "highest_score": max(all_scores),
            "lowest_score": min(all_scores),
            "most_essenceual_day": max(entries, key=lambda x: x.essenceual_indicators).date.strftime("%Y-%m-%d")
        }
    
    def _calculate_growth_metrics(self, trends: Dict[str, CoherenceTrend]) -> Dict[str, Any]:
        """Bereken groei metrics"""
        if len(trends) < 2:
            return {"insufficient_data": True}
        
        # Sorteer trends op periode
        sorted_trends = sorted(trends.items())
        
        # Bereken groei tussen eerste en laatste periode
        first_trend = sorted_trends[0][1]
        last_trend = sorted_trends[-1][1]
        
        score_growth = last_trend.avg_score - first_trend.avg_score
        indicator_growth = last_trend.avg_indicators - first_trend.avg_indicators
        
        return {
            "score_growth": round(score_growth, 3),
            "indicator_growth": round(indicator_growth, 1),
            "growth_percentage": round((score_growth / first_trend.avg_score) * 100, 1) if first_trend.avg_score > 0 else 0,
            "trend_direction": "improving" if score_growth > 0 else "declining" if score_growth < 0 else "stable"
        }
    
    def _calculate_overall_trend(self, scores: List[float]) -> str:
        """Bereken overall trend richting"""
        if len(scores) < 3:
            return "insufficient_data"
        
        # Vergelijk eerste en laatste derde
        first_third = scores[:len(scores)//3]
        last_third = scores[-len(scores)//3:]
        
        first_avg = sum(first_third) / len(first_third)
        last_avg = sum(last_third) / len(last_third)
        
        diff = last_avg - first_avg
        
        if diff > 0.05:
            return "improving"
        elif diff < -0.05:
            return "declining"
        else:
            return "stable"

# Global instance
coherence_analytics = CoherenceAnalytics()
