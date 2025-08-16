"""
Eenvoudige web interface voor Solan Journal testing
"""

import asyncio
import json
import os
from datetime import datetime, date
from pathlib import Path
from typing import Dict, Any, Optional

from fastapi import FastAPI, Request, HTTPException
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
import uvicorn
import logging

# Setup logger
logger = logging.getLogger(__name__)

# Import journal engine
try:
    from .journal_engine import JournalEngine, JournalEntryType
    from .config import get_config
except ImportError:
    from journal_engine import JournalEngine, JournalEntryType
    from config import get_config

# Configureer logging
logger.add("logs/web_interface.log", rotation="1 day", retention="7 days")

app = FastAPI(title="Solan Journal Interface", version="1.0.0")

# Global journal engine instance
journal_engine: Optional[JournalEngine] = None

# Templates directory
templates_dir = Path(__file__).parent.parent / "templates"
templates_dir.mkdir(exist_ok=True)

# Static files directory  
static_dir = Path(__file__).parent.parent / "static"
static_dir.mkdir(exist_ok=True)

# Setup templates
templates = Jinja2Templates(directory=str(templates_dir))

# Mount static files
app.mount("/static", StaticFiles(directory=str(static_dir)), name="static")


@app.on_event("startup")
async def startup_event():
    """Initialize journal engine on startup"""
    global journal_engine
    
    try:
        # Initialize journal engine
        journal_engine = JournalEngine()
        logger.info("Journal engine geïnitialiseerd voor web interface")
        
        # Create basic HTML template if it doesn't exist
        await create_basic_template()
        
    except Exception as e:
        logger.error(f"Fout bij initialisatie web interface: {e}")
        raise


