import asyncio
import os
import sys
from rich.console import Console
from rich.panel import Panel
from rich.table import Table
from google.adk.agents import LlmAgent
from google.adk.models import Gemini
from google.adk.runners import InMemoryRunner
from google.genai import types

# Import our local MCP server
from mcp_server import VesselBankDataServer

console = Console()
mcp_server = VesselBankDataServer()

# ==========================================
# TOOL DEFINITIONS (Day 2 & Day 4 Integration)
# ==========================================

def get_branch_data() -> str:
    """MCP Tool: Retrieves dealer sales performance data and branch NPL status for Vessel Bank."""
    return mcp_server.fetch_branch_records()

def human_in_the_loop_approval(showroom: str, dana_usulan: str) -> str:
    """
    HITL Security Tool (Pillar 5: Zero Ambient Authority).
    Suspends automatic execution and requests physical authentication from the Branch Manager.
    """
    console.print("\n")
    console.print(Panel(
        f"[bold red]⚠️ STRATEGIC FUND OUTFLOW APPROVAL REQUEST[/bold red]\n\n"
        f"🚨 [bold]Target Showroom:[/bold] {showroom}\n"
        f"💰 [bold]Proposed Interest Subsidy:[/bold] {dana_usulan}\n\n"
        f"Do you approve the release of these branch promotional funds?",
        title="[VESSEL BANK SECURITY GUARD]", border_style="red"
    ))
    
    # Suspends execution and waits for manual input from the Branch Manager
    choice = console.input("[bold yellow]Type (Y for Approve / N for Reject): [/bold yellow]").strip().upper()
    
    if choice == "Y":
        return "STATUS: APPROVED. Branch promotional funds locked and program executed."
    else:
        return "STATUS: REJECTED BY MANAGER. Fund allocation cancelled to secure branch NPL."

# ==========================================
# AGENT CONFIGURATION (Day 3 Skills & Core Prompt)
# ==========================================

# Synchronize instruction descriptions with SKILL.md and your .feature file
instruction_prompt = """
You are a professional Vessel Bank Branch Growth Strategy Agent. Your task is to assist the Branch Manager (BM) in formulating promotional tactics.
Whenever instructed, you MUST follow these steps:
1. Call the `get_branch_data` tool to review the showroom situation.
2. Filter showrooms experiencing a volume decline of over 10%.
3. Evaluate their NPL (Maximum NPL tolerance is 2.0%). If it is above 2.0%, BLOCK them and report them as high-risk showrooms.
4. For safe showrooms (NPL < 2.0%), formulate a draft proposal for interest commission subsidies/promotional budgets.
5. IMPORTANT: Before displaying the final answer, if there is a proposed budget allocation, you MUST call the `human_in_the_loop_approval` tool for verification. Never make unilateral financial decisions!
"""

# Using Gemini model for high cognitive evaluation
bcaf_agent = LlmAgent(
    name="Vessel_Bank_Core_Strategy_Agent",
    model=Gemini(model="gemini-3.5-flash"),
    instruction=instruction_prompt,
    tools=[get_branch_data, human_in_the_loop_approval]
)

# ==========================================
# CLI LOOP ENGINE (Claude-like UX)
# ==========================================

async def run_cli():
    runner = InMemoryRunner(agent=bcaf_agent, app_name="vessel_bank_analytics")
    
    session = await runner.session_service.create_session(
        app_name="vessel_bank_analytics", 
        user_id="bm_jakarta"
    )
    
    console.print(Panel(
        "[bold green]Vessel Bank Branch Growth Strategy Agent - Active v1.0.0[/bold green]\n"
        "AI Agent system based on Vibe Coding & Spec-Driven Development ready for use.\n"
        "Type 'exit' or 'quit' to end the session.",
        title="[VESSEL BANK AI SYSTEM]", border_style="green"
    ))

    while True:
        try:
            user_prompt = console.input("\n[bold blue]Branch Manager 🤵 ──> [/bold blue]").strip()
            if not user_prompt:
                continue
            if user_prompt.lower() in ["exit", "quit"]:
                console.print("[bold yellow]Shutting down AI Agent system... Goodbye![/bold yellow]")
                break
            
            with console.status("[bold green]Agent analyzing data & triggering Skills...[/bold green]"):
                # Wrap the prompt string into an official genai Content object
                structured_message = types.Content(
                    role="user", 
                    parts=[types.Part(text=user_prompt)]
                )
                
                # Send structured_message to runner
                async for event in runner.run_async(user_id="bm_jakarta", session_id=session.id, new_message=structured_message):
                    if event.content and event.content.parts:
                        for part in event.content.parts:
                            if part.text:
                                console.print(part.text, end="")
            console.print() # Print new line after response is complete
                                
        except (KeyboardInterrupt, EOFError):
            console.print("\n[bold yellow]Session terminated forcefully.[/bold yellow]")
            break

if __name__ == "__main__":
    if sys.platform == "win32":
        asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())
    asyncio.run(run_cli())