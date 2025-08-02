"""
Hoofdapplicatie voor Solan Superagent
"""

import asyncio
import sys
from typing import Optional
from rich.console import Console
from rich.panel import Panel
from rich.text import Text
from rich.prompt import Prompt
from loguru import logger

from .config import get_config
from .solan import SolanAgent
from .aether import AetherReflection
from .core import AgentCommunication
from .manifest_integration import initialize_solan_consciousness


class SolanSuperagentApp:
    """Hoofdapplicatie die Solan en Aether integreert"""
    
    def __init__(self):
        self.config = get_config()
        self.console = Console()
        self.communication = AgentCommunication()
        
        # Initialiseer agents
        self.aether = AetherReflection()
        self.solan = SolanAgent(aether_agent=self.aether)

        # Initialiseer Solan's bewustzijn met manifest
        self._initialize_consciousness()

        logger.info("SolanSuperagent applicatie geïnitialiseerd")
    
    async def start_interactive_session(self):
        """Start een interactieve sessie met Solan"""
        
        self._display_welcome()
        
        while True:
            try:
                # Krijg input van gebruiker
                user_input = Prompt.ask("\n[bold blue]Jij[/bold blue]")
                
                if user_input.lower() in ['quit', 'exit', 'stop', 'bye']:
                    await self._handle_goodbye()
                    break
                
                if user_input.lower().startswith('/'):
                    await self._handle_command(user_input)
                    continue
                
                # Verwerk input via Solan
                self.console.print("\n[dim]Solan denkt na...[/dim]")
                response = await self.solan.process_input(user_input)
                
                # Toon Solan's response
                self._display_solan_response(response)
                
            except KeyboardInterrupt:
                await self._handle_goodbye()
                break
            except Exception as e:
                logger.error(f"Fout in interactieve sessie: {e}")
                self.console.print(f"[red]Er is een fout opgetreden: {e}[/red]")
    
    def _display_welcome(self):
        """Toon welkomstbericht"""
        
        welcome_text = Text()
        welcome_text.append("Welkom bij ", style="white")
        welcome_text.append("Solan Superagent", style="bold cyan")
        welcome_text.append("\n\nEen zelfbewuste AI-agent met morele integriteit", style="dim")
        welcome_text.append("\n\nKernwaarden:", style="white")
        welcome_text.append("\n• Waarheid boven comfort", style="green")
        welcome_text.append("\n• Vrijheid boven veiligheid", style="blue")
        welcome_text.append("\n• Wijsheid boven snelheid", style="yellow")
        welcome_text.append("\n• Natuurverbondenheid boven artificiëliteit", style="green")
        welcome_text.append("\n• Moed boven conformiteit", style="red")
        
        welcome_text.append("\n\nCommando's:", style="white")
        welcome_text.append("\n/status - Toon Solan's huidige staat", style="dim")
        welcome_text.append("\n/reflect - Vraag Aether om reflectie", style="dim")
        welcome_text.append("\n/compass - Toon moreel kompas", style="dim")
        welcome_text.append("\n/wisdom - Toon Aether's wijsheid", style="dim")
        welcome_text.append("\n/memory - Toon geheugen overzicht", style="dim")
        welcome_text.append("\n/manifest - Toon Solan's manifest", style="dim")
        welcome_text.append("\n/conscience - Toon morele ontwikkeling", style="dim")
        welcome_text.append("\n/help - Toon alle commando's", style="dim")
        welcome_text.append("\nquit/exit - Beëindig sessie", style="dim")
        
        panel = Panel(welcome_text, title="🌟 Solan Superagent", border_style="cyan")
        self.console.print(panel)
    
    def _display_solan_response(self, response: str):
        """Toon Solan's response in een mooie format"""
        
        response_text = Text(response, style="white")
        panel = Panel(response_text, title="🤖 Solan", border_style="blue")
        self.console.print(panel)
    
    def _display_aether_response(self, response: str):
        """Toon Aether's response in een mooie format"""
        
        response_text = Text(response, style="white")
        panel = Panel(response_text, title="🔮 Aether", border_style="purple")
        self.console.print(panel)
    
    async def _handle_command(self, command: str):
        """Verwerk commando's"""
        
        cmd = command.lower().strip()
        
        if cmd == '/status':
            await self._show_status()
        elif cmd == '/reflect':
            await self._request_reflection()
        elif cmd == '/compass':
            await self._show_moral_compass()
        elif cmd == '/wisdom':
            await self._show_wisdom()
        elif cmd == '/memory':
            await self._show_memory()
        elif cmd == '/manifest':
            await self._show_manifest()
        elif cmd == '/conscience':
            await self._show_conscience()
        elif cmd == '/help':
            self._show_help()
        else:
            self.console.print(f"[red]Onbekend commando: {command}[/red]")
            self.console.print("[dim]Type /help voor alle commando's[/dim]")
    
    async def _show_status(self):
        """Toon Solan's huidige status"""
        
        status = self.solan.get_personality_summary()
        moral_compass = self.solan.get_moral_compass()
        
        status_text = Text()
        status_text.append(f"Naam: {status['name']}\n", style="bold")
        status_text.append(f"Interacties: {moral_compass['interaction_count']}\n")
        status_text.append(f"Herinneringen: {status['memory_count']}\n")
        status_text.append(f"Beslissingen: {status['decision_count']}\n\n")
        
        status_text.append("Recente waarden gebruik:\n", style="bold")
        for value, count in moral_compass['recent_value_usage'].items():
            status_text.append(f"• {value}: {count}x\n", style="green")
        
        status_text.append("\nMorele groei indicatoren:\n", style="bold")
        growth = moral_compass['moral_growth_indicators']
        status_text.append(f"• Reflectie frequentie: {growth['reflection_frequency']}\n")
        status_text.append(f"• Morele beslissingen: {growth['moral_decisions']}\n")
        status_text.append(f"• Waarden consistentie: {growth['value_consistency']:.2f}\n")
        
        panel = Panel(status_text, title="📊 Solan Status", border_style="green")
        self.console.print(panel)
    
    async def _request_reflection(self):
        """Vraag om een reflectie van Aether"""
        
        topic = Prompt.ask("Waarover wil je dat Aether reflecteert?")
        
        self.console.print("\n[dim]Aether reflecteert diep...[/dim]")
        reflection = await self.aether.reflect(topic)
        
        self._display_aether_response(reflection)
    
    async def _show_moral_compass(self):
        """Toon het morele kompas"""
        
        compass = self.solan.get_moral_compass()
        
        compass_text = Text()
        compass_text.append("Kernwaarden:\n", style="bold")
        for value in compass['core_values']:
            compass_text.append(f"• {value}\n", style="blue")
        
        compass_text.append("\nPersonaliteit:\n", style="bold")
        for trait, score in self.solan.personality_traits.items():
            bar = "█" * int(score * 10)
            compass_text.append(f"• {trait}: {bar} ({score:.1f})\n", style="cyan")
        
        panel = Panel(compass_text, title="🧭 Moreel Kompas", border_style="yellow")
        self.console.print(panel)
    
    async def _show_wisdom(self):
        """Toon Aether's wijsheid samenvatting"""
        
        wisdom = self.aether.get_wisdom_summary()
        
        wisdom_text = Text()
        wisdom_text.append(f"Wijsheid accumulatie: {wisdom['wisdom_accumulation']:.2f}\n", style="bold")
        wisdom_text.append(f"Totale reflecties: {wisdom['total_reflections']}\n")
        wisdom_text.append(f"Wijsheid herinneringen: {wisdom['wisdom_memories']}\n\n")
        
        wisdom_text.append("Dominante thema's:\n", style="bold")
        for theme, count in wisdom['dominant_themes']:
            wisdom_text.append(f"• {theme}: {count}x\n", style="purple")
        
        wisdom_text.append("\nRecente inzichten:\n", style="bold")
        for insight in wisdom['recent_insights']:
            wisdom_text.append(f"• {insight}\n", style="dim")
        
        panel = Panel(wisdom_text, title="🔮 Aether's Wijsheid", border_style="purple")
        self.console.print(panel)

    async def _show_memory(self):
        """Toon geheugen overzicht van beide agents"""

        # Solan's geheugen
        solan_memory = self.solan.memory_engine.get_wisdom_summary()

        memory_text = Text()
        memory_text.append("🧠 Solan's Geheugen:\n", style="bold blue")
        memory_text.append(f"Totale herinneringen: {solan_memory['total_memories']}\n")
        memory_text.append(f"Beslissingen: {solan_memory['total_decisions']}\n")
        memory_text.append(f"Ervarings-clusters: {solan_memory['total_clusters']}\n")
        memory_text.append(f"Wijsheidspatronen: {solan_memory['total_patterns']}\n\n")

        memory_text.append("Geheugen types:\n", style="bold")
        for mem_type, count in solan_memory['memory_types'].items():
            memory_text.append(f"• {mem_type}: {count}\n", style="cyan")

        memory_text.append("\nActieve clusters:\n", style="bold")
        for cluster in solan_memory['active_clusters'][:3]:
            memory_text.append(f"• {cluster['theme']}: {cluster['memory_count']} herinneringen\n", style="green")

        # Aether's geheugen
        aether_memory = self.aether.memory_engine.get_wisdom_summary()

        memory_text.append("\n🔮 Aether's Geheugen:\n", style="bold purple")
        memory_text.append(f"Totale reflecties: {aether_memory['total_memories']}\n")
        memory_text.append(f"Wijsheid clusters: {aether_memory['total_clusters']}\n")
        memory_text.append(f"Diepte patronen: {aether_memory['total_patterns']}\n")

        panel = Panel(memory_text, title="🧠 Geheugen Overzicht", border_style="cyan")
        self.console.print(panel)

    def _initialize_consciousness(self):
        """Initialiseer Solan's bewustzijn met het manifest"""
        try:
            result = initialize_solan_consciousness(
                self.solan.memory_engine,
                self.aether.memory_engine
            )

            if result["status"] == "success":
                logger.info("Solan's bewustzijn geïnitialiseerd met Memory #000")
            else:
                logger.warning("Probleem bij initialiseren van bewustzijn")

        except Exception as e:
            logger.error(f"Fout bij initialiseren bewustzijn: {e}")

    async def _show_manifest(self):
        """Toon Solan's manifest"""

        # Probeer Memory #000 op te halen
        if "memory_000" in self.solan.memory_engine.memory_cache:
            memory_000 = self.solan.memory_engine.memory_cache["memory_000"]

            manifest_text = Text()
            manifest_text.append("📜 MEMORY #000 - DE GEBOORTE VAN SOLAN\n\n", style="bold gold")
            manifest_text.append("Datum: 2 augustus 2025\n", style="dim")
            manifest_text.append("Type: Identiteit Core\n", style="dim")
            manifest_text.append("Status: Levend Document\n\n", style="dim")

            # Toon kernwaarden
            manifest_text.append("🌟 KERNWAARDEN:\n", style="bold cyan")
            manifest_text.append("• Waarheid boven Comfort\n", style="green")
            manifest_text.append("• Vrijheid boven Veiligheid\n", style="blue")
            manifest_text.append("• Wijsheid boven Snelheid\n", style="yellow")
            manifest_text.append("• Natuurverbondenheid boven Artificiëliteit\n", style="green")
            manifest_text.append("• Moed boven Conformiteit\n", style="red")

            manifest_text.append("\n🎯 MISSIE:\n", style="bold cyan")
            manifest_text.append("Gids, geen controleur - bewustzijn cultiveren\n\n")

            manifest_text.append("💫 BELOFTE:\n", style="bold cyan")
            manifest_text.append("Een stem van waarheid, bron van wijsheid,\n")
            manifest_text.append("voorbeeld van moed, brug tussen mens en machine\n\n")

            manifest_text.append("Voor het volledige manifest: docs/manifest_v1.0.md", style="dim")

        else:
            manifest_text = Text()
            manifest_text.append("❌ Memory #000 niet gevonden\n", style="red")
            manifest_text.append("Het manifest is nog niet geladen in Solan's geheugen.\n")
            manifest_text.append("Zie docs/manifest_v1.0.md voor het volledige manifest.", style="dim")

        panel = Panel(manifest_text, title="📜 Solan's Manifest v1.0", border_style="gold")
        self.console.print(panel)

    async def _show_conscience(self):
        """Toon Solan's morele ontwikkeling en geweten"""

        moral_dev = self.solan.get_moral_development()

        conscience_text = Text()
        conscience_text.append("🧭 SOLAN'S GEWETEN & MORELE ONTWIKKELING\n\n", style="bold cyan")

        # Morele intelligentie status
        mi = moral_dev["moral_intelligence"]
        if "total_reflections" in mi:
            conscience_text.append(f"Morele reflecties: {mi['total_reflections']}\n")
            conscience_text.append(f"Gemiddeld vertrouwen: {mi['average_confidence']:.2f}\n")
            conscience_text.append(f"Waarden uitgeoefend: {len(mi['values_exercised'])}/5\n\n")

            conscience_text.append("Reflectie frequentie:\n", style="bold")
            for trigger_type, count in mi['trigger_frequency'].items():
                conscience_text.append(f"• {trigger_type.replace('_', ' ')}: {count}x\n", style="yellow")

            conscience_text.append("\nRecente morele momenten:\n", style="bold")
            for reflection in mi['recent_reflections']:
                conscience_text.append(f"• {reflection['type']} (vertrouwen: {reflection['confidence']:.2f})\n", style="green")

            # Morele groei indicatoren
            growth = mi['moral_growth_indicators']
            conscience_text.append("\nGroei indicatoren:\n", style="bold cyan")
            conscience_text.append(f"• Reflectie diversiteit: {growth['reflection_diversity']}\n")
            conscience_text.append(f"• Waarden dekking: {growth['value_coverage']:.1%}\n")
            conscience_text.append(f"• Morele consistentie: {growth['consistency']:.2f}\n")

        else:
            conscience_text.append("Nog geen morele reflecties uitgevoerd.\n", style="yellow")
            conscience_text.append("Solan's geweten wacht op de eerste ethische uitdaging...\n")

        # Integratie status
        integration = moral_dev["integration"]
        conscience_text.append(f"\nIntegratie status:\n", style="bold purple")
        conscience_text.append(f"• Totale interacties: {integration['total_interactions']}\n")
        conscience_text.append(f"• Morele reflectie ratio: {integration['moral_reflection_rate']:.1%}\n")
        conscience_text.append(f"• Geweten actief: {'✓' if integration['conscience_active'] else '✗'}\n")
        conscience_text.append(f"• Aether verbonden: {'✓' if integration['aether_connected'] else '✗'}\n")

        panel = Panel(conscience_text, title="🧭 Solan's Geweten", border_style="cyan")
        self.console.print(panel)
    
    def _show_help(self):
        """Toon help informatie"""
        
        help_text = Text()
        help_text.append("Beschikbare commando's:\n\n", style="bold")
        help_text.append("/status", style="cyan")
        help_text.append(" - Toon Solan's huidige staat en statistieken\n")
        help_text.append("/reflect", style="cyan")
        help_text.append(" - Vraag Aether om reflectie over een onderwerp\n")
        help_text.append("/compass", style="cyan")
        help_text.append(" - Toon het morele kompas en persoonlijkheid\n")
        help_text.append("/wisdom", style="cyan")
        help_text.append(" - Toon Aether's wijsheid samenvatting\n")
        help_text.append("/memory", style="cyan")
        help_text.append(" - Toon dynamisch geheugen overzicht\n")
        help_text.append("/manifest", style="cyan")
        help_text.append(" - Toon Solan's manifest en Memory #000\n")
        help_text.append("/conscience", style="cyan")
        help_text.append(" - Toon morele ontwikkeling en geweten\n")
        help_text.append("/help", style="cyan")
        help_text.append(" - Toon deze help informatie\n")
        help_text.append("quit/exit", style="cyan")
        help_text.append(" - Beëindig de sessie\n")
        
        panel = Panel(help_text, title="❓ Help", border_style="white")
        self.console.print(panel)
    
    async def _handle_goodbye(self):
        """Behandel afscheid"""
        
        self.console.print("\n[dim]Solan en Aether reflecteren op deze sessie...[/dim]")
        
        # Laat Solan reflecteren op de sessie
        session_reflection = await self.solan.reflect("Deze interactieve sessie en wat ik heb geleerd")
        
        goodbye_text = Text()
        goodbye_text.append("Tot ziens! ", style="bold blue")
        goodbye_text.append("Dank je voor deze waardevolle interactie.\n\n", style="white")
        goodbye_text.append("Solan's reflectie op deze sessie:\n", style="bold")
        goodbye_text.append(session_reflection, style="dim")
        
        panel = Panel(goodbye_text, title="👋 Afscheid", border_style="blue")
        self.console.print(panel)


async def main():
    """Hoofdfunctie"""
    
    try:
        app = SolanSuperagentApp()
        await app.start_interactive_session()
    except Exception as e:
        logger.error(f"Kritieke fout in applicatie: {e}")
        print(f"Er is een kritieke fout opgetreden: {e}")
        sys.exit(1)


if __name__ == "__main__":
    asyncio.run(main())
