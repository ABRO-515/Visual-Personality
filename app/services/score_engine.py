class ScoreEngine:
    """
    Converts raw visual features into structured personality-style scores.

    This is not scientific personality prediction.
    It is an entertainment/self-reflection scoring layer.
    """

    def generate(self, face_features: dict | None = None, palm_features: dict | None = None) -> dict:
        face_features = face_features or {}
        palm_features = palm_features or {}

        scores = {
            "social_expression": {
                "score": 50,
                "signals": [],
            },
            "creativity": {
                "score": 50,
                "signals": [],
            },
            "focus_style": {
                "score": 50,
                "signals": [],
            },
            "emotional_balance": {
                "score": 50,
                "signals": [],
            },
            "decision_style": {
                "score": 50,
                "signals": [],
            },
            "practicality": {
                "score": 50,
                "signals": [],
            },
            "adaptability": {
                "score": 50,
                "signals": [],
            },
        }

        self._apply_face_rules(scores, face_features)
        self._apply_palm_rules(scores, palm_features)

        return self._finalize(scores)

    def _apply_face_rules(self, scores: dict, face: dict) -> None:
        symmetry = face.get("overall_face_symmetry", 0)
        smile = face.get("smile_intensity", 0)
        eye_openness = face.get("eye_openness", 0)
        head_tilt = abs(face.get("head_tilt_angle", 0))

        if symmetry >= 0.85:
            self._add(scores, "emotional_balance", 18, "high facial symmetry")
            self._add(scores, "decision_style", 8, "balanced facial proportions")
        elif symmetry >= 0.7:
            self._add(scores, "adaptability", 12, "moderate facial symmetry")

        if smile >= 0.35:
            self._add(scores, "social_expression", 22, "visible smile expression")
        elif smile >= 0.25:
            self._add(scores, "social_expression", 10, "mild smile expression")

        if eye_openness >= 0.24:
            self._add(scores, "focus_style", 16, "open eye posture")
            self._add(scores, "social_expression", 8, "attentive facial expression")
        elif eye_openness >= 0.18:
            self._add(scores, "focus_style", 8, "moderate eye openness")

        if head_tilt <= 5:
            self._add(scores, "emotional_balance", 10, "stable head alignment")
        else:
            self._add(scores, "adaptability", 10, "dynamic head angle")

    def _apply_palm_rules(self, scores: dict, palm: dict) -> None:
        hand_type = palm.get("hand_type")
        line_density = palm.get("palm_line_density_label")
        index_ring_ratio = palm.get("index_ring_ratio", 0)
        palm_ratio = palm.get("palm_ratio", 0)

        if hand_type == "square_palm":
            self._add(scores, "practicality", 22, "square palm geometry")
            self._add(scores, "decision_style", 10, "stable palm structure")

        elif hand_type == "long_palm":
            self._add(scores, "creativity", 22, "long palm geometry")
            self._add(scores, "adaptability", 12, "elongated palm structure")

        if line_density == "high":
            self._add(scores, "focus_style", 18, "high palm line density")
            self._add(scores, "creativity", 8, "complex palm line pattern")

        elif line_density == "medium":
            self._add(scores, "focus_style", 10, "medium palm line density")
            self._add(scores, "emotional_balance", 8, "balanced palm line pattern")

        elif line_density == "low":
            self._add(scores, "decision_style", 10, "low palm line density")
            self._add(scores, "practicality", 8, "simple palm line pattern")

        if index_ring_ratio >= 1:
            self._add(scores, "decision_style", 14, "index-to-ring finger ratio")
            self._add(scores, "focus_style", 8, "structured finger proportion")
        elif index_ring_ratio > 0:
            self._add(scores, "adaptability", 12, "ring finger dominant proportion")

        if palm_ratio >= 0.9:
            self._add(scores, "practicality", 10, "wide palm ratio")
        elif 0 < palm_ratio < 0.75:
            self._add(scores, "creativity", 10, "narrow palm ratio")

    def _add(self, scores: dict, dimension: str, points: int, signal: str) -> None:
        scores[dimension]["score"] += points
        scores[dimension]["signals"].append(signal)

    def _finalize(self, scores: dict) -> dict:
        finalized = {}

        for dimension, data in scores.items():
            score = self._clamp(data["score"])

            finalized[dimension] = {
                "score": score,
                "level": self._level(score),
                "signals": data["signals"],
            }

        return finalized

    def _clamp(self, score: int) -> int:
        return max(0, min(100, int(score)))

    def _level(self, score: int) -> str:
        if score >= 75:
            return "high"

        if score >= 45:
            return "medium"

        return "low"