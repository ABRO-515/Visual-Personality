import cv2
from fastapi import HTTPException

from app.core.config import settings


def validate_image_quality(image):
    height, width = image.shape[:2]

    if width < settings.MIN_IMAGE_WIDTH or height < settings.MIN_IMAGE_HEIGHT:
        raise HTTPException(
            status_code=400,
            detail=f"Image resolution too low. Minimum required is {settings.MIN_IMAGE_WIDTH}x{settings.MIN_IMAGE_HEIGHT}.",
        )

    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

    blur_score = float(cv2.Laplacian(gray, cv2.CV_64F).var())
    brightness = float(gray.mean())

    if blur_score < settings.BLUR_THRESHOLD:
        raise HTTPException(
            status_code=400,
            detail=f"Image is too blurry. Blur score: {blur_score:.2f}",
        )

    return {
        "width": width,
        "height": height,
        "blur_score": round(blur_score, 2),
        "brightness": round(brightness, 2),
    }
