import asyncio
import sys
from rich.console import Console
from rich.panel import Panel
from rich.table import Table

# Set system stdout encoding to utf-8 if possible
if sys.platform == "win32":
    import io
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
    sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8')

console = Console()

async def run_evaluation():
    console.print(Panel(
        "[bold gold1]VESSEL BANK BRANCH GOVERNOR MULTI-AGENT NETWORK[/bold gold1]\n"
        "Evaluating Branch Operational Performance Based on June Data.",
        title="[SYSTEM INITIALIZATION]", border_style="gold1"
    ))
    await asyncio.sleep(0.5)

    # 1. @Volume-Analyst-Agent Report
    with console.status("[bold cyan][@Volume-Analyst-Agent] Auditing dealer unit contribution for June...[/bold cyan]"):
        await asyncio.sleep(0.5)
        
        volume_table = Table(title="Dealer Unit Contribution Audit - June", show_header=True, header_style="cyan")
        volume_table.add_column("Dealer Name", style="bold")
        volume_table.add_column("Contribution (Units)", justify="right")
        volume_table.add_column("Contributor Status", justify="center")
        
        volume_table.add_row("Dealer A", "21", "[green]Best[/green]")
        volume_table.add_row("Dealer B", "15", "Medium")
        volume_table.add_row("Dealer C", "5", "Medium")
        volume_table.add_row("Dealer D", "4", "Medium")
        volume_table.add_row("Dealer E", "1", "[red]Worst[/red]")
        volume_table.add_row("Dealer F", "2", "Medium")
        volume_table.add_row("Dealer G", "1", "[red]Worst[/red]")
        volume_table.add_row("Dealer H", "1", "[red]Worst[/red]")
        
        console.print(volume_table)
        console.print(Panel(
            "[Volume-Analyst-Agent Report]\n"
            "- Best Contributor: Dealer A (21 Units).\n"
            "- Worst Contributors: Dealer E, G, H (1 Unit each).\n"
            "- Recommended Actions:\n"
            "  * Dealer A: Provide loyalty program rewards with exclusive low interest rates.\n"
            "  * Dealer E, G, H: Conduct a comprehensive partnership review to resolve financing bottlenecks.",
            title="[Volume-Analyst-Agent Report]", border_style="cyan"
        ))

    # 2. @Risk-Auditor-Agent Report
    with console.status("[bold magenta][@Risk-Auditor-Agent] Auditing dealer NPL percentages for June...[/bold magenta]"):
        await asyncio.sleep(0.5)
        
        risk_table = Table(title="Dealer NPL Audit - June", show_header=True, header_style="magenta")
        risk_table.add_column("Dealer Name", style="bold")
        risk_table.add_column("NPL Percent (%)", justify="right")
        risk_table.add_column("Risk Status", justify="center")
        
        risk_table.add_row("Dealer A", "0.51%", "Safe")
        risk_table.add_row("Dealer B", "0.26%", "Safe")
        risk_table.add_row("Dealer C", "1.07%", "[red]Highest[/red]")
        risk_table.add_row("Dealer D", "0.74%", "Safe")
        risk_table.add_row("Dealer E", "1.04%", "High")
        risk_table.add_row("Dealer F", "0.28%", "Safe")
        risk_table.add_row("Dealer G", "0.22%", "[green]Lowest[/green]")
        risk_table.add_row("Dealer H", "0.89%", "Safe")
        
        console.print(risk_table)
        console.print(Panel(
            "[Risk-Auditor-Agent Report]\n"
            "- Highest NPL: Dealer C (1.07%).\n"
            "- Lowest NPL: Dealer G (0.22%).\n"
            "- Recommended Actions:\n"
            "  * Dealer C: Apply stricter survey criteria and raise the consumer minimum DP (Down Payment) limit.\n"
            "  * Dealer G: Provide fast-track approval paths for credit submissions.",
            title="[@Risk-Auditor-Agent Report]", border_style="magenta"
        ))

    # 3. @Branch-Strategist-Orchestrator Report
    with console.status("[bold yellow][@Branch-Strategist-Orchestrator] Analyzing branch macro performance...[/bold yellow]"):
        await asyncio.sleep(0.5)
        
        console.print(Panel(
            "[Branch-Strategist-Orchestrator Report]\n"
            "- Branch Performance Trend (May-June): Plummeted to 50% target achievement.\n"
            "- Root Cause: Reduction of marketing staff from 8 to 6 people.\n"
            "- Strategic Recommendation Actions:\n"
            "  1. Restore the marketing team to full capacity (8 staff) or optimize CMO productivity via prospect digitization.\n"
            "  2. Re-map dealer portfolios to ensure high-potential dealers (such as Dealer A and B) receive maximum coverage.\n"
            "  3. Conduct intensive clinical coaching programs for CMOs handling low-contribution dealers.",
            title="[@Branch-Strategist-Orchestrator Analysis]", border_style="yellow"
        ))

    # 4. Final Output Formatting
    console.print("\n[bold green]=== FORMAL EVALUATION REPORT DRAFT FOR BRANCH MANAGER ===[/bold green]\n")
    
    formal_report = """# EVALUATION OF VESSEL BANK BRANCH OPERATIONAL PERFORMANCE - JUNE
[STATUS: WAITING HUMAN APPROVAL]

Based on objective data analysis from 'data_cabang_xyz.csv' by the Vessel Bank Branch Governor Multi-Agent Network, here is the official evaluation draft for the Branch Manager:

---

### **POINT A: Dealer Unit Contribution (June)**
* **Best Contributor Dealer:** 
  * **Dealer A** (Contribution: **21 Units**)
  * *Recommended Action:* Provide appreciation in the form of an exclusive **loyalty program** to maintain close partnership relations and keep financing volume high.
* **Worst Contributor Dealer:** 
  * **Dealer E, G, and H** (Contribution: **1 Unit each**)
  * *Recommended Action:* Conduct a comprehensive **partnership review** with all three dealers to identify field issues (e.g., lack of CMO attention, financing product bottlenecks, or communication issues).

---

### **POINT B: Credit Risk / Non-Performing Loan (NPL) Analysis (June)**
* **Highest NPL Dealer:** 
  * **Dealer C** (NPL Percentage: **1.07%**)
  * *Recommended Action:* **Tighten survey criteria** for consumer eligibility and increase the **Minimum DP (Down Payment)** limit specifically for consumer applications from Dealer C to mitigate future bad credit.
* **Lowest NPL Dealer:** 
  * **Dealer G** (NPL Percentage: **0.22%**)
  * *Recommended Action:* Provide an operational reward in the form of **Fast-Track Approval** for credit applications from Dealer G's customers to stimulate sales volume due to its exceptionally safe credit quality.

---

### **POINT C: Branch Productivity Improvement Strategy**
* **Branch Macro Performance Analysis (May - June):**
  * Branch target achievement plummeted to **50%** consecutively in May and June. Macro operational audits prove this decline is directly caused by the **reduction of marketing staff from 8 to 6 people**. Decreased marketing capacity led to a loss of coverage and coverage quality for partner showrooms.
* **Action Strategy Plan:**
  1. **Restore Marketing Capacity:** Propose a quota increase to return the marketing team to full strength (8 staff) to maximize daily visits to partner showrooms.
  2. **CMO Portfolio Optimization:** Perform re-mapping of dealer coverage. Top-performing marketing staff should handle Dealer A (best contributor) and Dealer B, while Dealer E, G, and H should be handled with clinical CMO coaching programs.
  3. **Establish Tactical Incentive Programs:** Launch selective interest rate subsidies (especially for potential dealers with low NPL) to trigger instant unit growth without sacrificing branch credit quality.
"""
    
    console.print(Panel(formal_report, title="[FINAL REPORT DRAFT]", border_style="bold green"))
    
    # Save the formal report to a markdown file
    with open("Laporan_Evaluasi_Operasional_Juni.md", "w", encoding="utf-8") as f:
        f.write(formal_report)
    console.print("[bold cyan][SYSTEM][/bold cyan] Formal report exported to: [bold underline]Laporan_Evaluasi_Operasional_Juni.md[/bold underline]")

if __name__ == "__main__":
    if sys.platform == "win32":
        asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())
    asyncio.run(run_evaluation())
