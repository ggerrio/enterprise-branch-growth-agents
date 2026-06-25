import asyncio
import sys
import json
import os
from datetime import datetime
from rich.console import Console
from rich.panel import Panel
from rich.table import Table
from data_parser import parse_data_cabang_real

console = Console()

# ----------------------------------------------------------------------
# 1. MAIN & COMPETITOR DATABASE SIMULATION
# ----------------------------------------------------------------------
DB_PATH = "Dealer_Sales_and_NPL.csv"
HISTORY_PATH = "historical_decisions.json"

def get_competitor_rate_live() -> float:
    """Simulates Competitor Intelligence Agent scraping live market data."""
    # Returns dynamic competitor rate (e.g., competitor leasing interest rate dropped by 1.5%)
    return 1.5

# ----------------------------------------------------------------------
# 2. DIGITAL FEATURE: AUTOMATED EMAIL/WHATSAPP NOTIFICATION
# ----------------------------------------------------------------------
def send_cmo_alert(cmo_name: str, showroom: str, budget: str):
    """Simulates sending tactical instructions automatically via Twilio API / SMTP Email."""
    console.print(Panel(
        f"✉️  [bold green]CMO NOTIFICATION SYSTEM (ALERT DISPATCHED)[/bold green]\n"
        f"To: [underline]{cmo_name}@vesselbank.com[/underline]\n"
        f"Subject: Execution of Interest Commission Subsidy Program - {showroom}\n\n"
        f"Hello {cmo_name}, the Branch Manager has approved a subsidy budget of {budget} "
        f"for your managed dealer ({showroom}). Please initiate market penetration today!",
        title="[OUTBOUND NOTIFICATION GATEWAY]", border_style="green"
    ))

# ----------------------------------------------------------------------
# 3. OBSERVABILITY FEATURE: RECORD HISTORICAL TRAJECTORY
# ----------------------------------------------------------------------
def save_to_history(showroom: str, budget: int, status: str, risk_level: float, cmo: str):
    """Logs the committee decision trajectory into a JSON file for the dashboard feed."""
    history_data = []
    if os.path.exists(HISTORY_PATH):
        with open(HISTORY_PATH, "r") as f:
            try:
                history_data = json.load(f)
            except json.JSONDecodeError:
                history_data = []
                
    new_log = {
        "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "showroom": showroom,
        "allocated_budget": budget if status == "APPROVED" else 0,
        "npl_checked": risk_level,
        "cmo_handler": cmo,
        "final_status": status
    }
    history_data.append(new_log)
    with open(HISTORY_PATH, "w") as f:
        json.dump(history_data, f, indent=4)

# ----------------------------------------------------------------------
# 4. CORE ENGINE: MULTI-AGENT COLLABORATION & DEBATE GRAPH
# ----------------------------------------------------------------------
import csv

