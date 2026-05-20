from fastapi import APIRouter, File, UploadFile

from app.services.image_loader import upload_file_to_cv2_image
from app.services.quality import validate_image_quality
from app.services.face_analyzer import FaceAnalyzer
from app.services.palm_analyzer import PalmAnalyzer
from app.services.trait_engine import TraitEngine


router = APIRouter()


def get_face_analyzer() -> FaceAnalyzer:
    return FaceAnalyzer()


def get_palm_analyzer() -> PalmAnalyzer:
    return PalmAnalyzer()


def get_trait_engine() -> TraitEngine:
    return TraitEngine()


@router.post("/face")
async def analyze_face(file: UploadFile = File(...)):
    image = await upload_file_to_cv2_image(file)

    quality = validate_image_quality(image)

    face_analyzer = get_face_analyzer()
    trait_engine = get_trait_engine()

    face_features = face_analyzer.analyze(image)
    traits = trait_engine.map_face_traits(face_features)

    return {
        "type": "face_analysis",
        "quality": quality,
        "features": face_features,
        "traits": traits,
    }


@router.post("/palm")
async def analyze_palm(file: UploadFile = File(...)):
    image = await upload_file_to_cv2_image(file)

    quality = validate_image_quality(image)

    palm_analyzer = get_palm_analyzer()
    trait_engine = get_trait_engine()

    palm_features = palm_analyzer.analyze(image)
    traits = trait_engine.map_palm_traits(palm_features)

    return {
        "type": "palm_analysis",
        "quality": quality,
        "features": palm_features,
        "traits": traits,
    }


@router.post("/combined")
async def analyze_combined(
    face_file: UploadFile = File(...),
    palm_file: UploadFile = File(...),
):
    face_image = await upload_file_to_cv2_image(face_file)
    palm_image = await upload_file_to_cv2_image(palm_file)

    face_quality = validate_image_quality(face_image)
    palm_quality = validate_image_quality(palm_image)

    face_analyzer = get_face_analyzer()
    palm_analyzer = get_palm_analyzer()
    trait_engine = get_trait_engine()

    face_features = face_analyzer.analyze(face_image)
    palm_features = palm_analyzer.analyze(palm_image)

    combined_traits = trait_engine.map_combined_traits(
        face_features=face_features,
        palm_features=palm_features,
    )

    return {
        "type": "combined_analysis",
        "quality": {
            "face": face_quality,
            "palm": palm_quality,
        },
        "features": {
            "face": face_features,
            "palm": palm_features,
        },
        "traits": combined_traits,
    }