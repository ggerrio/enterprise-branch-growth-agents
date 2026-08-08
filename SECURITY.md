# Security Policy

## Supported Versions

Only the latest release of this project is currently supported for security updates.

## Critical Assumptions
- **Zero Ambient Authority:** The multi-agent execution pipeline operates under strict zero ambient authority. The agents are blocked from autonomously executing transactions, database writes, or financial operations.
- **No Live Credentials:** No live production credentials or API keys are stored in this repository. All interactions with the Google ADK and LLM services are conducted via standard local environment variables (`GEMINI_API_KEY`) and are subjected to client-side verification.

## Dataset Sanitization
- All data contained in `data_cabang_xyz.csv` and `Dealer_Sales_and_NPL.csv` is synthetic and randomized.
- Showroom names (Dealer A–H) and CMO handler names (e.g., Budi Santoso, Siti Aminah) have been completely anonymized and sanitized. No real customer or corporate transaction history is present.

## Reporting a Vulnerability

If you discover a potential security vulnerability in this project, please open an issue in the GitHub repository or contact the project owners directly. We aim to address all verified security concerns within 48 hours.
