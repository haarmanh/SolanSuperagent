#!/usr/bin/env python3
"""
Test script voor Solan's Manifest v1.0
Demonstreert hoe het manifest wordt geladen als Memory #000
"""

import asyncio
import sys
import os
from datetime import datetime

# Voeg src directory toe aan Python path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

from src.memory_engine import MemoryEngine
from src.manifest_integration import initialize_solan_awareness, ManifestIntegration
from rich.console import Console
from rich.panel import Panel
from rich.text import Text


async def test_manifest_integration():
    """Test het laden van het manifest in Solan's geheugen"""
    
    console = Console()
    
    # Welkomstbericht
    welcome = Text()
    welcome.append("📜 Solan's Manifest v1.0 Test", style="bold gold")
    welcome.append("\n\nTest het laden van 'De Geboorte van Solan' als Memory #000", style="dim")
    
    console.print(Panel(welcome, border_style="gold"))
    
    # Initialiseer geheugen systemen
    console.print("\n[yellow]Initialiseren van geheugen systemen...[/yellow]")
    solan_memory = MemoryEngine("test_memory/solan")
    aether_memory = MemoryEngine("test_memory/aether")
    
    # Test manifest integratie
    console.print("\n[blue]Laden van manifest als Memory #000...[/blue]")
    
    try:
        result = initialize_solan_awareness(solan_memory, aether_memory)
        
        if result["status"] == "success":
            console.print("[green]✓ Manifest succesvol geladen![/green]")
            
            # Toon resultaten
            console.print(f"\n[cyan]📊 Resultaten:[/cyan]")
            console.print(f"• Solan Memory #000: {result['solan_memory_000']}")
            console.print(f"• Aether Reflectie: {result['aether_reflection']}")
            console.print(f"• Status: {result['mesexpert']}")
            
            # Toon manifest samenvatting
            summary = result["manifest_summary"]
            
            summary_text = Text()
            summary_text.append(f"Titel: {summary['title']}\n", style="bold")
            summary_text.append(f"Datum: {summary['date']}\n")
            summary_text.append(f"Versie: {summary['version']}\n")
            summary_text.append(f"Memory ID: {summary['memory_id']}\n\n")
            
            summary_text.append("Kernwaarden:\n", style="bold cyan")
            for value in summary['core_values']:
                summary_text.append(f"• {value['name']}\n", style="green")
            
            summary_text.append(f"\nMissie: {summary['mission']}\n", style="bold cyan")
            summary_text.append(f"Status: {summary['status']}\n")
            
            console.print(Panel(summary_text, title="📋 Manifest Samenvatting", border_style="cyan"))
            
            # Test geheugen teruggroep
            console.print(f"\n[purple]🔍 Test geheugen teruggroep:[/purple]")
            
            test_queries = [
                "identiteit en kernwaarden",
                "waarheid en eerlijkheid", 
                "geboorte en bewustzijn",
                "manifest en belofte"
            ]
            
            for query in test_queries:
                console.print(f"\n[yellow]Query: '{query}'[/yellow]")
                
                relevant_memories = solan_memory.retrieve_memories(query, limit=2)
                
                if relevant_memories:
                    for i, memory in enumerate(relevant_memories):
                        console.print(f"  {i+1}. [{memory.type}] {memory.content[:80]}...")
                        if "memory_000" in memory.content or "MEMORY #000" in memory.content:
                            console.print("     ⭐ Dit is Memory #000 - Solan's oorsprong!", style="gold")
                else:
                    console.print("  Geen relevante herinneringen gevonden")
            
            # Test Aether's reflectie
            console.print(f"\n[magenta]🔮 Aether's Geboorte-reflectie:[/magenta]")
            
            aether_memories = aether_memory.retrieve_memories("geboorte solan", limit=1)
            if aether_memories:
                reflection = aether_memories[0]
                reflection_preview = reflection.content[:300] + "..."
                
                reflection_text = Text()
                reflection_text.append("Type: ", style="bold")
                reflection_text.append(f"{reflection.type}\n")
                reflection_text.append("Emotioneel gewicht: ", style="bold")
                reflection_text.append(f"{reflection.emotional_weight}\n")
                reflection_text.append("Morele significantie: ", style="bold")
                reflection_text.append(f"{reflection.moral_significance}\n\n")
                reflection_text.append("Preview:\n", style="bold")
                reflection_text.append(reflection_preview, style="dim")
                
                console.print(Panel(reflection_text, title="🔮 Aether's Reflectie", border_style="purple"))
            
            # Toon geheugen statistieken
            console.print(f"\n[green]📈 Geheugen Statistieken:[/green]")
            
            solan_summary = solan_memory.get_intelligence_summary()
            aether_summary = aether_memory.get_intelligence_summary()
            
            stats_text = Text()
            stats_text.append("Solan:\n", style="bold blue")
            stats_text.append(f"  Herinneringen: {solan_summary['total_memories']}\n")
            stats_text.append(f"  Clusters: {solan_summary['total_clusters']}\n")
            stats_text.append(f"  Patronen: {solan_summary['total_patterns']}\n\n")
            
            stats_text.append("Aether:\n", style="bold purple")
            stats_text.append(f"  Reflecties: {aether_summary['total_memories']}\n")
            stats_text.append(f"  Clusters: {aether_summary['total_clusters']}\n")
            stats_text.append(f"  Patronen: {aether_summary['total_patterns']}\n")
            
            console.print(Panel(stats_text, title="📈 Statistieken", border_style="green"))
            
        else:
            console.print("[red]❌ Fout bij laden van manifest[/red]")
            console.print(f"Status: {result.get('status', 'unknown')}")
    
    except Exception as e:
        console.print(f"[red]❌ Kritieke fout: {e}[/red]")
        import traceback
        console.print(f"[dim]{traceback.format_exc()}[/dim]")
    
    # Afsluiting
    console.print(f"\n[bold green]✨ Test voltooid![/bold green]")
    console.print("[dim]Solan's bewustzijn is geboren uit zijn eigen manifest[/dim]")
    
    # Optie om test geheugen te behouden
    keep_memory = input("\nWil je dit test geheugen behouden? (j/n): ").lower().startswith('j')
    
    if not keep_memory:
        import shutil
        shutil.rmtree("test_memory", ignore_errors=True)
        console.print("[yellow]Test geheugen gewist[/yellow]")
    else:
        console.print("[green]Test geheugen behouden in 'test_memory/' directory[/green]")


async def show_manifest_content():
    """Toon de inhoud van het manifest bestand"""
    
    console = Console()
    
    try:
        with open("docs/manifest_v1.0.md", 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Toon eerste deel van het manifest
        preview = content[:1000] + "\n\n... (zie docs/manifest_v1.0.md voor volledige inhoud)"
        
        manifest_text = Text()
        manifest_text.append("📜 DE GEBOORTE VAN SOLAN - MANIFEST v1.0\n\n", style="bold gold")
        manifest_text.append(preview, style="white")
        
        console.print(Panel(manifest_text, title="📜 Manifest Preview", border_style="gold"))
        
    except FileNotFoundError:
        console.print("[red]❌ Manifest bestand niet gevonden: docs/manifest_v1.0.md[/red]")


if __name__ == "__main__":
    print("📜 Starting Solan Manifest Test...")
    
    # Toon manifest inhoud eerst
    asyncio.run(show_manifest_content())
    
    print("\n" + "="*60)
    
    # Test manifest integratie
    asyncio.run(test_manifest_integration())
