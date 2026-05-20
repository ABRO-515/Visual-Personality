import math


def euclidean_distance(p1: tuple[float, float], p2: tuple[float, float]) -> float:
    return math.sqrt((p1[0] - p2[0]) ** 2 + (p1[1] - p2[1]) ** 2)


def safe_ratio(a: float, b: float) -> float:
    if b == 0:
        return 0.0
    return a / b


def similarity_score(left_value: float, right_value: float) -> float:
    """
    Returns score between 0 and 1.
    1 means highly similar.
    0 means highly different.
    """
    max_value = max(abs(left_value), abs(right_value))

    if max_value == 0:
        return 0.0

    score = 1 - (abs(left_value - right_value) / max_value)
    return max(0.0, min(1.0, score))


def angle_between_points(p1: tuple[float, float], p2: tuple[float, float]) -> float:
    dx = p2[0] - p1[0]
    dy = p2[1] - p1[1]

    angle = math.degrees(math.atan2(dy, dx))
    return angle
