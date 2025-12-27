# InsightFace REST API

A FastAPI-based REST API for face recognition using InsightFace (DeepInsight) and InspireFace libraries.

## Project Structure

```
├── app/
│   ├── main.py                      # Main API with DeepInsight models
│   ├── example_inspireface_api.py   # Example API with InspireFace support (Linux/GitHub Actions)
│   ├── core/
│   │   ├── buffalo.py               # Buffalo_L recognizer
│   │   ├── detector.py              # Face detection
│   │   ├── swapper.py               # Face swapping
│   │   └── inspire.py               # InspireFace wrapper
│   └── utils.py
├── scripts/
│   ├── download_models.py           # Download required models
│   └── test_pikachu_model.py        # Test InspireFace Pikachu model
├── models/                          # Pre-downloaded models
│   ├── buffalo_l/                   # DeepInsight face detection & recognition
│   ├── pikachu/                     # InspireFace lightweight model (16MB)
│   └── inswapper_128.onnx           # Optional face swapping model
├── requirements.txt                 # Base Python dependencies
├── requirements-ci.txt              # GitHub Actions dependencies (includes InspireFace)
└── .github/workflows/ci.yml         # CI/CD pipeline configuration
```

## Development Environment (Windows)

### Install Base Dependencies

```bash
pip install -r requirements.txt
```

### Run Main API

```bash
python -m uvicorn app.main:app --reload
```

The API will be available at `http://localhost:8000`

**Note:** InspireFace is not available on Windows. Use the main API with DeepInsight models.

## GitHub Actions (Linux/CI)

### Install Full Dependencies (CI)

```bash
pip install -r requirements-ci.txt
```

This includes InspireFace which is Linux-only.

### Available Models

**DeepInsight Models:**
- `Buffalo_L` - Face detection & recognition (~100MB)
- `InSwapper` - Face swapping (~530MB)

**InspireFace Models:**
- `Pikachu` - Lightweight model (~16MB) - For edge devices
- `Megatron` - Full-featured model (~300MB) - For servers

### Download Models

```bash
python scripts/download_models.py
```

Models will be saved to the `models/` directory and cached in GitHub Actions.

### Test InspireFace (Linux only)

```bash
python scripts/test_pikachu_model.py
```

## API Endpoints

### Main API (`app/main.py`)

- `POST /recognition/embedding` - Get face embedding
- `POST /swap` - Swap faces in images

### InspireFace API (`app/example_inspireface_api.py`)

- `GET /` - API info
- `GET /health` - Health check
- `POST /api/detect-faces` - Detect faces in image

## Environment Setup

### Windows (Development)

```bash
# Create virtual environment
python -m venv env

# Activate
env\Scripts\activate

# Install dependencies
pip install -r requirements.txt
```

### Linux/GitHub Actions

Uses the complete requirements including InspireFace:

```bash
pip install -r requirements-ci.txt
```

## CI/CD Pipeline

The GitHub Actions workflow (`.github/workflows/ci.yml`):

1. ✅ Installs system dependencies (libgl1, etc.)
2. ✅ Installs Python packages (including InspireFace)
3. ✅ Downloads/caches models
4. ✅ Tests API initialization
5. ✅ Optionally builds Docker image

Models are cached automatically, so subsequent runs are much faster.

### Lazy Loading

The API uses **lazy loading** for the face swapping model:

- **Buffalo_L detector & recognizer**: Loaded eagerly (small, ~100MB)
- **InSwapper model**: Loaded on first use (large, ~530MB)

This allows the API to start immediately even if the swap model isn't downloaded yet. The model will be downloaded on-demand when the `/swap` endpoint is first called.

**Benefits:**
- Faster API startup
- Better compatibility with GitHub Actions CI
- Graceful degradation if model download fails

## Platform Support

| Feature | Windows | Linux/GitHub Actions |
|---------|---------|----------------------|
| DeepInsight (Buffalo_L, InSwapper) | ✅ | ✅ |
| InspireFace (Pikachu, Megatron) | ❌ | ✅ |
| Face Detection | ✅ | ✅ |
| Face Recognition | ✅ | ✅ |
| Face Swapping | ✅ | ✅ |

## Troubleshooting

### InspireFace import error

InspireFace is only available on Linux. This is expected on Windows.

**Solution:** Use the main API with DeepInsight models or deploy to GitHub Actions.

### Missing models

Run `python scripts/download_models.py` to download models locally.

Models are cached in GitHub Actions automatically.

### API import errors

Ensure all dependencies are installed:

```bash
pip install -r requirements.txt        # Windows
pip install -r requirements-ci.txt     # Linux/CI
```

## Deployment

### Local Development

```bash
python -m uvicorn app.main:app --host 0.0.0.0 --port 8000
```

### Docker

#### Quick Start with Docker Compose

```bash
# Build and start the API with Docker Compose
docker-compose up --build

# API will be available at http://localhost:8000
# Swagger docs: http://localhost:8000/docs
```

#### Manual Docker Build & Run

```bash
# Build the image
docker build -t insightface-api:latest .

# Run the container
docker run -p 8000:8000 \
  -v $(pwd)/models:/app/models \
  insightface-api:latest
```

**Health Check:**
```bash
curl http://localhost:8000/health
```

Expected response:
```json
{
  "status": "healthy",
  "service": "InsightFace REST API",
  "models": {
    "detector": "loaded",
    "recognizer": "loaded",
    "swapper": "lazy-loaded"
  }
}
```

### GitHub Actions

The CI/CD pipeline runs automatically on push to `main` branch.

To deploy:

1. Push changes to `main`
2. GitHub Actions will test and build
3. Models are cached for faster subsequent runs

## Resources

- [InsightFace GitHub](https://github.com/deepinsight/insightface)
- [InspireFace GitHub](https://github.com/HyperInspire/InspireFace)
- [FastAPI Documentation](https://fastapi.tiangolo.com/)