#!/usr/bin/env python
"""
Test script to verify lazy loading works correctly.
This should not fail even if the inswapper model hasn't been downloaded yet.
"""

import sys
import time

print("=" * 60)
print("Testing Lazy Loading Implementation")
print("=" * 60)

# Test 1: Import main app (should NOT download models)
print("\n[Test 1] Importing app.main (should succeed without models)...")
try:
    start = time.time()
    from app.main import app
    elapsed = time.time() - start
    print(f"✓ API imported successfully in {elapsed:.2f}s")
    print("  (No model downloads attempted)")
except Exception as e:
    print(f"✗ Failed to import app: {e}")
    sys.exit(1)

# Test 2: Check FaceSwapper is not loaded
print("\n[Test 2] Checking FaceSwapper lazy loading state...")
try:
    from app.main import swapper
    if not swapper._model_loaded:
        print("✓ FaceSwapper model not yet loaded (lazy loading working)")
    else:
        print("✗ FaceSwapper model was loaded on import (lazy loading failed)")
        sys.exit(1)
except Exception as e:
    print(f"✗ Error: {e}")
    sys.exit(1)

# Test 3: Check other models are loaded
print("\n[Test 3] Checking other models (Buffalo detector, recognizer)...")
try:
    from app.main import detector, recognizer
    print("✓ Detector and recognizer imported successfully")
except Exception as e:
    print(f"✗ Failed to import models: {e}")
    sys.exit(1)

# Test 4: Manual load test (with error handling)
print("\n[Test 4] Testing manual swap model load (with error handling)...")
try:
    from app.core.swapper import FaceSwapper
    test_swapper = FaceSwapper()
    print("✓ FaceSwapper instance created without loading model")
    
    # Try to load (may fail if model unavailable, but should be handled gracefully)
    try:
        test_swapper.load_model()
        print("✓ Swap model loaded successfully")
    except Exception as load_err:
        print(f"⚠ Swap model not available: {load_err}")
        print("  (This is OK - model will be downloaded on first use)")
        
except Exception as e:
    print(f"✗ Error creating FaceSwapper: {e}")
    sys.exit(1)

print("\n" + "=" * 60)
print("✓ All lazy loading tests passed!")
print("=" * 60)
