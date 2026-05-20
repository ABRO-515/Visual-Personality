import cv2
import mediapipe as mp
from fastapi import HTTPException

from app.utils.geometry import (
    euclidean_distance,
    safe_ratio,
    similarity_score,
    angle_between_points,
)


class FaceAnalyzer:
    def __init__(self):
        self.mp_face_mesh = mp.solutions.face_mesh

    def analyze(self, image):
        rgb_image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
        height, width = image.shape[:2]

        with self.mp_face_mesh.FaceMesh(
            static_image_mode=True,
            max_num_faces=1,
            refine_landmarks=True,
            min_detection_confidence=0.5,
        ) as face_mesh:
            results = face_mesh.process(rgb_image)

        if not results.multi_face_landmarks:
            raise HTTPException(
                status_code=422,
                detail="No face detected in the image.",
            )

        landmarks = results.multi_face_landmarks[0].landmark
        points = self._to_pixel_points(landmarks, width, height)

        return self._extract_features(points)

    def _to_pixel_points(self, landmarks, width: int, height: int):
        return {
            index: (landmark.x * width, landmark.y * height)
            for index, landmark in enumerate(landmarks)
        }

    def _extract_features(self, points):
        # Common MediaPipe FaceMesh landmark indices
        left_eye_outer = points[33]
        left_eye_inner = points[133]
        right_eye_inner = points[362]
        right_eye_outer = points[263]

        left_eye_top = points[159]
        left_eye_bottom = points[145]
        right_eye_top = points[386]
        right_eye_bottom = points[374]

        mouth_left = points[61]
        mouth_right = points[291]
        upper_lip = points[13]
        lower_lip = points[14]

        face_left = points[234]
        face_right = points[454]
        face_top = points[10]
        chin = points[152]
        nose_tip = points[1]

        face_width = euclidean_distance(face_left, face_right)
        face_height = euclidean_distance(face_top, chin)

        mouth_width = euclidean_distance(mouth_left, mouth_right)
        mouth_opening = euclidean_distance(upper_lip, lower_lip)

        left_eye_width = euclidean_distance(left_eye_outer, left_eye_inner)
        right_eye_width = euclidean_distance(right_eye_inner, right_eye_outer)

        left_eye_opening = euclidean_distance(left_eye_top, left_eye_bottom)
        right_eye_opening = euclidean_distance(right_eye_top, right_eye_bottom)

        left_eye_openness = safe_ratio(left_eye_opening, left_eye_width)
        right_eye_openness = safe_ratio(right_eye_opening, right_eye_width)

        eye_openness_score = (left_eye_openness + right_eye_openness) / 2

        eye_symmetry = similarity_score(left_eye_width, right_eye_width)

        left_mouth_distance = euclidean_distance(nose_tip, mouth_left)
        right_mouth_distance = euclidean_distance(nose_tip, mouth_right)
        mouth_symmetry = similarity_score(left_mouth_distance, right_mouth_distance)

        left_face_distance = euclidean_distance(nose_tip, face_left)
        right_face_distance = euclidean_distance(nose_tip, face_right)
        jaw_symmetry = similarity_score(left_face_distance, right_face_distance)

        overall_symmetry = (eye_symmetry + mouth_symmetry + jaw_symmetry) / 3

        head_tilt_angle = angle_between_points(left_eye_outer, right_eye_outer)

        smile_intensity = safe_ratio(mouth_width, face_width)
        face_ratio = safe_ratio(face_height, face_width)

        return {
            "face_width": round(face_width, 4),
            "face_height": round(face_height, 4),
            "face_ratio": round(face_ratio, 4),

            "eye_openness": round(eye_openness_score, 4),
            "eye_symmetry": round(eye_symmetry, 4),

            "mouth_width": round(mouth_width, 4),
            "mouth_opening": round(mouth_opening, 4),
            "smile_intensity": round(smile_intensity, 4),
            "mouth_symmetry": round(mouth_symmetry, 4),

            "jaw_symmetry": round(jaw_symmetry, 4),
            "overall_face_symmetry": round(overall_symmetry, 4),

            "head_tilt_angle": round(head_tilt_angle, 4),
        }
