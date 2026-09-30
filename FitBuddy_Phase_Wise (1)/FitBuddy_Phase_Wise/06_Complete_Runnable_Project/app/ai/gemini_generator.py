from .client import GeminiService
from ..config import get_settings

SYSTEM = """You are FitBuddy, a cautious fitness-planning assistant. Create general wellness guidance, not medical diagnosis or treatment. Never recommend dangerous challenges, extreme dieting, dehydration, unsafe supplements, or exercise through pain. Prefer gradual progression, rest, warm-ups, cool-downs, and technique. For users under 18, keep guidance age-appropriate and emphasize adult/qualified-coach supervision rather than calorie restriction or body-composition targets. Return a clear seven-day plan with warm-up, main workout, sets/reps or duration, rest, and cooldown/recovery."""


def demo_plan(name: str, goal: str, intensity: str) -> str:
    return f"""FitBuddy demo plan for {name}\nGoal: {goal}\nIntensity: {intensity}\n\nDay 1 – Full Body\nWarm-up: 5–10 minutes of easy movement.\nMain: Squats 3x8–12; incline push-ups 3x8–12; glute bridges 3x10–15; easy plank 3x20–30 sec. Rest 60–90 sec.\nCooldown: 5 minutes easy walking and gentle stretching.\n\nDay 2 – Cardio + Mobility\nWarm-up: 5 minutes.\nMain: 20–30 minutes comfortable-to-moderate cardio; mobility for hips, shoulders and ankles.\nCooldown: 5 minutes easy movement.\n\nDay 3 – Upper Body + Core\nWarm-up: 5–10 minutes.\nMain: Rows 3x8–12; wall/incline push-ups 3x8–12; bird-dog 3x8 each side; dead bug 3x8 each side.\nCooldown: Gentle stretching.\n\nDay 4 – Recovery\n20–30 minutes easy walking plus gentle mobility. Keep effort comfortable.\n\nDay 5 – Lower Body\nWarm-up: 5–10 minutes.\nMain: Squats 3x8–12; step-ups 3x8 each side; glute bridges 3x10–15; calf raises 3x12–15.\nCooldown: 5 minutes easy movement.\n\nDay 6 – Cardio + Full Body\nWarm-up: 5–10 minutes.\nMain: 20–30 minutes moderate cardio followed by 2 easy rounds of bodyweight squats, rows/band pulls, and incline push-ups.\nCooldown: Easy walking and stretching.\n\nDay 7 – Rest / Light Activity\nChoose rest or a relaxed walk and gentle mobility.\n\nNote: This demo is intentionally general. Stop if you feel pain, dizziness, or unusual symptoms and seek appropriate adult/professional guidance."""


def generate_workout_gemini(name: str, age: int, weight: float, goal: str, intensity: str) -> str:
    settings = get_settings()
    service = GeminiService()
    if not service.enabled:
        if settings.demo_mode:
            return demo_plan(name, goal, intensity)
        raise RuntimeError("GEMINI_API_KEY is required when DEMO_MODE=false.")

    prompt = f"""Create a personalized seven-day general fitness plan for:\nName: {name}\nAge: {age}\nWeight: {weight} kg\nGoal: {goal}\nPreferred intensity: {intensity}\n\nUse the exact seven day headings. Include warm-up, main workout, sets/reps or duration, rest guidance, and cooldown/recovery for each day. Include at least one recovery/rest day. Do not prescribe medical treatment, medication, supplements, extreme calorie restriction, dehydration, or exercise through pain. Do not infer medical conditions from the inputs."""
    return service.generate(model=settings.gemini_workout_model, prompt=prompt, system_instruction=SYSTEM)
