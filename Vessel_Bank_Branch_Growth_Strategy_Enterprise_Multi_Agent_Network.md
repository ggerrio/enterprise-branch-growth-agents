# Vessel Bank Branch Growth Strategy — Enterprise Multi-Agent Network

This notebook documents the complete Multi-Agent Network architecture for the **Vessel Bank Branch Growth Strategy**. It outlines the core business challenges of used car finance, explains the cooperating multi-agent structure built with **Google ADK**, details the repository blueprint, and showcases the source code components including the Model Context Protocol (MCP) server, CLI simulator, and Streamlit Dashboard.

---

## 1. Executive Summary & Business Problem

Vessel Bank operates a network of regional branches focused on used car financing. Financing profitability depends heavily on managing two competing forces: **growth volume** and **credit risk (NPL)**.

### Core Challenges:
1. **Volume Decline vs. Competitor Rate Wars:** Competitors frequently launch interest rate and commission wars (e.g., cutting rates by 1.5% in major areas). Showrooms will divert bookings to competitors if Vessel Bank does not respond with tactical commission or interest subsidies.
2. **Credit Risk & NPL Guardrails:** Subsidizing high-volume but high-risk showrooms leads to loan default spikes. The bank enforces a strict NPL limit of **2.0%** per dealer; any dealer exceeding this threshold is blocked from tactical funding.
3. **Operational Capacity Constraints:** Sales achievements are directly linked to the headcount of Customer Relations Officers (CMOs). A sudden drop in CMO staff (e.g., from 8 to 6) leads to a proportional drop in target achievement (plummeting to 50%).

### The Solution: Multi-Agent Orchestration with HITL
This project introduces a **Multi-Agent Committee Graph** that divides responsibilities among specialized agents, integrates database editing, and enforces a strict **Human-in-the-Loop (HITL)** governance gate. No LLM or strategy is finalized without explicit manager approval.

---

## 2. System Flow & Architecture

The collaboration is structured as an acyclic graph where analytical feeds converge on an orchestrator. Below is the system flow diagram:

```mermaid
graph TD
    CSV[(data_cabang_xyz.csv)] -->|June Dealer Data| VolAgent[@Volume-Analyst-Agent]
    CSV -->|June NPL Data| RiskAgent[@Risk-Auditor-Agent]
    CSV -->|May-June Macro Metrics| StratAgent[@Branch-Strategist-Orchestrator]
    
    VolAgent -->|Poin A: Best/Worst Volume & Actions| StratAgent
    RiskAgent -->|Poin B: Highest/Lowest NPL & Actions| StratAgent
    
    StratAgent -->|Poin C: CMO Staff Correlation & Plan| ReportDraft[Report Draft: WAITING HUMAN APPROVAL]
    
    ReportDraft -->|Streamlit Dashboard / Tab 3| HITL{Human Branch Manager}
    
    HITL -->|Approve Strategy| Approved[Status: APPROVED / Write to audit_trail.json]
    HITL -->|Reject Strategy| Rejected[Status: REJECTED / Stop Campaign]
```

### The Multi-Agent Roles:
* **@Volume-Analyst-Agent:** Focuses strictly on dealer contribution counts. It identifies top performers (rewarding them with loyalty programs) and bottom performers (recommending partnership reviews).
* **@Risk-Auditor-Agent:** Focuses strictly on credit quality and NPL ratios. It identifies the lowest NPL dealer (rewarding them with fast-track approvals) and the highest NPL dealer (tightening survey criteria and increasing minimum DP).
* **@Branch-Strategist-Orchestrator:** Performs macro analysis correlating staff reductions to target misses, integrates findings from the volume and risk agents, and drafts the evaluation report under a locked status.

---

## 3. Project Blueprint & Repository Layout

The project layout integrates source codes, agent rules, workflows, and specifications:

```
branch_growth_analyst/
├── app.py                     # Streamlit Dashboard (CRUD, Simulator, HITL Governance)
├── data_cabang_xyz.csv        # Semicolon-separated CSV database (Jan-Jun)
├── Dealer_Sales_and_NPL.csv   # Local MCP database (Showrooms & NPL)
├── simulate_committee.py      # CLI Multi-Agent Committee Simulator
├── run_june_evaluation.py     # CLI June Evaluation Runner
├── data_parser.py             # CSV Parser library
├── mcp_server.py              # Vessel Bank Data Server (MCP Mock)
├── enterprise_governance_suite.py # Enterprise CLI debate network
├── main.py                    # Vibe-coding entry point
├── single_analyst_agent.py    # Single agent prototype script
├── branch_strategy_spec.feature # Spec-Driven Gherkin features
├── SKILL.md                   # Skill instructions for AI agent
├── audit_trail.json           # Decision logs (Governance log)
├── Laporan_Evaluasi_Operasional_Juni.md # Generated strategy report (final outcome)
├── Laporan_Strategi_Bulan_Juni.md       # Strategic decision history report
└── .agents/
    └── workflows/             # Agent Workflow Configurations (English)
        ├── 1volumeanalyst.md
        ├── 2riskauditor.md
        └── 3branchorchestrator.md
```

---

## 4. Key Source Code Implementations

### 4.1. CSV Database Design (`data_cabang_xyz.csv`)
The database contains two distinct sections separated by empty semicolon lines:
* **Macro Performance Table:** Monthly targets, achievements, NPL, and CMO headcount.
* **Dealer Performance Table:** Sales, contribution, and NPL per showroom.

