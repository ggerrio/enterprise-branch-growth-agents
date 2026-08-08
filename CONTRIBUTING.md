# Contributing Guidelines

We welcome contributions to the **Vessel Bank - Enterprise Multi-Agent Growth Strategy Suite**! Please follow these guidelines to set up your local development workspace and submit contributions.

## Development Setup

1. **Clone the repository:**
   ```bash
   git clone https://github.com/ggerrio/enterprise-branch-growth-agents.git
   cd enterprise-branch-growth-agents
   ```

2. **Initialize python virtual environment:**
   ```bash
   python -m venv .venv
   source .venv/bin/activate # Windows: .venv\Scripts\activate.ps1
   ```

3. **Install the package in editable mode with development dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

## Development Guidelines

- ** DRY Code:** Reusable parser and formatter code should reside in the package package `src/branch_growth_analyst/data_parser.py` instead of script copy-pastes.
- **Testing:** Always add corresponding tests for any parsing or utility changes in the `tests/` directory.
- **Running Tests:**
  ```bash
  pytest
  ```
- **Linting:** Ensure code is formatted correctly and has no undefined imports:
  ```bash
  flake8 . --count --select=E9,F63,F7,F82 --show-source --statistics
  ```

## Making Changes
- Create a feature branch for your edits.
- Commit your changes with descriptive messages.
- Ensure the Streamlit dashboard (`streamlit run app.py`) and all tests pass before making a pull request.
