import asyncio
import json
from google.adk.agents import LlmAgent
from google.adk.models import Gemini
from google.adk.runners import InMemoryRunner

# 1. Define Local MCP Tool to read Vessel Bank simulation database
def read_branch_database() -> str:
    """Reads showroom sales data and NPL figures from local CSV file."""
    try:
        with open("Dealer_Sales_and_NPL.csv", "r") as file:
            return file.read()
    except FileNotFoundError:
        return "Error: Database file Dealer_Sales_and_NPL.csv not found."

# 2. Define Security Shield / Human Intervention Button (HITL)
def trigger_human_intervention(showroom: str, dana_usulan: int) -> bool:
    """
    [Security Pillar 5: High-Stakes Action HITL Lockout]
    Suspends automatic execution and requests physical confirmation from the Branch Manager.
    """
    print("\n" + "="*50)
    print(f"⚠️ SECURITY GUARD TRIGGERED: HIGH-STAKES ACTION DETECTED")
    print(f"Target Showroom: {showroom}")
    print(f"Proposed Subsidy Budget: IDR {dana_usulan:,}")
    print("="*50)
    
    # Simulates physical confirmation from user in terminal/UI
    approval = input("Do you approve this promotional budget? (Y/N): ")
    return approval.strip().upper() == "Y"

# 3. Initialize Core Brain AI Agent using Gemini
vessel_bank_agent = LlmAgent(
    name="Vessel_Bank_Branch_Growth_Agent",
    model=Gemini(model="gemini-flash-latest"),
    instruction=(
        "You are a Vessel Bank Branch Growth Strategy Agent. Your task is to assist the Branch Manager "
        "in analyzing sales declines based on CSV data provided by the tool. "
        "Follow the processing instructions and strict limitations specified in your SKILL.md file. "
        "If you want to recommend promotional funds, you MUST call the "
        "trigger_human_intervention tool to request approval first."
    ),
    tools=[read_branch_database, trigger_human_intervention]
)

# 4. Main function to run Vibe Coding simulation
async def main():
    runner = InMemoryRunner(agent=vessel_bank_agent, app_name="vessel_bank_strategy_app")
    
    # Natural language command (Vibe Coding prompt) from Branch Manager
    prompt_bm = "Analyze used car sales decline this month and provide promo recommendations"
    
    print(f"Branch Manager: '{prompt_bm}'\n")
    print("Executing AI Agent...")
    
    # Running agent session asynchronously
    async for event in runner.run_async(user_id="manager_vessel", new_message=prompt_bm):
        if event.content and event.content.parts:
            for part in event.content.parts:
                if part.text:
                    print(part.text, end="")

if __name__ == "__main__":
    asyncio.run(main())