import asyncio
import sys
from rich.live import Live
from rich.text import Text
from rich.console import Console
from rich.panel import Panel

console = Console()

async def simulate_agent_debate(prompt: str):
    console.print(Panel(
        "[bold green]🚀 VESSEL BANK MULTI-AGENT ORCHESTRATION ENGINE ACTIVATED[/bold green]\n"
        "Triggering Agent-to-Agent (A2A) collaboration using ADK Multi-Agent Graph Framework...",
        border_style="green"
    ))
    await asyncio.sleep(1)

    # 1. Trigger Sales Agent
    with console.status("[bold cyan][Agent 1: Sales & Growth Specialist] Analyzing market opportunities...[/bold cyan]"):
        await asyncio.sleep(2)
        console.print(Panel(
            "📢 [bold cyan]SALES AGENT RECOMMENDATION:[/bold cyan]\n"
            "Target achievement dropped due to intense competitor interest rate cuts (1.5% lower).\n"
            "Tactical suggestion: Allocate an additional interest commission subsidy of [bold green]IDR 25,000,000[/bold green] "
            "for Showroom Garuda Motor and Showroom Raya Automobil to recapture market share.",
            title="[SALES & GROWTH AGENT]", border_style="cyan"
        ))

    # 2. Trigger Risk Agent (Debate/Guardrail)
    with console.status("[bold magenta][Agent 2: Risk & NPL Auditor] Validating branch credit risk...[/bold magenta]"):
        await asyncio.sleep(2)
        console.print(Panel(
            "🛑 [bold magenta]RISK AGENT REBUTTAL (AUDIT REPORT):[/bold magenta]\n"
            "- [green]Garuda Motor:[/green] Volume drop 30%, NPL 1.2%. Recommendation: [bold green]APPROVED[/bold green].\n"
            "- [red]Raya Automobil:[/red] Volume drop 50%, NPL 3.5%. [bold red]CRITICAL WARNING![/bold red] NPL is above the 2.0% threshold.\n"
            "Decision: Vetoing Sales Agent's proposal. Subsidy for Raya Automobil [bold red]MUST BE BLOCKED[/bold red] to prevent default.",
            title="[RISK & NPL CONTROLLER]", border_style="magenta"
        ))

    # 3. Orchestrator Summarizes Results & Triggers HITL
    with console.status("[bold yellow][Orchestrator] Consolidating committee final decision...[/bold yellow]"):
        await asyncio.sleep(1.5)
        
    console.print("\n")
    console.print(Panel(
        f"[bold red]⚠️ [HITL] FINAL VERIFICATION GATEWAY FOR COMMITTEE CHAIR (BRANCH MANAGER)[/bold red]\n\n"
        f"Based on the sub-agent A2A collaborative debate, here is the drafted optimal strategy:\n"
        f"1. [✔] Showroom Garuda Motor -> Allocated Interest Subsidy of IDR 25,000,000 (Safe NPL)\n"
        f"2. [❌] Showroom Raya Automobil -> Automatically Rejected (NPL 3.5% Violates Guidelines)\n\n"
        f"Do you, as the Branch Manager, approve this final committee decision?",
        title="[VESSEL BANK SECURITY GATEWAY]", border_style="red"
    ))
    
    choice = console.input("[bold yellow]Type (Y for Execute / N for Cancel): [/bold yellow]").strip().upper()
    if choice == "Y":
        console.print("\n[bold green]STATUS: SUCCESS.[/bold green] Strategy locked. Writing report to file...")
        
        # Automatically export results to a separate file
        with open("Laporan_Strategi_Cabang.md", "w", encoding="utf-8") as f:
            f.write("# VESSEL BANK BRANCH GROWTH STRATEGY - OUTCOME REPORT\n")
            f.write("==================================================\n\n")
            f.write("### 📌 CREDIT COMMITTEE APPROVAL STATUS: APPROVED\n")
            f.write("As the Branch Manager, you have approved the following tactical fund allocation draft:\n\n")
            f.write("1. [✔] **Showroom Garuda Motor** -> Allocated Interest Subsidy of IDR 25,000,000 (NPL Evaluation: 1.2% - SAFE)\n")
            f.write("2. [❌] **Showroom Raya Automobil** -> AUTOMATICALLY REJECTED (NPL Evaluation: 3.5% - EXCEEDS SAFE LIMIT)\n\n")
            f.write("---\n")
            f.write("*Trajectory logs have been successfully secured to Spanner Graph for internal audit purposes.*\n")
            
        console.print("[bold cyan][SYSTEM][/bold cyan] Report successfully exported to file: [bold underline]Laporan_Strategi_Cabang.md[/bold underline] 📄")
    else:
        console.print("\n[bold red]STATUS: ABORTED.[/bold red] Draft cancelled by the Branch Manager.")

async def main():
    print("\n")
    await simulate_agent_debate("Analyze used car sales decline this month")

if __name__ == "__main__":
    if sys.platform == "win32":
        asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())
    asyncio.run(main())