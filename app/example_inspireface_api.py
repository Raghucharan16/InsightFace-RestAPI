"""
Example FastAPI integration with InspireFace Pikachu model.
This API runs in GitHub Actions (Linux environment).
On Windows, InspireFace is not supported - use the standard main.py instead.

Shows how to add face detection endpoints to your REST API.
"""

import os
import sys

# Try importing InspireFace (only available on Linux)
try:
    import inspireface as isf
    INSPIREFACE_AVAILABLE = True
except ImportError:
    INSPIREFACE_AVAILABLE = False
    print("⚠️  Warning: InspireFace not available on this platform (expected on Windows)")
    print("   InspireFace is only supported on Linux and will be used in GitHub Actions")

from fastapi import FastAPI, File, UploadFile, HTTPException
from fastapi.responses import JSONResponse
import cv2
import numpy as np

app = FastAPI(
    title="InsightFace REST API with InspireFace",
    description="Face Recognition API using InspireFace Pikachu Model (Linux only)",
    version="1.0.0"
)

# Global variables
session = None
MODELS_PATH = os.path.join(os.path.dirname(__file__), "..", "models")


@app.on_event("startup")
async def startup_event():
    """Initialize InspireFace model on startup"""
    global session
    
    if not INSPIREFACE_AVAILABLE:
        print("⚠️  InspireFace not available - skipping initialization")
        return
    
    print("\n" + "="*70)
    print("INITIALIZING INSPIREFACE MODEL")
    print("="*70)
    
    try:
        # Set resource path
        print(f"📁 Models path: {MODELS_PATH}")
        if not os.path.exists(MODELS_PATH):
            print(f"✗ Models directory not found at: {MODELS_PATH}")
            return
        
        ret = isf.set_resource_path(MODELS_PATH)
        if not ret:
            print("✗ Failed to set resource path")
            return
        
        # Load Pikachu model
        print("🚀 Loading Pikachu model...")
        ret = isf.reload("Pikachu")
        if not ret:
            print("✗ Failed to load Pikachu model")
            print(f"   Check that model exists at: {os.path.join(MODELS_PATH, 'pikachu', 'Pikachu')}")
            return
        
        # Create session
        print("✨ Creating InspireFace session...")
        opt = isf.HF_ENABLE_FACE_RECOGNITION
        session = isf.InspireFaceSession(opt, isf.HF_DETECT_MODE_ALWAYS_DETECT)
        
        print("✓ InspireFace initialized successfully!")
        print("="*70 + "\n")
        
    except Exception as e:
        print(f"✗ Error initializing InspireFace: {e}")
        print("="*70 + "\n")


@app.on_event("shutdown")
async def shutdown_event():
    """Cleanup on shutdown"""
    if INSPIREFACE_AVAILABLE:
        print("Shutting down InspireFace session...")


@app.get("/")
async def root():
    """Root endpoint"""
    return {
        "message": "InsightFace REST API with InspireFace Support",
        "status": "running",
        "model": "Pikachu",
        "inspireface_available": INSPIREFACE_AVAILABLE,
        "platform": "Linux (GitHub Actions)" if INSPIREFACE_AVAILABLE else "Windows (Limited)",
        "endpoints": {
            "/health": "Health check",
            "/docs": "API documentation",
            "/api/detect-faces": "Detect faces in image",
        }
    }


@app.get("/health")
async def health():
    """Health check endpoint"""
    global session
    return {
        "status": "healthy" if session or not INSPIREFACE_AVAILABLE else "initializing",
        "model": "Pikachu",
        "ready": session is not None,
        "inspireface_available": INSPIREFACE_AVAILABLE
    }


@app.post("/api/detect-faces")
async def detect_faces(file: UploadFile = File(...)):
    """
    Detect faces in an uploaded image.
    Only available when InspireFace is installed (GitHub Actions).
    
    Returns:
    - faces_count: Number of faces detected
    - faces: List of detected faces with bounding boxes and confidence
    """
    global session
    
    if not INSPIREFACE_AVAILABLE:
        raise HTTPException(
            status_code=501,
            detail="InspireFace not available on this platform. Use GitHub Actions for full functionality."
        )
    
    if session is None:
        raise HTTPException(status_code=503, detail="Model not initialized")
    
    try:
        # Read image
        contents = await file.read()
        nparr = np.frombuffer(contents, np.uint8)
        image = cv2.imdecode(nparr, cv2.IMREAD_COLOR)
        
        if image is None:
            raise HTTPException(status_code=400, detail="Invalid image format")
        
        # Detect faces
        faces = session.face_detection(image)
        
        # Format response
        detected_faces = [
            {
                "id": idx,
                "x": int(face.x),
                "y": int(face.y),
                "width": int(face.width),
                "height": int(face.height),
                "confidence": float(face.confidence)
            }
            for idx, face in enumerate(faces)
        ]
        
        return JSONResponse({
            "success": True,
            "faces_count": len(faces),
            "faces": detected_faces,
            "image_size": {
                "width": image.shape[1],
                "height": image.shape[0]
            }
        })
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error processing image: {str(e)}")


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
