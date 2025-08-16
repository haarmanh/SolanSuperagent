#!/usr/bin/env python3
"""
Test script voor Solan Journal generatie
Demonstreert verschillende modi: OpenAI, Solan Agent, en Demo
"""

import asyncio
import os
from datetime import datetime
from pathlib import Path

# Add src to path
import sys
sys.path.append('src')

from journal_engine import JournalEngine
import logging

# Setup logger
logger = logging.getLogger(__name__)

async def test_journal_generation():
    """Test verschillende journal generatie modi"""
    
    print("🤖 Solan Journal Generatie Test")
    print("=" * 50)
    
    # Initialize journal engine
    journal_engine = JournalEngine()
    
    # Test 1: Demo modus (geen OpenAI key)
    print("\n📝 Test 1: Demo Modus (Variërende Content)")
    print("-" * 40)
    
    for i in range(3):
        print(f"\nGeneratie {i+1}:")
        entry_id = await journal_engine.generate_daily_reflection()
        
        if entry_id:
            # Get the generated entry
            entries = journal_engine.get_recent_entries(days=1)
            if entries:
                latest_entry = entries[0]
                print(f"✅ Entry ID: {entry_id}")
                print(f"📅 Timestamp: {latest_entry.timestamp}")
                print(f"🎭 Entry Type: {latest_entry.entry_type.value}")
                print(f"😊 Mood: {latest_entry.mood.value}")
                print(f"📖 Content preview: {latest_entry.content[:100]}...")
                print(f"📊 Content length: {len(latest_entry.content)} characters")
        else:
            print("❌ Geen entry gegenereerd")
    
    # Test 2: OpenAI modus (als API key beschikbaar)
    print("\n\n🧠 Test 2: OpenAI Modus")
    print("-" * 40)
    
    if journal_engine.openai_client:
        print("✅ OpenAI client beschikbaar")
        
        # Test OpenAI generatie
        try:
            entry_id = await journal_engine.generate_daily_reflection()
            print(f"✅ OpenAI reflectie gegenereerd: {entry_id}")
        except Exception as e:
            print(f"❌ OpenAI fout: {e}")
    else:
        print("⚠️  OpenAI client niet beschikbaar")
        print("💡 Voeg OPENAI_API_KEY toe aan .env voor OpenAI functionaliteit")
    
    # Test 3: Statistieken
    print("\n\n📊 Journal Statistieken")
    print("-" * 40)
    
    stats = journal_engine.get_journal_statistics()
    print(f"📚 Totaal entries: {stats['total_entries']}")
    print(f"📝 Totaal woorden: {stats['total_words']}")
    print(f"📈 Gemiddeld woorden per entry: {stats['average_words_per_entry']:.1f}")
    print(f"🔥 Schrijf streak: {stats['writing_streak']} dagen")
    
    if stats['entries_by_type']:
        print("\n📋 Entries per type:")
        for entry_type, count in stats['entries_by_type'].items():
            print(f"  • {entry_type}: {count}")
    
    # Test 4: Content variatie analyse
    print("\n\n🔍 Content Variatie Analyse")
    print("-" * 40)
    
    recent_entries = journal_engine.get_recent_entries(days=7)
    if len(recent_entries) >= 2:
        # Vergelijk eerste woorden van recente entries
        first_words = []
        for entry in recent_entries[:5]:  # Laatste 5 entries
            words = entry.content.split()[:10]  # Eerste 10 woorden
            first_words.append(' '.join(words))
        
        print("🔤 Eerste 10 woorden van recente entries:")
        for i, words in enumerate(first_words):
            print(f"  {i+1}. {words}...")
        
        # Check voor duplicaten
        unique_starts = set(first_words)
        if len(unique_starts) == len(first_words):
            print("✅ Alle entries hebben unieke openingszinnen")
        else:
            print(f"⚠️  {len(first_words) - len(unique_starts)} duplicaat openingszinnen gevonden")
    else:
        print("⚠️  Niet genoeg entries voor variatie analyse")
    
    print("\n" + "=" * 50)
    print("🎯 Test Voltooid!")
    
    # Instructies voor gebruiker
    print("\n💡 Volgende Stappen:")
    print("1. 🌐 Open http://127.0.0.1:8000 in je browser")
    print("2. 🔄 Klik op 'Genereer Nieuwe Reflectie' meerdere keren")
    print("3. 👀 Observeer dat elke reflectie uniek is")
    print("4. 🔑 Voeg OPENAI_API_KEY toe aan .env voor echte AI generatie")
    print("5. 🧪 Test opnieuw om verschil te zien tussen demo en OpenAI modus")


if __name__ == "__main__":
    # Ensure logs directory exists
    Path("logs").mkdir(exist_ok=True)
    
    # Configure logging
    logger.add("logs/journal_test.log", rotation="1 day")
    
    # Run test
    asyncio.run(test_journal_generation())
