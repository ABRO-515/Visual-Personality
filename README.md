# Visual Personality API

Phase 1 backend for visual feature extraction using FastAPI, OpenCV, and MediaPipe.

## What this MVP does

- Accepts face image upload
- Accepts palm image upload
- Validates image quality
- Extracts facial landmarks using MediaPipe FaceMesh
- Extracts hand landmarks using MediaPipe Hands
- Uses OpenCV for image loading, blur detection, brightness check, and palm-line density
- Returns structured feature JSON
- Maps visual features to soft entertainment-style traits

## Run Project

```bash
uv run uvicorn app.main:app --reload