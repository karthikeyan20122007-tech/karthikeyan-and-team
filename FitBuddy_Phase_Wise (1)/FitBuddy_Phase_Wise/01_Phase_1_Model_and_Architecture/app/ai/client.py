from google import genai
from google.genai import types
from ..config import get_settings


class GeminiService:
    def __init__(self) -> None:
        settings = get_settings()
        self.settings = settings
        self.client = genai.Client(api_key=settings.gemini_api_key) if settings.gemini_api_key else None

    @property
    def enabled(self) -> bool:
        return self.client is not None

    def generate(self, *, model: str, prompt: str, system_instruction: str, temperature: float = 0.4) -> str:
        if not self.client:
            raise RuntimeError("Gemini API key is not configured.")
        response = self.client.models.generate_content(
            model=model,
            contents=prompt,
            config=types.GenerateContentConfig(
                system_instruction=system_instruction,
                temperature=temperature,
                max_output_tokens=5000,
            ),
        )
        text = (response.text or "").strip()
        if not text:
            raise RuntimeError("Gemini returned an empty response.")
        return text
