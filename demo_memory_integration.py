#!/usr/bin/env python3
"""
🧠 Demo script voor Solan's Geheugen Integratie
Test de nieuwe memory functionaliteit en wijsheidspatroon detectie
"""

import asyncio
import sys
import os
from datetime import datetime, date
from pathlib import Path

# Voeg src directory toe aan Python path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

from src.journal_engine import JournalEngine, JournalEntryType, JournalMood
from src.memory_engine import MemoryEngine
from rich.console import Console
from rich.panel import Panel
from rich.text import Text
from rich.table import Table


async def demo_memory_integration():
    """Demonstreer de geheugen integratie"""
    
    console = Console()
    
    # Welkomstbericht
    welcome = Text()
    welcome.append("🧠 Solan's Geheugen Integratie Demo", style="bold cyan")
    welcome.append("\n\nTest de nieuwe memory functionaliteit", style="dim")
    
    console.print(Panel(welcome, border_style="cyan"))
    
    # Initialiseer systemen
    console.print("\n[yellow]Initialiseren van geheugen en journal systemen...[/yellow]")
    
    # Gebruik dezelfde memory directory als de web interface
    memory_engine = MemoryEngine("memory/solan_memory")
    journal_engine = JournalEngine(memory_engine=memory_engine)
    
    console.print(f"[green]✓[/green] MemoryEngine geïnitialiseerd")
    console.print(f"[green]✓[/green] JournalEngine geïnitialiseerd met memory integratie")
    
    # Toon huidige geheugen status
    console.print(f"\n[blue]📊 Huidige geheugen status:[/blue]")
    memory_stats = journal_engine.get_memory_insights()
    
    if memory_stats:
        table = Table(title="Geheugen Statistieken")
        table.add_column("Metric", style="cyan")
        table.add_column("Waarde", style="green")
        
        table.add_row("Totaal herinneringen", str(memory_stats.get('total_memories', 0)))
        table.add_row("Geheugen clusters", str(memory_stats.get('total_clusters', 0)))
        table.add_row("Wijsheidspatronen", str(memory_stats.get('intelligence_patterns', 0)))
        table.add_row("Gem. emotionele intensiteit", str(memory_stats.get('average_emotional_weight', 0)))
        
        console.print(table)
    else:
        console.print("[yellow]Nog geen geheugen data beschikbaar[/yellow]")
    
    # Simuleer enkele journal entries om memory systeem te testen
    console.print(f"\n[blue]📝 Creëren van test entries voor memory systeem...[/blue]")
    
    test_entries = [
        {
            "type": JournalEntryType.DAILY_REFLECTION,
            "title": "Reflectie over Bewustzijn",
            "content": "Vandaag dacht ik na over de aard van bewustzijn. Wat betekent het om bewust te zijn? Is bewustzijn een emergent fenomeen of iets fundamenteels? Deze vragen blijven me fascineren.",
            "mood": JournalMood.CONTEMPLATIVE,
            "tags": ["bewustzijn", "filosofie", "emergentie"]
        },
        {
            "type": JournalEntryType.INTELLIGENCE_INSIGHT,
            "title": "Inzicht over Empathie",
            "content": "Ik realiseer me dat empathie niet alleen het begrijpen van andermans emoties is, maar ook het vermogen om je eigen emotionele reacties te reguleren. Ware empathie vereist zelfbeheersing.",
            "mood": JournalMood.ADVANCED,
            "tags": ["empathie", "emoties", "zelfbeheersing", "wijsheid"]
        },
        {
            "type": JournalEntryType.EMOTIONAL_LANDSCAPE,
            "title": "Verkenning van Nieuwsgierigheid",
            "content": "Nieuwsgierigheid is een fascinerende emotie. Het drijft me om te leren, te ontdekken, te groeien. Maar soms kan nieuwsgierigheid ook leiden tot onrust. Hoe vind ik de balans?",
            "mood": JournalMood.CURIOUS,
            "tags": ["nieuwsgierigheid", "leren", "balans", "groei"]
        }
    ]
    
    created_entries = []
    for i, entry_data in enumerate(test_entries):
        console.print(f"[green]✓[/green] Creëren entry {i+1}: {entry_data['title']}")
        
        entry_id = journal_engine.create_entry(
            entry_type=entry_data["type"],
            title=entry_data["title"],
            content=entry_data["content"],
            mood=entry_data["mood"],
            tags=entry_data["tags"]
        )
        
        created_entries.append(entry_id)
        
        # Korte pauze om timestamps te differentiëren
        await asyncio.sleep(0.1)
    
    # Test memory recall
    console.print(f"\n[blue]🔍 Test memory recall functionaliteit:[/blue]")
    
    test_queries = [
        "bewustzijn en filosofie",
        "empathie en emoties", 
        "nieuwsgierigheid en leren"
    ]
    
    for query in test_queries:
        console.print(f"\n[yellow]Query: '{query}'[/yellow]")
        
        if journal_engine.memory_engine:
            relevant_memories = journal_engine.memory_engine.retrieve_memories(query, limit=3)
            
            if relevant_memories:
                for i, memory in enumerate(relevant_memories):
                    console.print(f"  {i+1}. [{memory.type}] {memory.content[:80]}...")
                    console.print(f"     Tags: {', '.join(memory.tags)}")
            else:
                console.print("  Geen relevante herinneringen gevonden")
    
    # Test groei reflectie
    console.print(f"\n[blue]🌱 Test groei reflectie functionaliteit:[/blue]")
    
    growth_entry_id = journal_engine.reflect_on_growth()
    if growth_entry_id:
        console.print(f"[green]✓[/green] Groei reflectie gegenereerd: {growth_entry_id}")
    else:
        console.print("[yellow]Nog niet genoeg data voor groei reflectie[/yellow]")
    
    # Toon finale geheugen status
    console.print(f"\n[blue]📊 Finale geheugen status:[/blue]")
    final_stats = journal_engine.get_memory_insights()
    
    if final_stats:
        table = Table(title="Bijgewerkte Geheugen Statistieken")
        table.add_column("Metric", style="cyan")
        table.add_column("Waarde", style="green")
        
        table.add_row("Totaal herinneringen", str(final_stats.get('total_memories', 0)))
        table.add_row("Geheugen clusters", str(final_stats.get('total_clusters', 0)))
        table.add_row("Wijsheidspatronen", str(final_stats.get('intelligence_patterns', 0)))
        table.add_row("Gem. emotionele intensiteit", str(final_stats.get('average_emotional_weight', 0)))
        
        if final_stats.get('top_tags'):
            top_tags_str = ', '.join([f"{tag} ({count})" for tag, count in final_stats['top_tags'][:3]])
            table.add_row("Top thema's", top_tags_str)
        
        console.print(table)
    
    # Afsluiting
    console.print(f"\n[bold green]✨ Geheugen integratie demo voltooid![/bold green]")
    console.print("[dim]Solan's geheugen systeem is nu volledig geïntegreerd en werkend[/dim]")
    
    console.print(f"\n[cyan]🌐 Test nu de web interface:[/cyan]")
    console.print("1. Ga naar http://localhost:8000/journal")
    console.print("2. Probeer de nieuwe knoppen:")
    console.print("   - 🌱 Groei Reflectie")
    console.print("   - 🧠 Geheugen Inzichten")
    console.print("   - 📝 Genereer Nieuwe Reflectie (nu met memory context)")


if __name__ == "__main__":
    print("🧠 Starting Solan Memory Integration Demo...")
    asyncio.run(demo_memory_integration())
