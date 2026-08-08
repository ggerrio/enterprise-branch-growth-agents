# Safety Guards & Human-in-the-Loop (HITL) Policies

This document establishes the strict operational boundaries and governance protocols for all autonomous agents executing within the Vessel Bank Branch Governor Network.

## 1. High-Stakes Action Definition
A recommendation is marked as **High-Stakes** if it involves:
- **Financial Allocations:** Proposing commission subsidy budgets or promotional funds for showrooms.
- **Quota Adjustments:** Proposing modifications to Booking Volume targets or marketing staff counts.

## 2. Intercept & Triage Protocol (Zero Ambient Authority)
- **Direct Update Lockout:** Agents are strictly prohibited from writing directly to operational databases or dispatching external notifications autonomously.
- **State Suspension:** When a high-stakes action is detected, the agent must immediately freeze its state and trigger the `trigger_human_intervention()` function.

## 3. Human-in-the-Loop Gateway
Every strategic draft must be explicitly signed off by the human Branch Manager:
- **Pending Status:** The generated report is locked under `[STATUS: WAITING HUMAN APPROVAL]`.
- **UI Approval Check:** The Manager must manually review and select **Approve** or **Reject** on the dashboard.
- **Audit Logs:** Every action is timestamped and recorded in the immutable `audit_trail.json` file.
- **Post-Approval Action:** Automated dispatch scripts (e.g., CMO notifications) run *only* after explicit approval.