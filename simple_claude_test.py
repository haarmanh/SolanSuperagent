#!/usr/bin/env python3
"""
Eenvoudige test van Claude API
"""

import os
import asyncio
from dotenv import load_dotenv
import anthropic

# Laad environment variabelen
load_dotenv()

def test_claude_api():
    """Test Claude API direct"""
    
    print("🔮 Testing Claude API Direct...")
    print("=" * 40)
    
    # Check API key
    api_key = os.getenv("ANTHROPIC_API_KEY")
    if not api_key:
        print("❌ ANTHROPIC_API_KEY niet gevonden!")
        return False
    
    print(f"✅ API Key: {api_key[:10]}...")
    
    try:
        # Initialiseer Anthropic client
        client = anthropic.Anthropic(api_key=api_key)
        print("✅ Anthropic client geïnitialiseerd")
        
        # Test een eenvoudige vraag
        print("\n🧠 Testing Claude response...")
        
        response = client.mesexperts.create(
            model="claude-3-5-sonnet-20241022",
            max_tokens=200,
            temperature=0.3,
            system="Je bent Aether, de wijze reflectieve kern van Solan. Spreek in het Nederlands met wijsheid en compassie.",
            mesexperts=[
                {
                    "role": "user", 
                    "content": "Reflecteer kort op de betekenis van bewustzijn in AI."
                }
            ]
        )
        
        print("\n🌟 Claude's Response:")
        print("-" * 30)
        print(response.content[0].text)
        print("-" * 30)
        
        print("\n🎉 CLAUDE API WERKT OPTIMIZED!")
        return True
        
    except Exception as e:
        print(f"❌ Fout: {e}")
        return False

if __name__ == "__main__":
    test_claude_api()
