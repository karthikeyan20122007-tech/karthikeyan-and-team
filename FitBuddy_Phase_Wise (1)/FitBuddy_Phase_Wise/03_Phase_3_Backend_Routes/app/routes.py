from fastapi import APIRouter, Depends, Form, HTTPException, Request
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session
from .ai.gemini_flash_generator import generate_nutrition_tip_with_flash
from .ai.gemini_generator import generate_workout_gemini
from .ai.updated_plan import update_workout_plan
from .config import get_settings
from .database import get_db
from .schemas import FeedbackRequest, UserInput
from .services import delete_user, get_all_users, get_latest_plan, get_user, save_plan, save_user, update_plan

router = APIRouter()
templates = Jinja2Templates(directory="templates")


def render(request: Request, template: str, **context):
    context["request"] = request
    return templates.TemplateResponse(request=request, name=template, context=context)


@router.get("/", response_class=HTMLResponse)
def home(request: Request):
    return render(request, "index.html", settings=get_settings())


@router.post("/generate-workout", response_class=HTMLResponse)
def generate_workout(
    request: Request,
    name: str = Form(...), user_id: str = Form(...), age: int = Form(...), weight: float = Form(...),
    goal: str = Form(...), intensity: str = Form(...), db: Session = Depends(get_db),
):
    try:
        data = UserInput(name=name, user_id=user_id, age=age, weight=weight, goal=goal, intensity=intensity)
        user = save_user(db, data)
        workout = generate_workout_gemini(data.name, data.age, data.weight, data.goal, data.intensity)
        tip = generate_nutrition_tip_with_flash(data.goal, data.age)
        plan = save_plan(db, user.user_id, workout, tip)
        return render(request, "result.html", user=user, plan=plan, mode="generated", error=None)
    except Exception as exc:
        return render(request, "error.html", message=str(exc))


@router.post("/submit-feedback", response_class=HTMLResponse)
def submit_feedback(request: Request, user_id: str = Form(...), feedback: str = Form(...), db: Session = Depends(get_db)):
    try:
        data = FeedbackRequest(user_id=user_id, feedback=feedback)
        user = get_user(db, data.user_id)
        plan = get_latest_plan(db, data.user_id)
        if not user or not plan:
            raise HTTPException(status_code=404, detail="User or workout plan not found.")
        revised = update_workout_plan(user.name, user.age, user.goal, user.intensity, plan.updated_plan or plan.original_plan, data.feedback)
        update_plan(db, plan, revised, data.feedback)
        return render(request, "result.html", user=user, plan=plan, mode="updated", error=None)
    except HTTPException as exc:
        return render(request, "error.html", message=exc.detail)
    except Exception as exc:
        return render(request, "error.html", message=str(exc))


@router.get("/view-all-users", response_class=HTMLResponse)
def view_all_users(request: Request, token: str | None = None, db: Session = Depends(get_db)):
    settings = get_settings()
    if settings.admin_token and token != settings.admin_token:
        return render(request, "error.html", message="Admin access denied. Provide the configured admin token.")
    users = get_all_users(db)
    return render(request, "all_users.html", users=users)


@router.post("/delete-user")
def remove_user(user_id: str = Form(...), token: str | None = Form(None), db: Session = Depends(get_db)):
    settings = get_settings()
    if settings.admin_token and token != settings.admin_token:
        raise HTTPException(status_code=403, detail="Admin access denied")
    delete_user(db, user_id)
    return RedirectResponse(url="/view-all-users" + (f"?token={token}" if token else ""), status_code=303)


@router.get("/api/health")
def health():
    settings = get_settings()
    return {"status": "ok", "app": settings.app_name, "gemini_configured": bool(settings.gemini_api_key), "demo_mode": settings.demo_mode}


@router.get("/api/users")
def api_users(db: Session = Depends(get_db)):
    users = get_all_users(db)
    return [{"user_id": u.user_id, "name": u.name, "age": u.age, "weight": u.weight, "goal": u.goal, "intensity": u.intensity} for u in users]
