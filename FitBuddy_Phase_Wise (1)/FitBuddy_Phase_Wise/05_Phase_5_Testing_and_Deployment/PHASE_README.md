# Phase 5 – Testing & Deployment

Purpose: Install dependencies, configure environment variables, run the server, and verify the application.

Files included:
- tests/test_app.py – automated tests
- .env.example – environment template
- requirements.txt – dependencies
- run.bat – Windows helper
- run.sh – Linux/macOS helper
- README.md – complete setup instructions

Main commands:
python -m venv .venv
.venv\\Scripts\\activate
pip install -r requirements.txt
uvicorn app.main:app --reload

Documentation alignment:
- Milestone 5.1 – local deployment preparation
- Milestone 5.2 – testing and verification
