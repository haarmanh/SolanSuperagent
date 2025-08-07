#!/usr/bin/env python3
"""
Snelle test van API connecties en journal data
"""

import os
import json
from pathlib import Path
from dotenv import load_dotenv

# Laad environment variabelen
load_dotenv()

def test_openai_connection():
    """Test OpenAI API connectie"""
    try:
        import openai
        client = openai.OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
        
        # Simpele test call
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            mesexperts=[{"role": "user", "content": "Say 'OpenAI connection works!'"}],
            max_tokens=10
        )
        
        print("✅ OpenAI API werkt:", response.choices[0].mesexpert.content.strip())
        return True
    except Exception as e:
        print(f"❌ OpenAI API fout: {e}")
        return False

def test_anthropic_connection():
    """Test Anthropic API connectie"""
    try:
        import anthropic
        client = anthropic.Anthropic(api_key=os.getenv("ANTHROPIC_API_KEY"))
        
        # Simpele test call
        response = client.mesexperts.create(
            model="claude-3-haiku-20240307",
            max_tokens=10,
            mesexperts=[{"role": "user", "content": "Say 'Claude connection works!'"}]
        )
        
        print("✅ Anthropic API werkt:", response.content[0].text.strip())
        return True
    except Exception as e:
        print(f"❌ Anthropic API fout: {e}")
        return False

def check_journal_files():
    """Controleer journal bestanden"""
    journal_path = Path("memory/journal/entries")
    
    if not journal_path.exists():
        print(f"❌ Journal directory bestaat niet: {journal_path}")
        return False
    
    json_files = list(journal_path.glob("*.json"))
    print(f"📁 Gevonden {len(json_files)} JSON bestanden in {journal_path}")
    
    if json_files:
        # Test een bestand
        test_file = json_files[0]
        try:
            with open(test_file, 'r', encoding='utf-8') as f:
                data = json.load(f)
            print(f"✅ Test bestand geladen: {test_file.name}")
            print(f"   - Entry ID: {data.get('entry_id', 'N/A')}")
            print(f"   - Type: {data.get('entry_type', 'N/A')}")
            print(f"   - Datum: {data.get('date', 'N/A')}")
            return True
        except Exception as e:
            print(f"❌ Fout bij laden test bestand: {e}")
            return False
    else:
        print("⚠️ Geen JSON bestanden gevonden")
        return False

def test_imports():
    """Test alle belangrijke imports"""
    print("\n🔍 Testing imports...")
    
    try:
        from src.journal_engine import JournalEngine
        print("✅ JournalEngine import werkt")
    except Exception as e:
        print(f"❌ JournalEngine import fout: {e}")
    
    try:
        from src.analytics_engine import AdvancedAnalyticsEngine
        print("✅ AnalyticsEngine import werkt")
    except Exception as e:
        print(f"❌ AnalyticsEngine import fout: {e}")
    
    try:
        from src.aether import Aether
        print("✅ Aether import werkt")
    except Exception as e:
        print(f"❌ Aether import fout: {e}")

def main():
    print("🚀 Snelle systeem check...")
    print("=" * 50)
    
    # Test imports
    test_imports()
    
    print("\n📡 Testing API connections...")
    openai_ok = test_openai_connection()
    anthropic_ok = test_anthropic_connection()
    
    print("\n📚 Testing journal data...")
    journal_ok = check_journal_files()
    
    print("\n" + "=" * 50)
    print("📊 RESULTATEN:")
    print(f"   OpenAI API: {'✅' if openai_ok else '❌'}")
    print(f"   Anthropic API: {'✅' if anthropic_ok else '❌'}")
    print(f"   Journal Data: {'✅' if journal_ok else '❌'}")
    
    if openai_ok and anthropic_ok and journal_ok:
        print("\n🎉 Alle systemen werken!")
    else:
        print("\n⚠️ Er zijn problemen gevonden die opgelost moeten worden.")

if __name__ == "__main__":
    main()