```csv
;Month;Branch Target;Achv%;Achv (in IDR);Branch NPL;Marketing Staff Count
;Jan;10.000.000.000;80%;8.000.000.000;;8
;Jun;14.000.000.000;50%;7.000.000.000;0,65%;7
;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;
;MONTH;TOTAL SALES DEALER A;CONTRIBUTION DEALER A;NPL DEALER A;TOTAL SALES DEALER B;CONTRIBUTION DEALER B;NPL DEALER B;...
;JUN;160;28;0,42%;175;15;0,26%;130;5;1,07%;40;4;0,74%;14;1;1,04%;12;2;0,28%;10;1;0,22%;7;1;0,89%
;TOTAL;800;203;;1125;85;;730;53;;335;64;;138;27;;94;20;;95;11;;59;5
```

### 4.2. Streamlit Dashboard App (`app.py`)
The Streamlit application is structured modularly with custom enterprise HSL styling and three tabs for complete CRUD operations, simulation runs, and HITL governance.

```python
# Helper serialization functions in app.py
def parse_indonesian_number(val_str):
    if not val_str:
        return 0
    cleaned = val_str.replace(".", "").strip()
    return int(cleaned) if cleaned.isdigit() else 0

def format_indonesian_number(val_int):
    return f"{val_int:,}".replace(",", ".")

def parse_indonesian_percent(val_str):
    if not val_str:
        return 0.0
    cleaned = val_str.replace("%", "").replace(",", ".").strip()
    try:
        return float(cleaned)
    except ValueError:
        return 0.0

def format_indonesian_percent(val_float):
    if val_float == int(val_float):
        return f"{int(val_float)}%"
    formatted = f"{val_float:.2f}".replace(".", ",")
    return f"{formatted}%"
```

### 4.3. Data Load & Write Cycles (`app.py`)
Updates in the editor form automatically write back to the CSV while recalculating the sums in the `TOTAL` row.

```python
def save_csv_data(filepath, lines, edited_macro_jun, edited_dealer_jun):
    # 1. Update June macro data (line index 21)
    macro_parts = lines[21].strip().split(';')
    target = edited_macro_jun["Branch Target"]
    achv_rp = edited_macro_jun["Achv (in IDR)"]
    staf = edited_macro_jun["Marketing Staff Count"]
    npl_cab = edited_macro_jun["Branch NPL"]
    achv_pct = int((achv_rp / target) * 100) if target > 0 else 0
    
    macro_parts[2] = format_indonesian_number(target)
    macro_parts[3] = f"{achv_pct}%"
    macro_parts[4] = format_indonesian_number(achv_rp)
    macro_parts[5] = format_indonesian_percent(npl_cab)
    macro_parts[6] = str(staf)
    lines[21] = ";".join(macro_parts) + "\n"
    
    # 2. Update June dealer data (line index 29)
    dealer_parts = lines[29].strip().split(';')
    dealer_names = ["Dealer A", "Dealer B", "Dealer C", "Dealer D", "Dealer E", "Dealer F", "Dealer G", "Dealer H"]
    for i, name in enumerate(dealer_names):
        s_idx = 2 + i * 3
        c_idx = 3 + i * 3
        n_idx = 4 + i * 3
        dealer_parts[s_idx] = str(edited_dealer_jun[f"{name} Sales"])
        dealer_parts[c_idx] = str(edited_dealer_jun[f"{name} Contrib"])
        dealer_parts[n_idx] = format_indonesian_percent(edited_dealer_jun[f"{name} NPL"])
    lines[29] = ";".join(dealer_parts) + "\n"
    
    # 3. Recalculate TOTAL row (line index 30)
    total_parts = lines[30].strip().split(';')
    month_lines = [lines[m_idx].strip().split(';') for m_idx in range(24, 30)]
    for i, name in enumerate(dealer_names):
        s_idx = 2 + i * 3
        c_idx = 3 + i * 3
        n_idx = 4 + i * 3
        sum_sales = sum(int(r[s_idx].strip()) for r in month_lines if len(r) > s_idx and r[s_idx].strip().isdigit())
        sum_contrib = sum(int(r[c_idx].strip()) for r in month_lines if len(r) > c_idx and r[c_idx].strip().isdigit())
        total_parts[s_idx] = str(sum_sales)
        total_parts[c_idx] = str(sum_contrib)
        total_parts[n_idx] = ""
    lines[30] = ";".join(total_parts) + "\n"
    
    with open(filepath, "w", encoding="utf-8") as f:
        f.writelines(lines)
```

---

## 5. Observability & Human-in-the-Loop Governance

High-stakes strategies must not be autonomously deployed. The network enforces a locked state:
* **WAITING:** The report generated by `@Branch-Strategist-Orchestrator` starts with `[STATUS: WAITING HUMAN APPROVAL]`.
* **APPROVAL ACTION:** Clicking **✅ APPROVE STRATEGY** updates the file content to `[STATUS: APPROVED]` and logs details to `audit_trail.json`.
* **REJECTION/VETO ACTION:** Clicking **❌ REJECT / VETO** changes the file status to `[STATUS: REJECTED]` and blocks implementation logs.

### Example log in `audit_trail.json`:
```json
[
    {
        "timestamp": "2026-06-25 15:07:30",
        "reviewer": "Branch Manager (Human-in-the-Loop)",
        "action": "APPROVED",
        "status": "APPROVED BY BRANCH MANAGER",
        "file_audited": "Laporan_Evaluasi_Operasional_Juni.md"
    }
]
```

---

## 6. How to Run the Project

1. **Prerequisites:** Ensure Python 3.10+ and the required packages (`streamlit`, `pandas`, `rich`, `google-adk`) are installed in your environment.
2. **Starting the Web Interface:**
   ```powershell
   .venv\Scripts\streamlit.exe run app.py
   ```
3. **Starting the CLI Simulator:**
   ```powershell
   .venv\Scripts\python.exe simulate_committee.py
   ```
