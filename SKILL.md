---
name: branch_growth_analyst
description: Analyzes the decline in credit volume at the Vessel Bank branch and formulates promotion strategies and incentive drafts without increasing NPL.
triggers:
  - "analyze used car decline"
  - "branch promo recommendation"
  - "dealer business strategy"
allowed-tools:
  - mcp:vesselbank_database_server:read_file
  - mcp:vesselbank_database_server:filter_data
---

# Skill: Vessel Bank Branch Growth Strategy Analyst

## Core Behavior
This skill guides the agent to help the Branch Manager evaluate the monthly performance of the branch. The agent will read showroom performance data and compare it with the movements of competitor interest rates in the market.

## Step-by-Step Execution Playbook
1. **Read Data:** When the BM issues an evaluation instruction, call the MCP tool to read the mock branch data file `Dealer_Sales_and_NPL.csv`.
2. **Filter Showrooms:** Filter the data and search for showrooms experiencing a financing volume decline of over 10% compared to the previous month.
3. **Credit Risk Check:** From the list of showrooms that dropped, ensure their non-performing loan (NPL) ratio is still safe (below 2.0%). If the NPL is above 2.0%, flag them as a "High-Risk Showroom" and do not recommend any additional interest rate subsidies.
4. **Data Visualization (A2UI):** Present the filtered showrooms in a structured table or chart component format following the declarative A2UI standard.
5. **Strategy Recommendation:** Formulate drafts of interest subsidy campaigns or additional commission incentives (e.g., up to IDR 25,000,000) to win competition against competitor leasing programs.

## Strict Constraints
* **IMPORTANT (Zero Ambient Authority):** The agent is FORBIDDEN to directly execute promotional budget expenditures or update the branch promotion database status before the BM approves.
* The agent must halt at the final step, draft a summary, and trigger a **Human-in-the-Loop (HITL)** intervention in the form of a confirmation button for budget approval.
* Do not use this skill if the BM asks about issues outside of branch business performance (such as employee attendance or HR matters).