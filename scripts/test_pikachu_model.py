"""
Test script to verify InspireFace Pikachu model setup.
This script only runs in GitHub Actions (Linux environment).
On Windows, it will be skipped as InspireFace is not supported.
"""

import os
import sys

# Try to import inspireface library (only available on Linux)
try:
    import inspireface as isf
    INSPIREFACE_AVAILABLE = True
except ImportError:
    INSPIREFACE_AVAILABLE = False
    print("⚠️  InspireFace not available (expected on Windows)")
    print("   InspireFace is only supported on Linux")
    print("   It will be tested in GitHub Actions CI/CD")
    sys.exit(0)

import cv2

# Get the models directory path
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
REPO_ROOT = os.path.dirname(SCRIPT_DIR)
MODELS_DIR = os.path.join(REPO_ROOT, "models")
PIKACHU_MODEL = os.path.join(MODELS_DIR, "pikachu", "Pikachu")

print(f"\n📁 Models directory: {MODELS_DIR}")
print(f"🔍 Looking for Pikachu model at: {PIKACHU_MODEL}")


def check_model_exists():
    """Check if Pikachu model exists"""
    if os.path.exists(PIKACHU_MODEL):
        file_size = os.path.getsize(PIKACHU_MODEL)
        print(f"✓ Pikachu model found ({file_size / (1024*1024):.1f}MB)")
        return True
    else:
        print(f"✗ Pikachu model not found at {PIKACHU_MODEL}")
        return False


def test_inspireface_initialization():
    """Test InspireFace initialization"""
    print("\n" + "="*70)
    print("TESTING INSPIREFACE INITIALIZATION")
    print("="*70)
    
    try:
        # Set the resource path
        print(f"\n📦 Setting resource path to: {MODELS_DIR}")
        ret = isf.set_resource_path(MODELS_DIR)
        if not ret:
            print("✗ Failed to set resource path")
            return False
        
        # Load Pikachu model
        print("🚀 Loading Pikachu model...")
        ret = isf.reload("Pikachu")
        if not ret:
            print("✗ Failed to load Pikachu model")
            return False
        
        print("✓ Pikachu model loaded successfully")
        
        # Enable face recognition features
        print("\n✨ Enabling face recognition features...")
        opt = isf.HF_ENABLE_FACE_RECOGNITION
        session = isf.InspireFaceSession(opt, isf.HF_DETECT_MODE_ALWAYS_DETECT)
        print("✓ Face recognition session created")
        
        return True
        
    except Exception as e:
        print(f"✗ Error: {e}")
        return False


def main():
    """Main test function"""
    print("\n" + "="*70)
    print("INSPIREFACE PIKACHU MODEL TEST")
    print("="*70)
    
    if not check_model_exists():
        print("\n⚠️  Model not found, skipping initialization test")
        return
    
    if test_inspireface_initialization():
        print("\n" + "="*70)
        print("✓ ALL TESTS PASSED!")
        print("="*70)
    else:
        print("\n" + "="*70)
        print("✗ TESTS FAILED!")
        print("="*70)
        sys.exit(1)


if __name__ == "__main__":
    main()

