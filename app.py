import streamlit as st
import pandas as pd
import csv
import json
import os
from datetime import datetime

# ----------------------------------------------------------------------
# PAGE SETUP & STYLING (VESSEL BANK ENTERPRISE STYLING)
# ----------------------------------------------------------------------
st.set_page_config(page_title="Vessel Bank AI Agent Governance Suite", page_icon="🏢", layout="wide")

# Custom CSS for gorgeous enterprise look & feel (Accents of Dark Blue, Gold, and clean slate cards)
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;600;700&display=swap');
    
    html, body, [class*="css"] {
        font-family: 'Inter', sans-serif;
    }
    
    .main-title {
        font-size: 2.3rem;
        font-weight: 700;
        background: linear-gradient(135deg, #0d47a1 0%, #1976d2 50%, #ffb300 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        margin-bottom: 0.2rem;
    }
    
    .subtitle {
        font-size: 1rem;
        color: #64748b;
        margin-bottom: 1.5rem;
    }
    
    /* Elegant card styling for Multi-Agent Committee simulation */
    .agent-card {
        background-color: #0f172a;
        border-radius: 12px;
        padding: 20px;
        margin-bottom: 15px;
        border-left: 6px solid #1e293b;
        box-shadow: 0 4px 6px -1px rgb(0 0 0 / 0.1), 0 2px 4px -2px rgb(0 0 0 / 0.1);
    }
    
    .vol-agent { border-left-color: #00d2ff; }
    .risk-agent { border-left-color: #ec4899; }
    .strat-agent { border-left-color: #eab308; }
    
    .agent-header {
        font-weight: 700;
        font-size: 1.1rem;
        margin-bottom: 3px;
    }
    .vol-header { color: #00d2ff; }
    .risk-header { color: #ec4899; }
    .strat-header { color: #eab308; }
    
    .agent-role {
        font-size: 0.75rem;
        color: #94a3b8;
        text-transform: uppercase;
        letter-spacing: 0.05em;
        margin-bottom: 10px;
        font-weight: 600;
    }
    
    .agent-msg {
        color: #f1f5f9;
        font-size: 0.95rem;
        line-height: 1.6;
    }
    
    /* Governance badges */
    .status-badge {
        padding: 12px 24px;
        border-radius: 8px;
        font-weight: 700;
        font-size: 1.25rem;
        text-align: center;
        margin-bottom: 15px;
        display: inline-block;
    }
    .status-waiting {
        background-color: #fef3c7;
        color: #b45309;
        border: 1.5px solid #f59e0b;
    }
    .status-approved {
        background-color: #d1fae5;
        color: #065f46;
        border: 1.5px solid #10b981;
    }
    .status-rejected {
        background-color: #fee2e2;
        color: #991b1b;
        border: 1.5px solid #ef4444;
    }
</style>
""", unsafe_allow_html=True)

st.markdown('<div class="main-title">🏢 Vessel Bank Branch Growth Strategy Governance Suite</div>', unsafe_allow_html=True)
st.markdown('<div class="subtitle">Multi-Agent Committee Network & Live Human-in-the-Loop Governance Dashboard</div>', unsafe_allow_html=True)

CSV_FILEPATH = "data_cabang_xyz.csv"
AUDIT_TRAIL_PATH = "audit_trail.json"

# ----------------------------------------------------------------------
# HELPER PARSING FUNCTIONS
# ----------------------------------------------------------------------
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

def load_csv_data(filepath=CSV_FILEPATH):
    if not os.path.exists(filepath):
        st.error(f"File '{filepath}' not found!")
        return [], [], []
        
    with open(filepath, "r", encoding="utf-8") as f:
        lines = f.readlines()
        
    # Parse branch macro data (line indexes 16-21)
    macro_data = []
    for idx in range(16, 22):
        row = [c.strip() for c in lines[idx].split(";")]
        if len(row) > 6:
            month = row[1]
            target = parse_indonesian_number(row[2])
            achv_pct = row[3]
            achv_rp = parse_indonesian_number(row[4])
            npl = parse_indonesian_percent(row[5]) if row[5] else 0.0
            staff = int(row[6]) if row[6].isdigit() else 0
            
            macro_data.append({
                "Month": month,
                "Branch Target": target,
                "Achv%": achv_pct,
                "Achv (in IDR)": achv_rp,
                "Branch NPL": npl,
                "Marketing Staff Count": staff
            })
            
    # Parse dealer contribution data (line indexes 24-29)
    dealer_names = ["Dealer A", "Dealer B", "Dealer C", "Dealer D", "Dealer E", "Dealer F", "Dealer G", "Dealer H"]
    dealer_data = []
    for idx in range(24, 30):
        row = [c.strip() for c in lines[idx].split(";")]
        if len(row) > 2:
            month = row[1]
            month_dealers = {"Month": month}
            for i, name in enumerate(dealer_names):
                s_idx = 2 + i * 3
                c_idx = 3 + i * 3
                n_idx = 4 + i * 3
                
                sales = int(row[s_idx]) if len(row) > s_idx and row[s_idx].isdigit() else 0
                contrib = int(row[c_idx]) if len(row) > c_idx and row[c_idx].isdigit() else 0
                npl_val = parse_indonesian_percent(row[n_idx]) if len(row) > n_idx and row[n_idx] else 0.0
                
                month_dealers[f"{name} Sales"] = sales
                month_dealers[f"{name} Contrib"] = contrib
                month_dealers[f"{name} NPL"] = npl_val
                
            dealer_data.append(month_dealers)
            
    return lines, macro_data, dealer_data

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
    
    # 3. Recalculate and update TOTAL row (line index 30)
    total_parts = lines[30].strip().split(';')
    month_lines = []
    for m_idx in range(24, 30):
        month_lines.append(lines[m_idx].strip().split(';'))
        
    for i, name in enumerate(dealer_names):
        s_idx = 2 + i * 3
        c_idx = 3 + i * 3
        n_idx = 4 + i * 3
        
        sum_sales = 0
        sum_contrib = 0
        for r in month_lines:
            sum_sales += int(r[s_idx].strip()) if (len(r) > s_idx and r[s_idx].strip().isdigit()) else 0
            sum_contrib += int(r[c_idx].strip()) if (len(r) > c_idx and r[c_idx].strip().isdigit()) else 0
            
        total_parts[s_idx] = str(sum_sales)
        total_parts[c_idx] = str(sum_contrib)
        total_parts[n_idx] = "" # NPL is left blank
        
    lines[30] = ";".join(total_parts) + "\n"
    
    # Overwrite the CSV
    with open(filepath, "w", encoding="utf-8") as f:
        f.writelines(lines)

# ----------------------------------------------------------------------
# GOVERNANCE HELPERS
# ----------------------------------------------------------------------
def get_report_status():
    if not os.path.exists("Laporan_Evaluasi_Operasional_Juni.md"):
        return "NO_REPORT"
    with open("Laporan_Evaluasi_Operasional_Juni.md", "r", encoding="utf-8") as f:
        content = f.read()
    if "[STATUS: WAITING HUMAN APPROVAL]" in content:
        return "WAITING"
    elif "[STATUS: APPROVED]" in content:
        return "APPROVED"
    elif "[STATUS: REJECTED]" in content:
        return "REJECTED"
    return "UNKNOWN"

def log_audit_trail(action):
    trail = []
    if os.path.exists(AUDIT_TRAIL_PATH):
        try:
            with open(AUDIT_TRAIL_PATH, "r", encoding="utf-8") as f:
                trail = json.load(f)
        except:
            trail = []
            
    entry = {
        "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "reviewer": "Branch Manager (Human-in-the-Loop)",
        "action": action,
        "status": f"APPROVED BY BRANCH MANAGER" if action == "APPROVED" else "REJECTED / VETOED BY BRANCH MANAGER",
        "file_audited": "Laporan_Evaluasi_Operasional_Juni.md"
    }
    trail.append(entry)
    with open(AUDIT_TRAIL_PATH, "w", encoding="utf-8") as f:
        json.dump(trail, f, indent=4)

# Load data initially
lines, macro_data, dealer_data = load_csv_data()

# Identify June data
june_macro = next((m for m in macro_data if m["Month"] == "Jun"), None)
june_dealer = next((d for d in dealer_data if d["Month"] == "JUN"), None)

# Initialize Session State
if "simulation_run" not in st.session_state:
    st.session_state["simulation_run"] = False

# Create Tabs
tab1, tab2, tab3 = st.tabs(["📊 Tab 1: Visual Database Editor (CRUD)", "🚀 Tab 2: Live Agent Network Simulator", "🛡️ Tab 3: Governance Guardrail"])

# ----------------------------------------------------------------------
# TAB 1: VISUAL DATABASE EDITOR (CRUD)
# ----------------------------------------------------------------------
with tab1:
    st.markdown("### 📁 Visual Database Editor (`data_cabang_xyz.csv`)")
    
    # Render historical macro performance table
    st.markdown("#### **A. Branch Macro Performance (Jan - Jun)**")
    df_macro_show = pd.DataFrame(macro_data)
    df_macro_show_fmt = df_macro_show.copy()
    df_macro_show_fmt["Branch Target"] = df_macro_show_fmt["Branch Target"].apply(lambda x: f"Rp {x:,}".replace(",", "."))
    df_macro_show_fmt["Achv (in IDR)"] = df_macro_show_fmt["Achv (in IDR)"].apply(lambda x: f"Rp {x:,}".replace(",", "."))
    df_macro_show_fmt["Branch NPL"] = df_macro_show_fmt["Branch NPL"].apply(lambda x: f"{x:.2f}%" if x > 0 else "")
    st.dataframe(df_macro_show_fmt, use_container_width=True)
    
    # Render dealer contribution table
    st.markdown("#### **B. Dealer / Showroom Performance (Jan - Jun)**")
    df_dealers_show = pd.DataFrame(dealer_data)
    df_dealers_show_fmt = df_dealers_show.copy()
    for col in df_dealers_show_fmt.columns:
        if col.endswith("NPL"):
            df_dealers_show_fmt[col] = df_dealers_show_fmt[col].apply(lambda x: f"{x:.2f}%" if x > 0 else "")
    st.dataframe(df_dealers_show_fmt, use_container_width=True)
    
    st.markdown("---")
    st.markdown("#### **📝 Edit Current Month Data (June)**")
    
    if june_macro and june_dealer:
        with st.form("edit_june_form"):
            col1, col2, col3, col4 = st.columns(4)
            with col1:
                target_input = st.number_input("Branch Target (IDR)", value=june_macro["Branch Target"], step=500000000)
            with col2:
                achv_rp_input = st.number_input("Achv (in IDR)", value=june_macro["Achv (in IDR)"], step=500000000)
            with col3:
                npl_cabang_input = st.number_input("Branch NPL (%)", value=june_macro["Branch NPL"], min_value=0.0, max_value=100.0, step=0.05, format="%.2f")
            with col4:
                staff_input = st.number_input("Marketing Staff Count", value=june_macro["Marketing Staff Count"], min_value=0, max_value=50, step=1)
                
            st.markdown("##### **Dealer Contribution & NPL Metrics**")
            edited_dealer_vals = {}
            dealer_names = ["Dealer A", "Dealer B", "Dealer C", "Dealer D", "Dealer E", "Dealer F", "Dealer G", "Dealer H"]
            
            # Row 1: Dealer A - D
            cols_r1 = st.columns(4)
            for idx, name in enumerate(dealer_names[:4]):
                with cols_r1[idx]:
                    st.markdown(f"**{name}**")
                    dsales = st.number_input("Total Sales", value=june_dealer[f"{name} Sales"], key=f"sales_{name}", min_value=0, step=1)
                    dcontrib = st.number_input("Contribution (Units)", value=june_dealer[f"{name} Contrib"], key=f"contrib_{name}", min_value=0, step=1)
                    dnpl = st.number_input("NPL (%)", value=june_dealer[f"{name} NPL"], key=f"npl_{name}", min_value=0.0, max_value=100.0, step=0.05, format="%.2f")
                    edited_dealer_vals[f"{name} Sales"] = dsales
                    edited_dealer_vals[f"{name} Contrib"] = dcontrib
                    edited_dealer_vals[f"{name} NPL"] = dnpl
                    
            # Row 2: Dealer E - H
            cols_r2 = st.columns(4)
            for idx, name in enumerate(dealer_names[4:]):
                with cols_r2[idx]:
                    st.markdown(f"**{name}**")
                    dsales = st.number_input("Total Sales", value=june_dealer[f"{name} Sales"], key=f"sales_{name}", min_value=0, step=1)
                    dcontrib = st.number_input("Contribution (Units)", value=june_dealer[f"{name} Contrib"], key=f"contrib_{name}", min_value=0, step=1)
                    dnpl = st.number_input("NPL (%)", value=june_dealer[f"{name} NPL"], key=f"npl_{name}", min_value=0.0, max_value=100.0, step=0.05, format="%.2f")
                    edited_dealer_vals[f"{name} Sales"] = dsales
                    edited_dealer_vals[f"{name} Contrib"] = dcontrib
                    edited_dealer_vals[f"{name} NPL"] = dnpl
            
            save_btn = st.form_submit_button("💾 Save Changes")
            if save_btn:
                new_macro_jun = {
                    "Branch Target": target_input,
                    "Achv (in IDR)": achv_rp_input,
                    "Branch NPL": npl_cabang_input,
                    "Marketing Staff Count": staff_input
                }
                save_csv_data(CSV_FILEPATH, lines, new_macro_jun, edited_dealer_vals)
                st.success("🎉 June data successfully saved and TOTAL recalculated!")
                st.rerun()
    else:
        st.warning("June data not found in database.")

# ----------------------------------------------------------------------
# TAB 2: LIVE AGENT NETWORK SIMULATOR
# ----------------------------------------------------------------------
with tab2:
    st.markdown("### 🚀 Live Agent Network Simulator")
    st.caption("Trigger the orchestration of 3 internal sub-agents to perform a tactical audit on the real-time database.")
    
    trigger_btn = st.button("🚀 Trigger Multi-Agent Committee", type="primary")
    
    if trigger_btn:
        with st.spinner("Activating Governance Agent Graph..."):
            # Load fresh data
            _, fresh_macro, fresh_dealers = load_csv_data()
            
            jun_m = next((m for m in fresh_macro if m["Month"] == "Jun"), None)
            may_m = next((m for m in fresh_macro if m["Month"] == "May"), None)
            
            jun_d = next((d for d in fresh_dealers if d["Month"] == "JUN"), None)
            
            dealer_names = ["Dealer A", "Dealer B", "Dealer C", "Dealer D", "Dealer E", "Dealer F", "Dealer G", "Dealer H"]
            june_dealers_list = []
            for name in dealer_names:
                june_dealers_list.append({
                    "name": name,
                    "sales": jun_d[f"{name} Sales"],
                    "contrib": jun_d[f"{name} Contrib"],
                    "npl": jun_d[f"{name} NPL"]
                })
            
            # 1. Volume Analyst Agent logic
            sorted_by_contrib = sorted(june_dealers_list, key=lambda x: x["contrib"], reverse=True)
            best_val = sorted_by_contrib[0]["contrib"]
            worst_val = sorted_by_contrib[-1]["contrib"]
            
            best_dealers = [d["name"] for d in june_dealers_list if d["contrib"] == best_val]
            worst_dealers = [d["name"] for d in june_dealers_list if d["contrib"] == worst_val]
            
            # 2. Risk Auditor Agent logic
            sorted_by_npl = sorted(june_dealers_list, key=lambda x: x["npl"], reverse=True)
            highest_npl_val = sorted_by_npl[0]["npl"]
            lowest_npl_val = sorted_by_npl[-1]["npl"]
            
            highest_npl_dealers = [d["name"] for d in june_dealers_list if d["npl"] == highest_npl_val]
            lowest_npl_dealers = [d["name"] for d in june_dealers_list if d["npl"] == lowest_npl_val]
            
            # 3. Branch Strategist Orchestrator logic
            jun_achv_str = jun_m["Achv%"]
            may_achv_str = may_m["Achv%"]
            jun_staff = jun_m["Marketing Staff Count"]
            needed_staff = max(0, 8 - jun_staff)
            
            st.session_state["simulation_run"] = True
            st.session_state["vol_report"] = {
                "best": f"{', '.join(best_dealers)} ({best_val} Units)",
                "worst": f"{', '.join(worst_dealers)} ({worst_val} Units each)",
                "dealers_best": best_dealers,
                "dealers_worst": worst_dealers,
                "worst_val": worst_val
            }
            
            st.session_state["risk_report"] = {
                "highest": f"{', '.join(highest_npl_dealers)} ({highest_npl_val:.2f}%)",
                "lowest": f"{', '.join(lowest_npl_dealers)} ({lowest_npl_val:.2f}%)",
                "dealers_highest": highest_npl_dealers,
                "dealers_lowest": lowest_npl_dealers,
                "highest_val": highest_npl_val,
                "lowest_val": lowest_npl_val
            }
            
            st.session_state["strat_report"] = {
                "decline_info": f"Branch target achievement dropped to 50% ({jun_achv_str}) consecutively in May ({may_achv_str}) and June ({jun_achv_str}). Operational audits prove this decline is fully correlated with the reduction of marketing staff from 8 people to {jun_staff} people.",
                "action": f"Propose a quota increase of {needed_staff} new marketing staff to headquarters to return operational capacity to full (8 people)."
            }
            
            # Save report file Laporan_Evaluasi_Operasional_Juni.md
            best_dealers_md = ", ".join([f"**{d}**" for d in best_dealers])
            worst_dealers_md = ", ".join([f"**{d}**" for d in worst_dealers[:-1]]) + (" and " if len(worst_dealers) > 1 else "") + f"**{worst_dealers[-1]}**"
            highest_npl_md = ", ".join([f"**{d}**" for d in highest_npl_dealers])
            lowest_npl_md = ", ".join([f"**{d}**" for d in lowest_npl_dealers])
            
            report_content = f"""# EVALUATION OF VESSEL BANK BRANCH OPERATIONAL PERFORMANCE
[STATUS: WAITING HUMAN APPROVAL]

This report was automatically compiled by the Vessel Bank Branch Governor Multi-Agent Network as a result of the June 2026 evaluation.

---

### **POINT A: Dealer Unit Contribution (June)**
* **Best Contributor Dealer:** {best_dealers_md} (Contribution: **{best_val} Units**)
  * *Action:* Recommended to provide an exclusive low-interest **loyalty program** to retain loyalty.
* **Worst Contributor Dealer:** {worst_dealers_md} (Contribution: **{worst_val} Units each**)
  * *Action:* Recommended to conduct a comprehensive **partnership review** to identify and resolve financing bottlenecks.

---

### **POINT B: Credit Risk / Non-Performing Loan (NPL) Analysis (June)**
* **Highest NPL Dealer:** {highest_npl_md} (NPL Percentage: **{highest_npl_val:.2f}%**)
  * *Action:* Recommended to **tighten survey criteria** in the region and increase the consumer **Minimum DP** limit.
* **Lowest NPL Dealer:** {lowest_npl_md} (NPL Percentage: **{lowest_npl_val:.2f}%**)
  * *Action:* Recommended to provide a reward facility in the form of **Fast-Track Approval**.

---

### **POINT C: Branch Productivity Improvement Strategy**
* **Performance Decline Analysis (May-June):**
  * Branch target achievement plummeted to **{jun_achv_str}** consecutively in May and June. Operational audits prove this decline is fully correlated with the **reduction of marketing staff from 8 people to {jun_staff} people**.
* **Action Strategy:**
  1. Propose a quota increase of **{needed_staff} new marketing staff** to headquarters to return operational capacity to full (8 people).
  2. Perform re-mapping of CMO working areas so potential dealers receive priority services.
  3. Conduct clinical coaching for CMOs handling the worst-performing dealers to assist market penetration.
"""
            with open("Laporan_Evaluasi_Operasional_Juni.md", "w", encoding="utf-8") as rf:
                rf.write(report_content)
                
            st.success("🎉 Multi-agent simulation completed! Report 'Laporan_Evaluasi_Operasional_Juni.md' successfully generated.")
            st.rerun()

    # Display dialogue if simulation has run
    if st.session_state["simulation_run"]:
        st.markdown("### 💬 Multi-Agent Interaction Log")
        
        # Volume Analyst Agent
        vol_data = st.session_state["vol_report"]
        st.markdown(f"""
        <div class="agent-card vol-agent">
            <div class="agent-header vol-header">@Volume-Analyst-Agent</div>
            <div class="agent-role">Branch Portfolio & Dealer Volume Auditor</div>
            <div class="agent-msg">
                <b>[June Dealer Contribution Audit]:</b><br>
                - Best Contributor: <b>{vol_data['best']}</b>.<br>
                - Worst Contributors: <b>{vol_data['worst']}</b>.<br><br>
                <b>[Recommended Action]:</b><br>
                - Provide loyalty program for the best contributor.<br>
                - Conduct partnership review for the worst contributors.<br>
                <i>Audit results sent directly to @Branch-Strategist-Orchestrator.</i>
            </div>
        </div>
        """, unsafe_allow_html=True)
        
        # Risk Auditor Agent
        risk_data = st.session_state["risk_report"]
        st.markdown(f"""
        <div class="agent-card risk-agent">
            <div class="agent-header risk-header">@Risk-Auditor-Agent</div>
            <div class="agent-role">Credit Quality & Non-Performing Loan (NPL) Guardrail</div>
            <div class="agent-msg">
                <b>[June Credit Quality Audit]:</b><br>
                - Dealer with Highest NPL: <b>{risk_data['highest']}</b>.<br>
                - Dealer with Lowest NPL: <b>{risk_data['lowest']}</b>.<br><br>
                <b>[Mitigation Recommendation]:</b><br>
                - Tighten consumer survey criteria / increase DP for the highest NPL dealer.<br>
                - Provide fast-track approval paths for the lowest NPL dealer.<br>
                <i>Risk analysis results sent directly to @Branch-Strategist-Orchestrator.</i>
            </div>
        </div>
        """, unsafe_allow_html=True)
        
        # Strategist Orchestrator Agent
        strat_data = st.session_state["strat_report"]
        st.markdown(f"""
        <div class="agent-card strat-agent">
            <div class="agent-header strat-header">@Branch-Strategist-Orchestrator</div>
            <div class="agent-role">Master Governance & Strategy Orchestrator</div>
            <div class="agent-msg">
                <b>[Consolidation of Vessel Bank Branch Strategic Report]:</b><br>
                - <i>Integration of Volume (Point A) and Credit Quality (Point B) data complete.</i><br>
                - <b>Macro Analysis of Performance Decline:</b> {strat_data['decline_info']}<br>
                - <b>Strategic Action Plan:</b> {strat_data['action']}<br><br>
                <b>[Governance Lock]:</b> Locking report draft to status <b>[WAITING HUMAN APPROVAL]</b>. Report is ready for review on Tab 3.
            </div>
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown("---")
        st.markdown("#### **📄 Generated Report Draft**")
        if os.path.exists("Laporan_Evaluasi_Operasional_Juni.md"):
            with open("Laporan_Evaluasi_Operasional_Juni.md", "r", encoding="utf-8") as f:
                st.code(f.read(), language="markdown")

# ----------------------------------------------------------------------
# TAB 3: HUMAN-IN-THE-LOOP GOVERNANCE GUARDRAIL
# ----------------------------------------------------------------------
with tab3:
    st.markdown("### 🛡️ Human-in-the-Loop Governance Guardrail")
    st.caption("Formal approval from the branch manager on the strategic recommendations formulated by the multi-agent committee.")
    
    status = get_report_status()
    
    if status == "NO_REPORT":
        st.info("💡 No report has been evaluated yet. Please run 'Trigger Multi-Agent Committee' in Tab 2 first.")
    else:
        # Display large status badge
        if status == "WAITING":
            st.markdown('<div class="status-badge status-waiting">⏳ STATUS: WAITING HUMAN APPROVAL</div>', unsafe_allow_html=True)
            st.warning("This report requires review and approval from the Branch Manager before finalization.")
        elif status == "APPROVED":
            st.markdown('<div class="status-badge status-approved">✅ STATUS: APPROVED BY BRANCH MANAGER</div>', unsafe_allow_html=True)
            st.success("The operational strategy report has been officially approved and recorded in the audit trail.")
        elif status == "REJECTED":
            st.markdown('<div class="status-badge status-rejected">❌ STATUS: REJECTED / VETOED BY BRANCH MANAGER</div>', unsafe_allow_html=True)
            st.error("The operational strategy report was rejected (vetoed) by the Branch Manager.")
            
        # Display the report content
        with st.expander("📄 Review Operational Evaluation Report Content", expanded=True):
            with open("Laporan_Evaluasi_Operasional_Juni.md", "r", encoding="utf-8") as f:
                st.markdown(f.read())
                
        # Approve/Reject Buttons (Only available if status is WAITING)
        if status == "WAITING":
            col1, col2 = st.columns(2)
            with col1:
                if st.button("✅ APPROVE STRATEGY", type="primary", use_container_width=True):
                    with open("Laporan_Evaluasi_Operasional_Juni.md", "r", encoding="utf-8") as f:
                        content = f.read()
                    content = content.replace("[STATUS: WAITING HUMAN APPROVAL]", "[STATUS: APPROVED]")
                    with open("Laporan_Evaluasi_Operasional_Juni.md", "w", encoding="utf-8") as f:
                        f.write(content)
                    log_audit_trail("APPROVED")
                    st.success("Report successfully approved!")
                    st.rerun()
            with col2:
                if st.button("❌ REJECT / VETO", use_container_width=True):
                    with open("Laporan_Evaluasi_Operasional_Juni.md", "r", encoding="utf-8") as f:
                        content = f.read()
                    content = content.replace("[STATUS: WAITING HUMAN APPROVAL]", "[STATUS: REJECTED]")
                    with open("Laporan_Evaluasi_Operasional_Juni.md", "w", encoding="utf-8") as f:
                        f.write(content)
                    log_audit_trail("REJECTED")
                    st.error("Report successfully rejected.")
                    st.rerun()
                    
    # Display Audit Trail logs
    st.markdown("---")
    st.markdown("#### **📋 Approval Audit Trail History (Governance Log)**")
    if os.path.exists(AUDIT_TRAIL_PATH):
        try:
            with open(AUDIT_TRAIL_PATH, "r", encoding="utf-8") as f:
                trail_data = json.load(f)
            st.dataframe(pd.DataFrame(trail_data), use_container_width=True)
        except:
            st.caption("No audit trail logs yet.")
    else:
        st.caption("No audit trail logs yet.")