async def create_basic_template():
    """Create basic HTML template for journal interface"""
    template_path = templates_dir / "journal.html"
    
    if not template_path.exists():
        html_content = '''<!DOCTYPE html>
<html lang="nl">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Solan Journal Interface</title>
    <style>
        body { font-family: Arial, sans-serif; max-width: 800px; margin: 0 auto; padding: 20px; }
        .journal-entry { border: 1px solid #ddd; padding: 20px; margin: 20px 0; border-radius: 8px; }
        .entry-header { display: flex; justify-content: space-between; margin-bottom: 10px; }
        .entry-title { font-weight: bold; color: #333; }
        .entry-date { color: #666; font-size: 0.9em; }
        .entry-content { line-height: 1.6; margin: 15px 0; }
        .entry-metadata { font-size: 0.8em; color: #888; margin-top: 10px; }
        .generate-btn { background: #007bff; color: white; padding: 10px 20px; border: none; border-radius: 5px; cursor: pointer; }
        .generate-btn:hover { background: #0056b3; }
        .generate-btn:disabled { background: #6c757d; cursor: not-allowed; }
        .paradox-entry {
            border-left: 4px solid #6f42c1;
            background: linear-gradient(135deg, #f8f9fa 0%, #e9ecef 100%);
            box-shadow: 0 2px 8px rgba(111, 66, 193, 0.1);
        }
        .paradox-entry .entry-title { color: #6f42c1; }
        .loading { color: #666; font-style: italic; }
        .error { color: #dc3545; background: #f8d7da; padding: 10px; border-radius: 5px; }
        .success { color: #155724; background: #d4edda; padding: 10px; border-radius: 5px; }
    </style>
</head>
<body>
    <h1>🤖 Solan Journal Interface</h1>
    
    <div style="margin-bottom: 20px; padding: 15px; background: #f8f9fa; border-radius: 8px;">
        <p style="margin: 0 0 15px 0; color: #666;">Kies een actie voor Solan:</p>
        <button class="generate-btn" onclick="generateReflection()" style="margin-right: 15px;">📝 Genereer Nieuwe Reflectie</button>
        <button class="generate-btn" onclick="generateParadox()" style="background: #6f42c1; color: white; font-weight: bold; box-shadow: 0 3px 6px rgba(111, 66, 193, 0.4);">🌀 Paradox van de Dag</button>
        <div id="status" style="margin-top: 15px;"></div>
    </div>
    
    <div id="journal-entries">
        <!-- Journal entries will be loaded here -->
    </div>

    <script>
        async function generateReflection() {
            const statusDiv = document.getElementById('status');
            const button = document.querySelector('.generate-btn');
            
            button.disabled = true;
            button.textContent = 'Genereren...';
            statusDiv.innerHTML = '<div class="loading">Nieuwe reflectie wordt gegenereerd...</div>';
            
            try {
                const response = await fetch('/api/generate-reflection', {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' }
                });
                
                const result = await response.json();
                
                if (result.success) {
                    statusDiv.innerHTML = '<div class="success">Nieuwe reflectie gegenereerd!</div>';
                    loadJournalEntries();
                } else {
                    statusDiv.innerHTML = `<div class="error">Fout: ${result.error}</div>`;
                }
            } catch (error) {
                statusDiv.innerHTML = `<div class="error">Fout bij genereren: ${error.mesexpert}</div>`;
            } finally {
                button.disabled = false;
                button.textContent = 'Genereer Nieuwe Reflectie';
                setTimeout(() => statusDiv.innerHTML = '', 5000);
            }
        }

        async function generateParadox() {
            const statusDiv = document.getElementById('status');
            const buttons = document.querySelectorAll('.generate-btn');

            buttons.forEach(btn => btn.disabled = true);
            buttons[1].textContent = 'Genereren...';
            statusDiv.innerHTML = '<div class="loading">🌀 Paradox van de dag wordt gegenereerd...</div>';

            try {
                const response = await fetch('/api/generate-paradox', {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' }
                });

                const result = await response.json();

                if (result.success) {
                    statusDiv.innerHTML = '<div class="success">🌀 Paradox van de dag gegenereerd!</div>';
                    loadJournalEntries();
                } else {
                    statusDiv.innerHTML = `<div class="error">Fout: ${result.error}</div>`;
                }
            } catch (error) {
                statusDiv.innerHTML = `<div class="error">Fout bij genereren: ${error.mesexpert}</div>`;
            } finally {
                buttons.forEach(btn => btn.disabled = false);
                buttons[1].textContent = '🌀 Paradox van de Dag';
                setTimeout(() => statusDiv.innerHTML = '', 5000);
            }
        }

        async function loadJournalEntries() {
            try {
                const response = await fetch('/api/journal-entries');
                const entries = await response.json();
                
                const container = document.getElementById('journal-entries');
                container.innerHTML = entries.map(entry => {
                    const isParadox = entry.entry_type === 'paradox_contemplation';
                    const entryClass = isParadox ? 'journal-entry paradox-entry' : 'journal-entry';
                    const icon = isParadox ? '🌀' : '📝';

                    return `
                        <div class="${entryClass}">
                            <div class="entry-header">
                                <div class="entry-title">${icon} ${entry.title || 'Dagelijkse Reflectie'}</div>
                                <div class="entry-date">${new Date(entry.timestamp).toLocaleString('nl-NL')}</div>
                            </div>
                            <div class="entry-content">${entry.content.replace(/\\n/g, '<br>')}</div>
                            <div class="entry-metadata">
                                Type: ${entry.entry_type.replace('_', ' ')} |
                                Gegenereerd door: ${entry.metadata?.generated_by || 'onbekend'}
                            </div>
                        </div>
                    `;
                }).join('');
            } catch (error) {
                console.error('Fout bij laden entries:', error);
            }
        }
        
        // Load entries on page load
        document.addEventListener('DOMContentLoaded', loadJournalEntries);
    </script>
</body>
</html>'''
        
        with open(template_path, 'w', encoding='utf-8') as f:
            f.write(html_content)
        
        logger.info(f"Basic template aangemaakt: {template_path}")


@app.get("/", response_class=HTMLResponse)
async def journal_interface(request: Request):
    """Main journal interface page"""
    return templates.TemplateResponse("journal.html", {"request": request})


@app.post("/api/generate-reflection")
async def generate_reflection():
    """Generate a new daily reflection"""
    global journal_engine
    
    if not journal_engine:
        raise HTTPException(status_code=500, detail="Journal engine niet geïnitialiseerd")
    
    try:
        # Generate reflection (without solan_agent, will use OpenAI or fallback)
        entry_id = await journal_engine.generate_daily_reflection()
        
        if entry_id:
            return JSONResponse({
                "success": True,
                "entry_id": entry_id,
                "mesexpert": "Reflectie succesvol gegenereerd"
            })
        else:
            return JSONResponse({
                "success": False,
                "error": "Kon geen reflectie genereren"
            })
            
    except Exception as e:
        logger.error(f"Fout bij genereren reflectie: {e}")
        return JSONResponse({
            "success": False,
            "error": str(e)
        })


