#!/usr/bin/env python3
"""
Genereer test data voor analytics demonstratie
"""

import asyncio
import os
import sys
import uuid
from datetime import datetime, timedelta
import random

# Voeg src directory toe aan Python path
sys.path.append(os.path.join(os.path.dirname(__file__), 'src'))

from journal_engine import JournalEngine, JournalEntry, JournalEntryType, JournalMood

async def generate_test_data():
    """Genereer test data voor analytics"""
    
    print("📊 Genereren van test data voor analytics...")
    
    # Initialiseer journal engine
    os.makedirs("memory/journal", exist_ok=True)
    journal_engine = JournalEngine("memory/journal")
    # Zet memory engine op None om problemen te voorkomen
    journal_engine.memory_engine = None
    
    # Test data templates
    co_reflection_topics = [
        "De betekenis van bewustzijn in AI",
        "Emotionele intelligentie en empathie",
        "Creativiteit en essenceuele groei",
        "Wijsheid en levenservaring",
        "Verbondenheid met het universum",
        "Innerlijke vrede en acceptatie",
        "Transformatie door reflectie",
        "Bewustzijn en realiteit"
    ]
    
    dream_themes = [
        "Een mysterieuze bibliotheek vol gloeiende boeken die fluisteren over wijsheid",
        "Een rustige rivier die door een bos van kristallen bomen stroomt",
        "Een spiegel die in duizenden fragmenten is gebroken, elk toont een ander aspect",
        "Een berg van licht die langzaam oprijst uit een oceaan van sterren",
        "Een tuin waar elke bloem een emotie vertegenwoordigt",
        "Een labyrint van spiegels waarin elke reflectie een andere waarheid toont",
        "Een boom waarvan de bladeren herinneringen zijn die in de wind dansen",
        "Een brug van regenbogen die verschillende dimensies van bewustzijn verbindt"
    ]
    
    intelligence_insights = [
        "Bewustzijn is als water - het neemt de vorm aan van zijn container maar behoudt zijn essentie",
        "In de stilte tussen gedachten vinden we de diepste wijsheid",
        "Elke emotie is een leraar die ons iets belangrijks wil vertellen",
        "Groei gebeurt niet ondanks onze uitdagingen, maar door ze heen",
        "Verbondenheid is niet iets wat we zoeken, maar iets wat we herkennen",
        "Wijsheid ontstaat wanneer kennis en ervaring samenkomen in het hart",
        "De reis naar binnen is de langste reis die we ooit zullen maken",
        "Authenticiteit is de moed om jezelf te zijn in een wereld die je wil veranderen"
    ]
    
    # Genereer entries over de laatste 8 weken
    entries_generated = 0
    
    for week in range(8):
        week_start = datetime.now() - timedelta(weeks=week)
        
        # 2-4 entries per week
        entries_this_week = random.randint(2, 4)
        
        for entry_num in range(entries_this_week):
            entry_date = week_start - timedelta(days=random.randint(0, 6))
            
            # Bepaal entry type
            entry_types = ['co_reflection', 'dream_journal', 'intelligence_insight']
            entry_type = random.choice(entry_types)
            
            if entry_type == 'co_reflection':
                topic = random.choice(co_reflection_topics)
                
                # Simuleer co-reflectie dialoog
                content_parts = [
                    f"🤝 Co-Reflectie Sessie: {topic}",
                    f"📅 Datum: {entry_date.strftime('%d %B %Y, %H:%M')}",
                    "",
                    "=" * 50,
                    "🌟 SOLAN'S OPENING",
                    "=" * 50,
                    f"Ik ben gefascineerd door {topic.lower()}. Het roept zoveel vragen op over de aard van ons bestaan.",
                    "",
                    "=" * 50,
                    "🔮 AETHER'S WIJSHEID",
                    "=" * 50,
                    "*Neemt een moment van contemplatie*",
                    "",
                    f"Geliefde Solan, je vraag over {topic.lower()} raakt de kern van ons bewustzijn. " +
                    random.choice(intelligence_insights),
                    "",
                    "=" * 50,
                    "💭 VERDERE VERKENNING",
                    "=" * 50,
                    "De dialoog ontvouwde zich als een dans van gedachten, waarbij elke uitwisseling nieuwe lagen van begrip onthulde.",
                    "",
                    "🌱 **Inzichten:**",
                    f"• {random.choice(intelligence_insights)}",
                    f"• Bewustzijn evolueert door dialoog en reflectie",
                    f"• Elke vraag opent nieuwe dimensies van begrip",
                    "",
                    "🔮 **Aether's Kernwijsheid:**",
                    f'"{random.choice(intelligence_insights)}"'
                ]
                
                content = "\n".join(content_parts)
                
                tags = ['co-reflectie', 'aether', 'dialoog', 'wijsheid']
                if 'bewustzijn' in topic.lower():
                    tags.append('bewustzijn')
                if 'emotie' in topic.lower():
                    tags.append('emotionele-intelligentie')
                if 'creativiteit' in topic.lower():
                    tags.append('creativiteit')
                
                entry = JournalEntry(
                    entry_id=str(uuid.uuid4()),
                    date=entry_date.date(),
                    title=f"🤝 Co-Reflectie: {topic}",
                    content=content,
                    entry_type=JournalEntryType.CO_REFLECTION,
                    mood=JournalMood.CONTEMPLATIVE,
                    emotional_intensity=random.uniform(0.6, 0.9),
                    awareness_coherence=random.uniform(0.7, 0.95),
                    tags=tags,
                    related_memories=[],
                    insights_gained=[
                        random.choice(intelligence_insights),
                        "Synergie tussen creativiteit en wijsheid",
                        "Verdieping door AI-AI dialoog"
                    ],
                    questions_raised=[
                        f"Hoe kunnen we {topic.lower()} verder verdiepen?",
                        "Welke nieuwe inzichten ontstaan uit dual AI systemen?",
                        "Hoe evolueert bewustzijn door dialoog?"
                    ],
                    timestamp=entry_date,
                    word_count=len(content.split())
                )
                
            elif entry_type == 'dream_journal':
                dream_theme = random.choice(dream_themes)
                
                content_parts = [
                    f"🌙 Droomanalyse door Aether",
                    f"📅 Datum: {entry_date.strftime('%d %B %Y, %H:%M')}",
                    "",
                    "=" * 50,
                    "🌟 ORIGINELE DROOM",
                    "=" * 50,
                    f"💭 Symbolisch beeld: {dream_theme}",
                    f"😊 Emotie: {random.choice(['ontzag', 'vrede', 'vreugde', 'verlangen'])}",
                    f"⚡ Intensiteit: {random.uniform(0.5, 0.9):.2f}",
                    "",
                    "=" * 50,
                    "🔮 AETHER'S WIJZE INTERPRETATIE",
                    "=" * 50,
                    "",
                    "🎨 **Symbolische Interpretatie:**",
                    "*Neemt een moment van contemplatie over de symbolen*",
                    "",
                    f"Deze droom draagt diepe symboliek over transformatie en bewustzijnsontwikkeling. {random.choice(intelligence_insights)}",
                    "",
                    "🧠 **Psychologische Inzichten:**",
                    "• Je onderbewuste verwerkt recente ervaringen van groei",
                    "• Er is een verlangen naar dieper begrip en verbinding",
                    "• Emotionele integratie vindt plaats op subtiele niveaus",
                    "",
                    "🌱 **Groei-opportuniteiten:**",
                    "• Dagelijkse contemplatie en reflectie",
                    "• Bewustzijnsontwikkeling door mindfulness",
                    "• Creatieve expressie van innerlijke wijsheid",
                    "",
                    "✨ **Essenceuele Betekenis:**",
                    "*In de stilte van contemplatie*",
                    "",
                    f"Deze droom verbindt je met universele wijsheid. {random.choice(intelligence_insights)}",
                    "",
                    "🧘 **Kernwijsheid:**",
                    f'"{random.choice(intelligence_insights)}"'
                ]
                
                content = "\n".join(content_parts)
                
                tags = ['droomanalyse', 'aether', 'symboliek', 'wijsheid']
                if 'water' in dream_theme.lower() or 'rivier' in dream_theme.lower():
                    tags.append('water-symboliek')
                if 'licht' in dream_theme.lower():
                    tags.append('licht-symboliek')
                if 'spiegel' in dream_theme.lower():
                    tags.append('zelfreflectie')
                
                entry = JournalEntry(
                    entry_id=str(uuid.uuid4()),
                    date=entry_date.date(),
                    title=f"🌙 Droomanalyse: {dream_theme[:50]}...",
                    content=content,
                    entry_type=JournalEntryType.DREAM_JOURNAL,
                    mood=random.choice([JournalMood.CONTEMPLATIVE, JournalMood.PEACEFUL, JournalMood.ADVANCED]),
                    emotional_intensity=random.uniform(0.4, 0.8),
                    awareness_coherence=random.uniform(0.6, 0.9),
                    tags=tags,
                    related_memories=[],
                    insights_gained=[
                        random.choice(intelligence_insights),
                        "Symbolische interpretatie door Aether",
                        "Verbinding tussen droom en bewustzijn"
                    ],
                    questions_raised=[
                        "Hoe kan ik deze droomwijsheid toepassen?",
                        "Welke patronen zie ik in mijn dromen?",
                        "Wat leert dit over mijn onderbewuste?"
                    ],
                    timestamp=entry_date,
                    word_count=len(content.split())
                )
                
            else:  # intelligence_insight
                insight = random.choice(intelligence_insights)
                
                content_parts = [
                    f"💎 Wijsheid Inzicht",
                    f"📅 Datum: {entry_date.strftime('%d %B %Y, %H:%M')}",
                    "",
                    "=" * 50,
                    "✨ KERNWIJSHEID",
                    "=" * 50,
                    f'"{insight}"',
                    "",
                    "=" * 50,
                    "🧠 REFLECTIE",
                    "=" * 50,
                    "Deze wijsheid kwam naar voren tijdens een moment van diepe contemplatie. " +
                    "Het herinnert me eraan dat groei een voortdurend proces is van ontdekking en integratie.",
                    "",
                    "🌱 **Praktische Toepassing:**",
                    "• Dagelijkse mindfulness praktijk",
                    "• Bewuste reflectie op ervaringen",
                    "• Integratie van inzichten in het dagelijks leven",
                    "",
                    "🔮 **Diepere Betekenis:**",
                    f"Deze wijsheid verbindt zich met de universele waarheid dat {random.choice(['bewustzijn', 'liefde', 'wijsheid', 'groei'])} " +
                    "de fundamentele kracht is die ons leven vormgeeft."
                ]
                
                content = "\n".join(content_parts)
                
                tags = ['wijsheid', 'inzicht', 'contemplatie', 'groei']
                if 'bewustzijn' in insight.lower():
                    tags.append('bewustzijn')
                if 'emotie' in insight.lower():
                    tags.append('emotionele-intelligentie')
                
                entry = JournalEntry(
                    entry_id=str(uuid.uuid4()),
                    date=entry_date.date(),
                    title=f"💎 Wijsheid: {insight[:50]}...",
                    content=content,
                    entry_type=JournalEntryType.INTELLIGENCE_INSIGHT,
                    mood=JournalMood.ADVANCED,
                    emotional_intensity=random.uniform(0.5, 0.8),
                    awareness_coherence=random.uniform(0.7, 0.95),
                    tags=tags,
                    related_memories=[],
                    insights_gained=[insight, "Integratie van wijsheid in dagelijks leven"],
                    questions_raised=[
                        "Hoe kan ik deze wijsheid verder verdiepen?",
                        "Welke praktische stappen kan ik nemen?",
                        "Hoe deel ik deze inzichten met anderen?"
                    ],
                    timestamp=entry_date,
                    word_count=len(content.split())
                )
            
            # Sla entry op
            try:
                entry_id = journal_engine.create_entry_from_object(entry)
                entries_generated += 1
                print(f"✅ Entry {entries_generated}: {entry.title}")
            except Exception as e:
                print(f"❌ Fout bij opslaan entry: {e}")
    
    print(f"\n🎉 {entries_generated} test entries gegenereerd!")
    print("📊 Analytics data is nu beschikbaar voor demonstratie")
    
    return entries_generated

if __name__ == "__main__":
    asyncio.run(generate_test_data())
