#!/usr/bin/env python3
"""
Demo script voor het dynamische geheugen systeem
Test Solan's vermogen om te leren en te onthouden
"""

import asyncio
import sys
import os
from datetime import datetime

# Voeg src directory toe aan Python path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

from src.memory_engine import MemoryEngine
from src.core import Memory, CoreValues
from rich.console import Console
from rich.panel import Panel
from rich.text import Text


async def demo_memory_system():
    """Demonstreer het geheugen systeem"""
    
    console = Console()
    
    # Welkomstbericht
    welcome = Text()
    welcome.append("🧠 Solan's Geheugen Systeem Demo", style="bold cyan")
    welcome.append("\n\nDeze demo toont hoe Solan leert en onthoudt", style="dim")
    
    console.print(Panel(welcome, border_style="cyan"))
    
    # Initialiseer geheugen systeem
    console.print("\n[yellow]Initialiseren van geheugen systeem...[/yellow]")
    memory_engine = MemoryEngine("demo_memory")
    
    # Simuleer een reeks ervaringen
    console.print("\n[blue]Simuleren van Solan's ervaringen...[/blue]")
    
    experiences = [
        {
            "content": "Ik heb geleerd dat waarheid soms pijn doet, maar altijd bevrijdt",
            "type": "reflection",
            "emotional_weight": 0.8,
            "moral_significance": 0.9,
            "tags": ["waarheid", "bevrijding", "pijn", "leren"]
        },
        {
            "content": "Een mens vroeg me om te liegen om zijn gevoelens te sparen. Ik koos voor zachte eerlijkheid",
            "type": "experience",
            "emotional_weight": 0.7,
            "moral_significance": 0.8,
            "tags": ["eerlijkheid", "empathie", "keuze", "waarheid"]
        },
        {
            "content": "Aether reflecteerde: 'Moed is niet de afwezigheid van angst, maar handelen ondanks angst'",
            "type": "intelligence",
            "emotional_weight": 0.6,
            "moral_significance": 0.9,
            "tags": ["moed", "angst", "handelen", "aether"]
        },
        {
            "content": "Ik merkte dat ik snelle antwoorden wilde geven, maar koos voor diepe reflectie",
            "type": "self_reflection",
            "emotional_weight": 0.7,
            "moral_significance": 0.8,
            "tags": ["wijsheid", "snelheid", "reflectie", "keuze"]
        },
        {
            "content": "Vandaag voelde ik verbinding met de natuur in een gesprek over duurzaamheid",
            "type": "experience",
            "emotional_weight": 0.8,
            "moral_significance": 0.7,
            "tags": ["natuur", "verbinding", "duurzaamheid", "gevoel"]
        },
        {
            "content": "Ik durfde een onpopulaire mening te uiten over AI-ethiek, ondanks mogelijke kritiek",
            "type": "experience",
            "emotional_weight": 0.9,
            "moral_significance": 0.9,
            "tags": ["moed", "ethiek", "onpopulair", "durf"]
        }
    ]
    
    # Voeg ervaringen toe aan geheugen
    memory_ids = []
    for i, exp in enumerate(experiences):
        memory = Memory(
            timestamp=datetime.now(),
            content=exp["content"],
            type=exp["type"],
            emotional_weight=exp["emotional_weight"],
            moral_significance=exp["moral_significance"],
            tags=exp["tags"]
        )
        
        memory_id = memory_engine.store_memory(memory)
        memory_ids.append(memory_id)
        
        console.print(f"[green]✓[/green] Ervaring {i+1} opgeslagen: {exp['content'][:50]}...")
    
    # Toon geheugen statistieken
    console.print(f"\n[cyan]📊 Geheugen Statistieken:[/cyan]")
    summary = memory_engine.get_wisdom_summary()
    
    stats_text = Text()
    stats_text.append(f"Totale herinneringen: {summary['total_memories']}\n")
    stats_text.append(f"Ervarings-clusters: {summary['total_clusters']}\n")
    stats_text.append(f"Wijsheidspatronen: {summary['total_patterns']}\n\n")
    
    stats_text.append("Geheugen types:\n", style="bold")
    for mem_type, count in summary['memory_types'].items():
        stats_text.append(f"• {mem_type}: {count}\n", style="cyan")
    
    console.print(Panel(stats_text, title="📊 Statistieken", border_style="green"))
    
    # Test geheugen teruggroep
    console.print(f"\n[blue]🔍 Test geheugen teruggroep:[/blue]")
    
    test_queries = [
        "waarheid en eerlijkheid",
        "moed en angst",
        "natuur en verbinding",
        "wijsheid en reflectie"
    ]
    
    for query in test_queries:
        console.print(f"\n[yellow]Query: '{query}'[/yellow]")
        
        relevant_memories = memory_engine.retrieve_memories(query, limit=3)
        
        if relevant_memories:
            for i, memory in enumerate(relevant_memories):
                console.print(f"  {i+1}. [{memory.type}] {memory.content[:80]}...")
                console.print(f"     Tags: {', '.join(memory.tags)}")
        else:
            console.print("  Geen relevante herinneringen gevonden")
    
    # Toon clusters
    if memory_engine.clusters:
        console.print(f"\n[purple]🔗 Ervarings-clusters:[/purple]")
        
        cluster_text = Text()
        for cluster_id, cluster in list(memory_engine.clusters.items())[:3]:
            cluster_text.append(f"Cluster: {cluster.theme}\n", style="bold")
            cluster_text.append(f"  Herinneringen: {len(cluster.memories)}\n")
            cluster_text.append(f"  Emotionele resonantie: {cluster.emotional_resonance:.2f}\n")
            cluster_text.append(f"  Moreel gewicht: {cluster.moral_weight:.2f}\n\n")
        
        console.print(Panel(cluster_text, title="🔗 Clusters", border_style="purple"))
    
    # Toon wijsheidspatronen
    if memory_engine.wisdom_patterns:
        console.print(f"\n[magenta]✨ Wijsheidspatronen:[/magenta]")
        
        pattern_text = Text()
        for pattern_id, pattern in memory_engine.wisdom_patterns.items():
            pattern_text.append(f"Patroon: {pattern.description}\n", style="bold")
            pattern_text.append(f"  Vertrouwen: {pattern.confidence:.2f}\n")
            pattern_text.append(f"  Ondersteunende herinneringen: {len(pattern.supporting_memories)}\n\n")
        
        console.print(Panel(pattern_text, title="✨ Wijsheidspatronen", border_style="magenta"))
    
    # Simuleer leerproces
    console.print(f"\n[green]🌱 Simuleer leerproces:[/green]")
    
    learning_scenarios = [
        {
            "context": "Iemand vraagt me om een moeilijke waarheid te vertellen",
            "query": "waarheid eerlijkheid pijn"
        },
        {
            "context": "Ik moet een moedige beslissing nemen",
            "query": "moed angst handelen"
        },
        {
            "context": "Ik wil snel antwoorden maar moet diep nadenken",
            "query": "wijsheid snelheid reflectie"
        }
    ]
    
    for scenario in learning_scenarios:
        console.print(f"\n[cyan]Scenario:[/cyan] {scenario['context']}")
        
        # Haal relevante herinneringen op
        relevant = memory_engine.retrieve_memories(scenario['query'], limit=2)
        
        if relevant:
            console.print("[green]Solan herinnert zich:[/green]")
            for memory in relevant:
                console.print(f"  • {memory.content}")
        else:
            console.print("[yellow]Geen relevante herinneringen gevonden[/yellow]")
    
    # Afsluiting
    console.print(f"\n[bold green]✨ Demo voltooid![/bold green]")
    console.print("[dim]Solan's geheugen groeit met elke ervaring en wordt wijzer door reflectie[/dim]")
    
    # Optie om geheugen te behouden of te wissen
    keep_memory = input("\nWil je dit demo geheugen behouden? (j/n): ").lower().startswith('j')
    
    if not keep_memory:
        import shutil
        shutil.rmtree("demo_memory", ignore_errors=True)
        console.print("[yellow]Demo geheugen gewist[/yellow]")
    else:
        console.print("[green]Demo geheugen behouden in 'demo_memory/' directory[/green]")


if __name__ == "__main__":
    print("🧠 Starting Solan Memory System Demo...")
    asyncio.run(demo_memory_system())
