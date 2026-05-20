import asyncio
import json
import re

from google import genai
from google.genai import types

from app.core.config import settings
from app.schemas.report import PersonalityReport
from app.services.prompt_builder import PromptBuilder


class ReportGenerator:
    def __init__(self):
        self.prompt_builder = PromptBuilder()

        self.client = None

        if settings.GEMINI_API_KEY:
            self.client = genai.Client(api_key=settings.GEMINI_API_KEY)

    async def generate_report(
        self,
        features: dict,
        trait_scores: dict,
        traits: list[str],
    ) -> dict:
        if not self.client:
            return self._fallback_report(trait_scores, traits, source="fallback_no_api_key")

        prompt = self.prompt_builder.build_personality_report_prompt(
            features=features,
            trait_scores=trait_scores,
            traits=traits,
        )

        try:
            return await asyncio.to_thread(self._call_gemini, prompt)
        except Exception as error:
            fallback = self._fallback_report(
                trait_scores=trait_scores,
                traits=traits,
                source="fallback_llm_error",
            )
            fallback["llm_error"] = str(error)
            return fallback

    def _call_gemini(self, prompt: str) -> dict:
        response = self.client.models.generate_content(
            model=settings.GEMINI_MODEL,
            contents=prompt,
            config=types.GenerateContentConfig(
                temperature=0.7,
                max_output_tokens=1200,
                response_mime_type="application/json",
            ),
        )

        text = response.text or ""
        data = self._parse_json(text)

        validated = PersonalityReport.model_validate(data)

        result = validated.model_dump()
        result["generation_source"] = "gemini"

        return result

    def _parse_json(self, text: str) -> dict:
        cleaned = text.strip()

        # Handles cases where the model wraps JSON in ```json blocks.
        cleaned = re.sub(r"^```json", "", cleaned).strip()
        cleaned = re.sub(r"^```", "", cleaned).strip()
        cleaned = re.sub(r"```$", "", cleaned).strip()

        return json.loads(cleaned)

    def _fallback_report(
        self,
        trait_scores: dict,
        traits: list[str],
        source: str,
    ) -> dict:
        top_dimensions = sorted(
            trait_scores.items(),
            key=lambda item: item[1].get("score", 0),
            reverse=True,
        )[:3]

        top_names = [
            name.replace("_", " ")
            for name, _ in top_dimensions
        ]

        readable_traits = traits[:5] if traits else top_names

        summary_traits = ", ".join(readable_traits) if readable_traits else "balanced and reflective"

        return {
            "summary": f"Your visual indicators suggest a {summary_traits} style. This reading is best understood as a soft self-reflection insight rather than a scientific personality assessment.",
            "core_traits": readable_traits,
            "strengths": [
                "Ability to adapt your expression and style",
                "Balanced approach to personal interaction",
                "Potential for thoughtful decision-making",
            ],
            "growth_areas": [
                "Maintaining consistency under pressure",
                "Balancing intuition with structured decisions",
            ],
            "career_style": "You may be comfortable in roles that combine independent thinking with flexible problem-solving.",
            "relationship_style": "You may prefer interactions that feel natural, meaningful, and emotionally balanced.",
            "confidence_note": "This report is generated from image-derived visual features and should be treated as entertainment-style guidance.",
            "disclaimer": "This analysis is for entertainment and self-reflection only. It is not a psychological, medical, hiring, or diagnostic assessment.",
            "generation_source": source,
        }