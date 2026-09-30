from .client import GeminiService
from ..config import get_settings

SYSTEM = """You are FitBuddy's nutrition and recovery tip assistant. Give one concise, practical general-wellness tip. Do not prescribe restrictive diets, supplements, fasting, dehydration, or medical treatment. For users under 18, avoid calorie or weight-loss prescriptions and emphasize balanced meals, hydration, sleep, and support from a parent/guardian or qualified professional when needed."""


def demo_tip(goal: str) -> str:
    tips = {
        "muscle gain": "Include a balanced protein source in regular meals and pair it with carbohydrates, fruits/vegetables, and enough fluids.",
        "weight loss": "Build meals around a variety of vegetables or fruit, whole grains, and protein-rich foods; avoid extreme restriction and keep hydration consistent.",
        "general wellness": "Aim for regular balanced meals, enough fluids, and a consistent sleep routine to support energy and recovery.",
        "flexibility": "Hydrate normally and include a variety of nutrient-rich foods while giving your body enough recovery time.",
        "endurance": "Pair regular carbohydrate-rich foods with protein and fluids so you have energy for activity and recovery.",
    }
    return tips.get(goal, tips["general wellness"])


def generate_nutrition_tip_with_flash(goal: str, age: int) -> str:
    settings = get_settings()
    service = GeminiService()
    if not service.enabled:
        if settings.demo_mode:
            return demo_tip(goal)
        raise RuntimeError("GEMINI_API_KEY is required when DEMO_MODE=false.")
    prompt = f"Give one concise nutrition or recovery tip for a person age {age} whose fitness goal is {goal}. Keep it practical and general."
    return service.generate(model=settings.gemini_tip_model, prompt=prompt, system_instruction=SYSTEM, temperature=0.5)
