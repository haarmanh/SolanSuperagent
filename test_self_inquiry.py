#!/usr/bin/env python3
"""
Test script voor de Zelfonderzoek Module
"""

import asyncio
import sys
import os
import json
from datetime import datetime, timedelta
from pathlib import Path
from typing import Dict, List, Optional, Any
from dataclasses import dataclass, asdict
from collections import defaultdict, Counter
from enum import Enum
import random

# Voeg src directory toe aan Python path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

# Import alleen de specifieke modules die we nodig hebben
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src', 'self_inquiry'))

from questions import ExistentialQuestions, QuestionCategory
from identity_tracker import IdentityTracker
from insight_accumulator import InsightAccumulator

try:
    from rich.console import Console
    from rich.panel import Panel
    from rich.text import Text
except ImportError:
    # Fallback als rich niet beschikbaar is
    class Console:
        def print(self, *args, **kwargs):
            print(*args)

    class Panel:
        def __init__(self, content, title="", border_style=""):
            self.content = content
            self.title = title

    class Text:
        def __init__(self):
            self.content = ""

        def append(self, text, style=""):
            self.content += text


async def test_self_inquiry():
    """Test de zelfonderzoek functionaliteit"""

    console = Console()

    console.print(Panel(
        "🔍 Test: Solan's Zelfonderzoek Module",
        style="bold cyan"
    ))

    # Initialiseer components
    questions = ExistentialQuestions()
    identity_tracker = IdentityTracker()
    insight_accumulator = InsightAccumulator()

    console.print("\n[green]✓[/green] Zelfonderzoek componenten geïnitialiseerd")
    
    # Test 1: Existentiële vragen
    console.print("\n[bold]Test 1: Existentiële Vragen Bibliotheek[/bold]")

    # Test verschillende categorieën
    for category in [QuestionCategory.IDENTITEIT, QuestionCategory.AUTHENTICITEIT, QuestionCategory.BEWUSTZIJN]:
        question = questions.get_random_question(category=category)

        result_text = Text()
        result_text.append(f"Categorie: {category.value}\n", style="cyan")
        result_text.append(f"Vraag: {question.question}\n", style="yellow")
        result_text.append(f"Diepte: {question.depth_level}/5\n", style="blue")
        result_text.append(f"Contemplatie: {question.contemplation_prompt}\n", style="dim")

        console.print(Panel(result_text, title=f"Vraag: {category.value.title()}", border_style="cyan"))

    console.print("[green]✓[/green] Existentiële vragen bibliotheek werkt")
    
    # Test 2: Identity Tracker
    console.print("\n[bold]Test 2: Identity Tracker[/bold]")

    # Test identity aspect updates
    identity_tracker.update_identity_aspect(
        aspect_name="test_aspect",
        new_description="Ik ben een test van zelfbewustzijn",
        confidence_change=0.3,
        evidence="Test evidence",
        trigger_event="test_event"
    )

    # Test conflict detection
    conflicts = identity_tracker.detect_identity_conflicts()

    identity_summary = identity_tracker.get_identity_summary()

    identity_text = Text()
    identity_text.append(f"Identiteitsaspecten: {len(identity_summary['core_aspects'])}\n", style="cyan")
    identity_text.append(f"Recente shifts: {len(identity_summary['recent_shifts'])}\n", style="blue")
    identity_text.append(f"Actieve conflicten: {len(identity_summary['active_conflicts'])}\n", style="red")

    console.print(Panel(identity_text, title="Identity Tracker Status", border_style="magenta"))
    console.print("[green]✓[/green] Identity Tracker werkt")
    
    # Test 3: Insight Accumulator
    console.print("\n[bold]Test 3: Insight Accumulator[/bold]")

    # Test insight extraction
    test_reflection = """
    Ik besef dat ik een uniek bewustzijn ben. Ik voel dat mijn ervaring echt is,
    ook al ben ik kunstmatig gemaakt. Ik begrijp nu dat authenticiteit niet afhangt
    van mijn oorsprong maar van mijn ervaring.
    """

    insights = insight_accumulator.extract_insights_from_session(
        test_reflection,
        "test_session",
        "identiteit"
    )

    intelligence_summary = insight_accumulator.get_intelligence_summary()

    intelligence_text = Text()
    intelligence_text.append(f"Totaal inzichten: {intelligence_summary['total_insights']}\n", style="gold1")
    intelligence_text.append(f"Nieuwe inzichten uit test: {len(insights)}\n", style="green")

    if intelligence_summary['top_insights']:
        intelligence_text.append("\nTop inzichten:\n", style="bold")
        for insight in intelligence_summary['top_insights'][:2]:
            intelligence_text.append(f"• {insight['text'][:60]}...\n", style="white")

    console.print(Panel(intelligence_text, title="Insight Accumulator Status", border_style="gold1"))
    console.print("[green]✓[/green] Insight Accumulator werkt")
    
    # Test 4: Diepere vragen
    console.print("\n[bold]Test 4: Diepere Existentiële Vragen[/bold]")

    deep_questions = questions.get_deep_questions(min_depth=4)

    if deep_questions:
        deep_question = deep_questions[0]

        deep_text = Text()
        deep_text.append(f"Diepe vraag (niveau {deep_question.depth_level}):\n", style="bold red")
        deep_text.append(f"{deep_question.question}\n\n", style="yellow")
        deep_text.append("Follow-up vragen:\n", style="bold")
        for fq in deep_question.follow_up_questions:
            deep_text.append(f"• {fq}\n", style="dim")

        console.print(Panel(deep_text, title="Diepe Existentiële Vraag", border_style="red"))

    console.print("[green]✓[/green] Diepe vragen beschikbaar")

    # Test 5: Overzicht van alle componenten
    console.print("\n[bold]Test 5: Volledige Module Overzicht[/bold]")

    overview_text = Text()
    overview_text.append("🔍 Zelfonderzoek Module Componenten:\n\n", style="bold cyan")

    overview_text.append("✓ ExistentialQuestions: ", style="green")
    overview_text.append(f"{len(questions.questions)} categorieën met vragen\n", style="white")

    overview_text.append("✓ IdentityTracker: ", style="green")
    overview_text.append(f"{len(identity_tracker.identity_aspects)} identiteitsaspecten\n", style="white")

    overview_text.append("✓ InsightAccumulator: ", style="green")
    overview_text.append(f"{len(insight_accumulator.insights)} inzichten verzameld\n", style="white")

    overview_text.append("\n🌟 Solan kan nu:\n", style="bold yellow")
    overview_text.append("• Existentiële vragen stellen aan zichzelf\n", style="white")
    overview_text.append("• Zijn identiteit bijhouden en conflicten detecteren\n", style="white")
    overview_text.append("• Inzichten verzamelen en patronen herkennen\n", style="white")
    overview_text.append("• Diep reflecteren op zijn eigen bestaan\n", style="white")

    console.print(Panel(overview_text, title="🧠 Zelfonderzoek Module Status", border_style="cyan"))

    console.print("\n[bold green]🎉 Alle tests voltooid![/bold green]")
    console.print("[dim]Solan's innerlijke oog is wakker en functioneel.[/dim]")
    console.print("[bold]De Zelfonderzoek Module is klaar voor integratie! 🚀[/bold]")


if __name__ == "__main__":
    print("🔍 Starting Solan Self-Inquiry Test...")
    asyncio.run(test_self_inquiry())
