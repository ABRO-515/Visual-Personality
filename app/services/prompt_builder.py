import json


class PromptBuilder:
    def build_personality_report_prompt(
        self,
        features: dict,
        trait_scores: dict,
        traits: list[str],
    ) -> str:
        payload = {
            "visual_features": features,
            "trait_scores": trait_scores,
            "traits": traits,
        }

        return f"""
You are generating a user-facing AI personality insight report for an entertainment/self-reflection app.

Important rules:
- Do not claim scientific certainty.
- Do not say this is a medical, psychological, hiring, criminal, or diagnostic assessment.
- Do not mention palmistry as proven science.
- Use soft language like "suggests", "may indicate", "appears", "leans toward".
- Make the report feel personal, useful, and polished.
- Return valid JSON only.
- Do not include markdown.
- Do not include extra text outside JSON.

Input data:
{json.dumps(payload, indent=2)}

Return JSON in exactly this structure:

{{
  "summary": "string",
  "core_traits": ["string"],
  "strengths": ["string"],
  "growth_areas": ["string"],
  "career_style": "string",
  "relationship_style": "string",
  "confidence_note": "string",
  "disclaimer": "string"
}}
"""