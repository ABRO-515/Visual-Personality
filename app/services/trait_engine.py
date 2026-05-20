class TraitEngine:
    """
    MVP rule engine.

    This does NOT scientifically predict personality.
    It maps extracted visual features into soft, entertainment-style traits.
    Later, these traits can be sent to an LLM for narrative report generation.
    """

    def map_face_traits(self, face_features: dict) -> list[str]:
        traits = []

        symmetry = face_features.get("overall_face_symmetry", 0)
        smile = face_features.get("smile_intensity", 0)
        eye_openness = face_features.get("eye_openness", 0)
        head_tilt = abs(face_features.get("head_tilt_angle", 0))

        if symmetry >= 0.85:
            traits.append("balanced")
        elif symmetry >= 0.7:
            traits.append("adaptive")

        if smile >= 0.35:
            traits.append("socially expressive")

        if eye_openness >= 0.22:
            traits.append("alert and attentive")

        if head_tilt <= 5:
            traits.append("composed")
        else:
            traits.append("dynamic expression")

        return traits

    def map_palm_traits(self, palm_features: dict) -> list[str]:
        traits = []

        hand_type = palm_features.get("hand_type")
        line_density = palm_features.get("palm_line_density_label")
        index_ring_ratio = palm_features.get("index_ring_ratio", 0)

        if hand_type == "square_palm":
            traits.append("practical")
        elif hand_type == "long_palm":
            traits.append("imaginative")

        if line_density == "high":
            traits.append("detail-oriented")
        elif line_density == "medium":
            traits.append("balanced focus")
        elif line_density == "low":
            traits.append("simple and direct")

        if index_ring_ratio >= 1:
            traits.append("structured thinker")
        else:
            traits.append("action-oriented")

        return traits

    def map_combined_traits(self, face_features: dict, palm_features: dict) -> list[str]:
        face_traits = self.map_face_traits(face_features)
        palm_traits = self.map_palm_traits(palm_features)

        combined = face_traits + palm_traits

        # Remove duplicates while preserving order
        return list(dict.fromkeys(combined))