async def run_multi_agent_suite():
    console.print(Panel(
        "[bold gold1]🚀 WELCOME TO VESSEL BANK ENTERPRISE MULTI-AGENT GOVERNANCE SUITE[/bold gold1]\n"
        "Engine: Multi-Agent Collaboration Graph (Sales Agent, Risk Agent, & Competitor Scout).",
        title="[VESSEL BANK AI SYSTEM]", border_style="gold1"
    ))

    # ----------------------------------------------------------------------
    # AUTOMATIC DATA READ & REASONING ENGINE (Reads directly from CSV)
    # ----------------------------------------------------------------------
    showroom_target = None
    cmo_handler = None
    npl_rate = 0.0
    calculated_budget = 0
    subsidi_per_unit_drop = 1500000 

    # Execute dynamic extraction from data_cabang_xyz.csv
    try:
        cleaned_dealers = parse_data_cabang_real("data_cabang_xyz.csv")
        for dealer in cleaned_dealers:
            vol_last = dealer["Booking_Volume_Last_Month"]
            vol_this = dealer["Booking_Volume_This_Month"]
            
            if vol_this < vol_last:
                drop_unit = vol_last - vol_this
                # Find dealers that dropped but pass the strict rule NPL <= 2.0%
                if dealer["NPL_Percent"] <= 2.0 and dealer["NPL_Percent"] > 0:
                    showroom_target = dealer["Showroom_Name"]
                    cmo_handler = dealer["CMO_Handler_Name"]
                    npl_rate = dealer["NPL_Percent"]
                    calculated_budget = drop_unit * subsidi_per_unit_drop
                    break
    except Exception as e:
        console.print(f"[bold red]Error processing real data pipeline:[/bold red] {str(e)}")
        return

    # ----------------------------------------------------------------------
    # MULTI-AGENT A2A DIALOGUE WORKFLOW (Dynamic based on calculation)
    # ----------------------------------------------------------------------
    # Market Intelligence movement
    with console.status("[bold yellow]Competitor Intelligence Agent monitoring competitor leasing rates...[/bold yellow]"):
        await asyncio.sleep(1.2)
        comp_gap = get_competitor_rate_live()
        console.print(f"🔍 [bold yellow][COMPETITOR INTEL][/bold yellow] Detected competitor leasing cutting commission rates by [bold red]-{comp_gap}%[/bold red] in Jabodetabek area.")

    # Agent 1 debate (Sales)
    with console.status("[bold cyan]Sales & Growth Agent formulating counter-strategy...[/bold cyan]"):
        await asyncio.sleep(1.2)
        console.print(Panel(
            f"📢 [bold cyan]SALES AGENT STRATEGY PROPOSAL:[/bold cyan]\n"
            f"To offset the competitor's rate gap ({comp_gap}%), we must secure the volume of [bold]{showroom_target}[/bold].\n"
            f"According to CSV data, this showroom is experiencing a sales decline. Recommended balancing tactical funds:\n"
            f"👉 [bold green]IDR {calculated_budget:,}[/bold green] interest subsidy to win back consumers.",
            title="[PERSONA 1: SALES & GROWTH]", border_style="cyan"
        ))

    # Agent 2 debate (Risk Guard)
    with console.status("[bold magenta]Risk & NPL Auditor screening regulations...[/bold magenta]"):
        await asyncio.sleep(1.2)
        console.print(Panel(
            f"🛡️ [bold magenta]RISK AGENT AUDIT:[/bold magenta]\n"
            f"Checking branch database for {showroom_target}...\n"
            f"- Bad Credit Ratio (NPL): {npl_rate}% (Below maximum tolerance limit of 2.0%).\n"
            f"Risk Decision: [bold green]PASSED / SAFE[/bold green]. Budget allocation of IDR {calculated_budget:,} is cleared for release.",
            title="[PERSONA 2: RISK CONTROLLER]", border_style="magenta"
        ))

    # Orchestrator triggers HITL
    console.print(Panel(
        f"[bold red]⚠️ [HITL CONTROL] HUMAN INTERVENTION REQUIRED BEFORE FUND RELEASE[/bold red]\n\n"
        f"The application is about to execute a commission subsidy program for [bold]{showroom_target}[/bold] valued at [bold green]IDR {calculated_budget:,}[/bold green].",
        title="[VESSEL BANK SECURITY GUARD]", border_style="red"
    ))

    choice = console.input("[bold yellow]Approve this AI committee recommendation? (Y/N): [/bold yellow]").strip().upper()
    
    if choice == "Y":
        save_to_history(showroom_target, calculated_budget, "APPROVED", npl_rate, cmo_handler)
        console.print("\n[bold green][✔ SYSTEM][/bold green] Trajectory trace successfully saved to `historical_decisions.json`.")
        await asyncio.sleep(0.8)
        send_cmo_alert(cmo_handler, showroom_target, f"IDR {calculated_budget:,}")
        show_historical_dashboard()
    else:
        save_to_history(showroom_target, calculated_budget, "REJECTED", npl_rate, cmo_handler)
        console.print("\n[bold red]❌ SYSTEM:[/bold red] Allocation cancelled. Trajectory frozen with REJECTED status.")

# ----------------------------------------------------------------------
# 5. ADDITIONAL FEATURE: HISTORICAL ANALYTICS DASHBOARD TERMINAL
# ----------------------------------------------------------------------
def show_historical_dashboard():
    """Renders the execution history table of branch decisions (Data Observability)."""
    if not os.path.exists(HISTORY_PATH):
        return
        
    with open(HISTORY_PATH, "r") as f:
        logs = json.load(f)
        
    table = Table(title="📊 VESSEL BANK BRANCH TRAJECTORY DASHBOARD", show_header=True, header_style="bold gold1")
    table.add_column("Date/Time", style="dim")
    table.add_column("Showroom Name")
    table.add_column("CMO Handler")
    table.add_column("NPL Check")
    table.add_column("Disbursed Funds")
    table.add_column("Final Status")
    
    for log in logs:
        status_color = "[green]APPROVED[/green]" if log["final_status"] == "APPROVED" else "[red]REJECTED[/red]"
        table.add_row(
            log["timestamp"],
            log["showroom"],
            log["cmo_handler"],
            f"{log['npl_checked']}%",
            f"IDR {log['allocated_budget']:,}",
            status_color
        )
        
    console.print("\n")
    console.print(table)

if __name__ == "__main__":
    if sys.platform == "win32":
        asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())
    asyncio.run(run_multi_agent_suite())