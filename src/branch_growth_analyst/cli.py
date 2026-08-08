import asyncio
import sys

def run_simulation_cli():
    """CLI command to run the multi-agent committee simulation."""
    from . import simulate_committee
    if sys.platform == "win32":
        asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())
    asyncio.run(simulate_committee.run_simulation())

def run_evaluation_cli():
    """CLI command to run the June operational performance evaluation report generator."""
    from . import run_june_evaluation
    if sys.platform == "win32":
        asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())
    asyncio.run(run_june_evaluation.run_evaluation())

def run_governance_cli():
    """CLI command to run the interactive multi-agent governance suite."""
    from . import enterprise_governance_suite
    if sys.platform == "win32":
        asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())
    asyncio.run(enterprise_governance_suite.run_multi_agent_suite())
