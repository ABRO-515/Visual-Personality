import cv2
import mediapipe as mp
from fastapi import HTTPException

from app.utils.geometry import euclidean_distance, safe_ratio


class PalmAnalyzer:
    def __init__(self):
        self.mp_hands = mp.solutions.hands

    def analyze(self, image):
        rgb_image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
        height, width = image.shape[:2]

        with self.mp_hands.Hands(
            static_image_mode=True,
            max_num_hands=1,
            min_detection_confidence=0.5,
        ) as hands:
            results = hands.process(rgb_image)

        print("\n========== MEDIAPIPE HANDS RAW OUTPUT ==========", flush=True)
        print("results:", results, flush=True)
        print("multi_hand_landmarks:", results.multi_hand_landmarks, flush=True)
        print("multi_handedness:", results.multi_handedness, flush=True)

        if results.multi_hand_landmarks:
            for hand_index, hand_landmarks in enumerate(results.multi_hand_landmarks):
                print(f"\n--- Hand {hand_index} landmarks ---", flush=True)

                for i, landmark in enumerate(hand_landmarks.landmark):
                    print(
                        f"Landmark {i}: "
                        f"x={landmark.x:.4f}, "
                        f"y={landmark.y:.4f}, "
                        f"z={landmark.z:.4f}",
                        flush=True,
                    )

        print("===============================================\n", flush=True)

        if not results.multi_hand_landmarks:
            raise HTTPException(
                status_code=422,
                detail="No hand/palm detected in the image.",
            )

        landmarks = results.multi_hand_landmarks[0].landmark
        points = self._to_pixel_points(landmarks, width, height)

        geometry_features = self._extract_geometry_features(points)
        line_features = self._extract_palm_line_features(image, points)

        return {
            **geometry_features,
            **line_features,
        }

    def _to_pixel_points(self, landmarks, width: int, height: int):
        return {
            index: (landmark.x * width, landmark.y * height)
            for index, landmark in enumerate(landmarks)
        }

    def _extract_geometry_features(self, points):
        wrist = points[0]

        index_mcp = points[5]
        middle_mcp = points[9]
        ring_mcp = points[13]
        pinky_mcp = points[17]

        thumb_tip = points[4]
        index_tip = points[8]
        middle_tip = points[12]
        ring_tip = points[16]
        pinky_tip = points[20]

        palm_width = euclidean_distance(index_mcp, pinky_mcp)
        palm_height = euclidean_distance(wrist, middle_mcp)
        palm_ratio = safe_ratio(palm_width, palm_height)

        index_length = euclidean_distance(index_mcp, index_tip)
        middle_length = euclidean_distance(middle_mcp, middle_tip)
        ring_length = euclidean_distance(ring_mcp, ring_tip)
        pinky_length = euclidean_distance(pinky_mcp, pinky_tip)
        thumb_length = euclidean_distance(wrist, thumb_tip)

        index_ring_ratio = safe_ratio(index_length, ring_length)

        if palm_ratio >= 0.9:
            hand_type = "square_palm"
        else:
            hand_type = "long_palm"

        return {
            "palm_width": round(palm_width, 4),
            "palm_height": round(palm_height, 4),
            "palm_ratio": round(palm_ratio, 4),
            "hand_type": hand_type,

            "thumb_length": round(thumb_length, 4),
            "index_length": round(index_length, 4),
            "middle_length": round(middle_length, 4),
            "ring_length": round(ring_length, 4),
            "pinky_length": round(pinky_length, 4),

            "index_ring_ratio": round(index_ring_ratio, 4),
        }

    def _extract_palm_line_features(self, image, points):
        height, width = image.shape[:2]

        xs = [p[0] for p in points.values()]
        ys = [p[1] for p in points.values()]

        x_min = max(int(min(xs)) - 20, 0)
        y_min = max(int(min(ys)) - 20, 0)
        x_max = min(int(max(xs)) + 20, width)
        y_max = min(int(max(ys)) + 20, height)

        hand_crop = image[y_min:y_max, x_min:x_max]

        if hand_crop.size == 0:
            return {
                "palm_line_density": 0.0,
                "palm_line_density_label": "unknown",
            }

        gray = cv2.cvtColor(hand_crop, cv2.COLOR_BGR2GRAY)

        clahe = cv2.createCLAHE(clipLimit=2.0, tileGridSize=(8, 8))
        enhanced = clahe.apply(gray)

        blurred = cv2.GaussianBlur(enhanced, (3, 3), 0)
        edges = cv2.Canny(blurred, 50, 150)

        edge_pixels = cv2.countNonZero(edges)
        total_pixels = edges.shape[0] * edges.shape[1]

        density = edge_pixels / total_pixels if total_pixels else 0.0

        if density < 0.04:
            label = "low"
        elif density < 0.09:
            label = "medium"
        else:
            label = "high"

        return {
            "palm_line_density": round(float(density), 4),
            "palm_line_density_label": label,
        }