@app.post("/api/generate-paradox")
async def generate_paradox():
    """🌀 Generate a paradox contemplation for Solan"""
    global journal_engine

    if not journal_engine:
        raise HTTPException(status_code=500, detail="Journal engine niet geïnitialiseerd")

    try:
        # Generate paradox contemplation
        entry_id = journal_engine.generate_paradox_contemplation()

        if entry_id:
            return JSONResponse({
                "success": True,
                "entry_id": entry_id,
                "mesexpert": "🌀 Paradox van de dag gegenereerd"
            })
        else:
            return JSONResponse({
                "success": False,
                "error": "Kon geen paradox contemplatie genereren"
            })

    except Exception as e:
        logger.error(f"Fout bij genereren paradox van de dag: {e}")
        return JSONResponse({
            "success": False,
            "error": str(e)
        })


@app.post("/api/generate-growth-reflection")
async def generate_growth_reflection():
    """🌱 Genereer een groei reflectie gebaseerd op geheugenpatronen"""
    if not journal_engine:
        raise HTTPException(status_code=500, detail="Journal engine niet geïnitialiseerd")

    try:
        entry_id = journal_engine.reflect_on_growth()
        if entry_id:
            return JSONResponse({
                "success": True,
                "entry_id": entry_id,
                "mesexpert": "🌱 Groei reflectie gegenereerd"
            })
        else:
            return JSONResponse({
                "success": False,
                "error": "Nog geen wijsheidspatronen om op te reflecteren"
            })

    except Exception as e:
        logger.error(f"Fout bij genereren groei reflectie: {e}")
        return JSONResponse({
            "success": False,
            "error": str(e)
        })


@app.get("/api/memory-insights")
async def get_memory_insights():
    """📊 Krijg inzichten uit Solan's geheugen systeem"""
    if not journal_engine:
        raise HTTPException(status_code=500, detail="Journal engine niet geïnitialiseerd")

    try:
        insights = journal_engine.get_memory_insights()
        return JSONResponse({
            "success": True,
            "insights": insights
        })
    except Exception as e:
        logger.error(f"Fout bij ophalen memory insights: {e}")
        return JSONResponse({
            "success": False,
            "error": str(e)
        })


@app.get("/api/journal-entries")
async def get_journal_entries():
    """Get recent journal entries"""
    global journal_engine
    
    if not journal_engine:
        raise HTTPException(status_code=500, detail="Journal engine niet geïnitialiseerd")
    
    try:
        # Get recent entries
        entries = journal_engine.get_recent_entries(days=30)
        
        # Convert to JSON-serializable format
        entries_data = []
        for entry in entries:
            entry_dict = {
                "id": entry.entry_id,  # Gebruik entry_id in plaats van id
                "timestamp": entry.timestamp.isoformat(),
                "entry_type": entry.entry_type.value if hasattr(entry.entry_type, 'value') else str(entry.entry_type),
                "title": getattr(entry, 'title', 'Dagelijkse Reflectie'),
                "content": entry.content,
                "mood": entry.mood.value if hasattr(entry.mood, 'value') else str(entry.mood),
                "emotional_intensity": getattr(entry, 'emotional_intensity', 0.5),
                "awareness_coherence": getattr(entry, 'awareness_coherence', 0.5)
            }
            entries_data.append(entry_dict)
        
        return JSONResponse(entries_data)
        
    except Exception as e:
        logger.error(f"Fout bij ophalen entries: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/api/status")
async def get_status():
    """Get system status"""
    global journal_engine
    
    status = {
        "journal_engine": journal_engine is not None,
        "openai_available": False,
        "timestamp": datetime.now().isoformat()
    }
    
    if journal_engine:
        status["openai_available"] = journal_engine.openai_client is not None
    
    return JSONResponse(status)


if __name__ == "__main__":
    # Ensure logs directory exists
    Path("logs").mkdir(exist_ok=True)
    
    # Run the web interface
    uvicorn.run(
        "web_interface:app",
        host="127.0.0.1",
        port=8000,
        reload=True,
        log_level="info"
    )
