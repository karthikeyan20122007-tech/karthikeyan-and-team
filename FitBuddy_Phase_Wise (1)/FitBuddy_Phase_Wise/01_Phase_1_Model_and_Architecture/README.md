# FitBuddy – AI Fitness Plan Generator

FitBuddy is a FastAPI + Jinja2 + SQLite application based on the supplied project documentation. It generates a seven-day general fitness plan, a nutrition/recovery tip, and a feedback-based revised plan.

## Architecture

- **Frontend:** Jinja2 HTML templates + responsive CSS
- **Backend:** FastAPI + Uvicorn
- **AI:** Google GenAI SDK (`google-genai`)
- **Workout/feedback:** configurable Gemini Pro-class model (`GEMINI_WORKOUT_MODEL`)
- **Nutrition/recovery:** configurable Gemini Flash model (`GEMINI_TIP_MODEL`)
- **Database:** SQLAlchemy + SQLite
- **Testing:** Pytest + FastAPI TestClient

The original document names Gemini 1.5 Pro and Gemini Flash. Those model names are legacy in the current Gemini API, so this implementation makes the model IDs configurable in `.env`. The defaults are current model IDs documented by Google at project creation time.

## Folder structure

```text
FitBuddy/
├── app/
│   ├── __init__.py
│   ├── main.py
│   ├── config.py
│   ├── database.py
│   ├── models.py
│   ├── schemas.py
│   ├── services.py
│   ├── routes.py
│   └── ai/
│       ├── __init__.py
│       ├── client.py
│       ├── gemini_generator.py
│       ├── gemini_flash_generator.py
│       └── updated_plan.py
├── templates/
│   ├── base.html
│   ├── index.html
│   ├── result.html
│   ├── all_users.html
│   └── error.html
├── static/css/style.css
├── tests/test_app.py
├── .env.example
├── .gitignore
├── requirements.txt
└── README.md
```

## VS Code setup – Windows

1. Install Python 3.11+ and VS Code.
2. Open the `FitBuddy` folder in VS Code.
3. Open **Terminal → New Terminal**.
4. Create a virtual environment:

```powershell
python -m venv .venv
```

5. Activate it:

```powershell
.venv\Scripts\Activate.ps1
```

If PowerShell blocks activation, use Command Prompt:

```cmd
.venv\Scripts\activate
```

6. Install dependencies:

```powershell
python -m pip install --upgrade pip
pip install -r requirements.txt
```

7. Create `.env` from `.env.example`:

```powershell
Copy-Item .env.example .env
```

8. For real Gemini generation, put your Gemini API key into `.env`:

```text
GEMINI_API_KEY=your_key_here
DEMO_MODE=false
```

If you do not have a key yet, leave `DEMO_MODE=true`. The app will still run locally with deterministic demo content so that the frontend, routes, database, and feedback workflow can be tested.

## Run

```powershell
uvicorn app.main:app --reload
```

Open:

- http://127.0.0.1:8000 — application
- http://127.0.0.1:8000/docs — FastAPI API documentation
- http://127.0.0.1:8000/api/health — health check
- http://127.0.0.1:8000/view-all-users — admin dashboard

## Test

With the virtual environment active:

```powershell
pytest -q
```

The tests use demo mode, so they do not need a Gemini API key.

## Main application flow

1. `/` displays the input form.
2. `/generate-workout` validates the form, saves the user, generates a workout and nutrition/recovery tip, and stores the plan.
3. `/submit-feedback` loads the latest plan, sends the plan + feedback to the workout model, and stores the revised plan.
4. `/view-all-users` displays stored users and their original/updated plans.
5. `/api/health` provides a simple operational check.

## Configuration

`GEMINI_WORKOUT_MODEL` and `GEMINI_TIP_MODEL` are intentionally configurable because Gemini model availability can vary by account/project. The code uses Google's current `google-genai` SDK rather than the older `google-generativeai` package.

## Notes for a real deployment

This is a complete local/project demonstration. Before production deployment, add real authentication/authorization for the admin dashboard, HTTPS, stronger privacy controls, database migrations, structured logging, rate limiting, secret management, and a production database. Do not expose the admin page publicly without authentication.
