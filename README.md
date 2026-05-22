# Visual Personality API

A FastAPI-based visual personality analysis MVP that uses computer vision to analyze face and palm images and generate personality trait reports.

## ⚠️ Disclaimer

**This project is for entertainment and self-reflection purposes only.** It does not provide scientific, psychological, medical, hiring, or diagnostic assessments. The personality traits generated are based on visual feature extraction and rule-based mapping, not validated psychological research.

## Features

- **Face Analysis** - Extracts facial features using MediaPipe FaceMesh:
  - Face symmetry and ratios
  - Eye openness and symmetry
  - Smile intensity
  - Head tilt angle
  - Mouth and jaw symmetry

- **Palm Analysis** - Extracts palm features using MediaPipe Hands:
  - Palm geometry (width, height, ratios)
  - Finger length measurements
  - Palm line density analysis using Canny edge detection

- **Trait Mapping** - Rule-based engine that maps visual features to personality traits

- **Scoring Engine** - Generates trait scores across personality dimensions

- **Report Generation** - Uses Google Gemini API to create narrative personality reports (with fallback template if API unavailable)

## Tech Stack

- **FastAPI** - Modern web framework
- **MediaPipe** - Face mesh and hand landmark detection
- **OpenCV** - Image processing and computer vision
- **Google Gemini (GenAI)** - LLM for narrative report generation
- **Pydantic** - Data validation and settings management
- **NumPy** - Numerical computations

## Installation

### Prerequisites
- Python 3.11+
- uv (recommended) or pip

### Setup with uv
```bash
# Clone the repository
git clone <repository-url>
cd Visual-Personality

# Install dependencies
uv sync

# Activate virtual environment
source .venv/bin/activate  # On Windows: .venv\Scripts\activate
```

### Setup with pip
```bash
# Clone the repository
git clone <repository-url>
cd Visual-Personality

# Create virtual environment
python -m venv .venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt
```

### Configuration

Create a `.env` file in the project root (copy from `.env.example`):

```bash
cp .env.example .env
```

Edit `.env` and add your Google Gemini API key (optional - without it, the API will use fallback reports):

```env
GEMINI_API_KEY=your_gemini_api_key_here
GEMINI_MODEL=gemini-2.5-flash
```

## Usage

### Running the Server

```bash
# Development server with auto-reload
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000

# Production server
uvicorn app.main:app --host 0.0.0.0 --port 8000
```

The API will be available at `http://localhost:8000`

### API Documentation

Once the server is running, visit:
- **Swagger UI**: `http://localhost:8000/docs`
- **ReDoc**: `http://localhost:8000/redoc`

## API Endpoints

### POST `/api/v1/face`
Analyze a face image.

**Request**: Multipart form data with `file` field containing the face image.

**Response**:
```json
{
  "type": "face_analysis",
  "quality": {
    "valid": true,
    "width": 800,
    "height": 600,
    "blur_score": 120.5
  },
  "features": {
    "face_width": 234.5678,
    "face_height": 289.1234,
    "face_ratio": 1.2345,
    "eye_openness": 0.2345,
    "eye_symmetry": 0.9876,
    "mouth_width": 45.6789,
    "mouth_opening": 5.4321,
    "smile_intensity": 0.3456,
    "mouth_symmetry": 0.9123,
    "jaw_symmetry": 0.8765,
    "overall_face_symmetry": 0.9255,
    "head_tilt_angle": 2.3456
  },
  "traits": ["balanced", "socially expressive", "alert and attentive", "composed"],
  "trait_scores": {
    "openness": {"score": 0.75, "confidence": "medium"},
    "conscientiousness": {"score": 0.68, "confidence": "medium"}
  }
}
```

### POST `/api/v1/palm`
Analyze a palm image.

**Request**: Multipart form data with `file` field containing the palm image.

**Response**:
```json
{
  "type": "palm_analysis",
  "quality": {
    "valid": true,
    "width": 800,
    "height": 600,
    "blur_score": 110.2
  },
  "features": {
    "palm_width": 123.4567,
    "palm_height": 145.6789,
    "palm_ratio": 0.8472,
    "hand_type": "long_palm",
    "thumb_length": 67.8901,
    "index_length": 78.9012,
    "middle_length": 89.0123,
    "ring_length": 76.5432,
    "pinky_length": 56.7890,
    "index_ring_ratio": 1.0308,
    "palm_line_density": 0.0654,
    "palm_line_density_label": "medium"
  },
  "traits": ["imaginative", "balanced focus", "structured thinker"],
  "trait_scores": {
    "creativity": {"score": 0.72, "confidence": "medium"},
    "practicality": {"score": 0.65, "confidence": "medium"}
  }
}
```

### POST `/api/v1/combined`
Analyze both face and palm images together with a full narrative report.

**Request**: Multipart form data with `face_file` and `palm_file` fields.

**Response**:
```json
{
  "type": "combined_analysis",
  "quality": {
    "face": {
      "valid": true,
      "width": 800,
      "height": 600,
      "blur_score": 120.5
    },
    "palm": {
      "valid": true,
      "width": 800,
      "height": 600,
      "blur_score": 110.2
    }
  },
  "features": {
    "face": { /* face features */ },
    "palm": { /* palm features */ }
  },
  "traits": ["balanced", "imaginative", "socially expressive"],
  "trait_scores": { /* trait scores */ },
  "report": {
    "summary": "Your visual indicators suggest a balanced, imaginative, and socially expressive style...",
    "core_traits": ["balanced", "imaginative", "socially expressive"],
    "strengths": ["Ability to adapt your expression", "Balanced approach to interaction"],
    "growth_areas": ["Maintaining consistency under pressure"],
    "career_style": "You may be comfortable in roles that combine independent thinking...",
    "relationship_style": "You may prefer interactions that feel natural...",
    "confidence_note": "This report is generated from image-derived visual features...",
    "disclaimer": "This analysis is for entertainment and self-reflection only...",
    "generation_source": "gemini"
  }
}
```

## Project Structure

```
Visual-Personality/
├── app/
│   ├── api/
│   │   └── v1/
│   │       ├── endpoints/
│   │       │   ├── analysis.py    # Main analysis endpoints
│   │       │   └── health.py      # Health check endpoint
│   │       └── router.py          # API router
│   ├── core/
│   │   └── config.py              # Configuration settings
│   ├── schemas/
│   │   ├── analysis.py            # Analysis response models
│   │   └── report.py              # Report response models
│   ├── services/
│   │   ├── face_analyzer.py       # Face feature extraction
│   │   ├── palm_analyzer.py       # Palm feature extraction
│   │   ├── trait_engine.py        # Trait mapping logic
│   │   ├── score_engine.py        # Trait scoring
│   │   ├── report_generator.py    # LLM report generation
│   │   ├── prompt_builder.py      # LLM prompt construction
│   │   ├── image_loader.py        # Image upload handling
│   │   └── quality.py             # Image quality validation
│   ├── utils/
│   │   └── geometry.py            # Geometric calculations
│   └── main.py                    # FastAPI application
├── tests/
│   └── test_health.py             # Health check tests
├── .env.example                   # Environment variables template
├── pyproject.toml                 # Project dependencies
└── README.md                      # This file
```

## Configuration Options

Environment variables in `.env`:

- `GEMINI_API_KEY` - Google Gemini API key (optional, for enhanced reports)
- `GEMINI_MODEL` - Gemini model to use (default: `gemini-2.5-flash`)
- `MIN_IMAGE_WIDTH` - Minimum image width in pixels (default: 300)
- `MIN_IMAGE_HEIGHT` - Minimum image height in pixels (default: 300)
- `BLUR_THRESHOLD` - Blur detection threshold (default: 80.0)

## Development

### Running Tests

```bash
pytest
```

### Code Quality

The project uses:
- Type hints throughout
- Pydantic for data validation
- Structured service layer architecture
- Async/await for I/O operations

## Limitations

- Single face/palm detection per image
- Requires good lighting and clear images
- Trait mapping is rule-based, not scientifically validated
- LLM reports depend on API availability and quality

## License

[Add your license here]

## Contributing

[Add contribution guidelines here]