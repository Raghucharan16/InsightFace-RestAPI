import os
import urllib.request
import zipfile
import time
import ssl
import hashlib

# Define paths
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
MODELS = os.path.join(ROOT, "models")
BUFFALO_DIR = os.path.join(MODELS, "buffalo_l")
PIKACHU_DIR = os.path.join(MODELS, "pikachu")
MEGATRON_DIR = os.path.join(MODELS, "megatron")

os.makedirs(BUFFALO_DIR, exist_ok=True)
os.makedirs(PIKACHU_DIR, exist_ok=True)
os.makedirs(MEGATRON_DIR, exist_ok=True)

# Model configurations - Using InspireFace OSS direct URLs
INSPIREFACE_MODELS = {
    "Pikachu": {
        "url": "https://inspireface-1259028827.cos.ap-singapore.myqcloud.com/inspireface_modelzoo/t4/Pikachu",
        "filename": "Pikachu",
    },
    "Megatron": {
        "url": "https://inspireface-1259028827.cos.ap-singapore.myqcloud.com/inspireface_modelzoo/t4/Megatron",
        "filename": "Megatron",
    }
}


def get_file_md5(filepath):
    """Calculate MD5 hash of a file"""
    md5_hash = hashlib.md5()
    with open(filepath, 'rb') as f:
        for chunk in iter(lambda: f.read(4096), b''):
            md5_hash.update(chunk)
    return md5_hash.hexdigest()

def download_file(url, filepath, expected_md5=None, max_retries=3):
    """Download file with retry logic, proper headers, and MD5 verification"""
    for attempt in range(max_retries):
        try:
            print(f"\n📥 Downloading from: {url}")
            print(f"   Saving to: {filepath} (attempt {attempt + 1}/{max_retries})...")
            
            # Create SSL context (ignore certificate verification for OSS)
            ssl_context = ssl.create_default_context()
            ssl_context.check_hostname = False
            ssl_context.verify_mode = ssl.CERT_NONE
            
            # Create request with proper headers
            headers = {
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
            }
            request = urllib.request.Request(url, headers=headers)
            
            with urllib.request.urlopen(request, context=ssl_context, timeout=300) as response:
                total_size = int(response.headers.get('content-length', 0))
                block_size = 8192
                downloaded_size = 0
                
                with open(filepath, 'wb') as f:
                    while True:
                        buffer = response.read(block_size)
                        if not buffer:
                            break
                        downloaded_size += len(buffer)
                        f.write(buffer)
                        
                        if total_size > 0:
                            percent = (downloaded_size / total_size) * 100
                            mb_downloaded = downloaded_size / (1024 * 1024)
                            mb_total = total_size / (1024 * 1024)
                            print(f"   Progress: {percent:.1f}% ({mb_downloaded:.1f}MB / {mb_total:.1f}MB)", end='\r')
            
            # Check if file is actually downloaded (has content)
            file_size = os.path.getsize(filepath)
            if file_size == 0:
                print(f"\n✗ Downloaded file is empty (0 bytes)")
                os.remove(filepath)
                if attempt < max_retries - 1:
                    print(f"   Retrying with different source...")
                    time.sleep(2 ** attempt)
                continue
            
            print(f"\n✓ Download completed ({file_size / (1024*1024):.1f}MB)")
            
            # Verify MD5 if provided
            if expected_md5:
                print(f"🔐 Verifying MD5 hash...")
                actual_md5 = get_file_md5(filepath)
                if actual_md5.lower() == expected_md5.lower():
                    print(f"✓ MD5 verification passed")
                    return True
                else:
                    print(f"✗ MD5 mismatch!")
                    print(f"   Expected: {expected_md5}")
                    print(f"   Got:      {actual_md5}")
                    os.remove(filepath)
                    if attempt < max_retries - 1:
                        print(f"   Retrying download...")
                        time.sleep(2 ** attempt)
                    continue
            
            return True
            
        except urllib.error.HTTPError as e:
            print(f"\n✗ HTTP Error {e.code}: {e.reason}")
            if attempt < max_retries - 1:
                print(f"   Retrying in {2**attempt}s...")
                time.sleep(2 ** attempt)
        except Exception as e:
            print(f"\n✗ Error: {e}")
            if attempt < max_retries - 1:
                print(f"   Retrying in {2**attempt}s...")
                time.sleep(2 ** attempt)
    
    print(f"✗ Failed to download after {max_retries} attempts")
    if os.path.exists(filepath):
        os.remove(filepath)
    return False

def download_and_extract_zip(model_name, urls, extract_dir):
    """Download and extract a zip file, trying multiple URLs"""
    zip_path = os.path.join(MODELS, f"{model_name}.zip")
    
    # Check if already extracted
    if os.path.exists(extract_dir) and os.listdir(extract_dir):
        print(f"✓ {model_name} already extracted, skipping download")
        return True
    
    # Try each URL
    for idx, url in enumerate(urls):
        print(f"\n   Trying source {idx + 1}/{len(urls)}...")
        if download_file(url, zip_path):
            try:
                print(f"📦 Extracting {model_name}.zip to {extract_dir}...")
                with zipfile.ZipFile(zip_path, 'r') as z:
                    z.extractall(extract_dir)
                print(f"✓ Successfully extracted {model_name}")
                os.remove(zip_path)
                return True
            except Exception as e:
                print(f"✗ Error extracting: {e}")
                if os.path.exists(zip_path):
                    os.remove(zip_path)
                continue
    
    return False

def download_model_file(model_name, url, target_dir):
    """Download a model file directly to target directory"""
    model_path = os.path.join(target_dir, model_name)
    
    # Check if already downloaded
    if os.path.exists(model_path):
        file_size = os.path.getsize(model_path)
        if file_size > 0:
            print(f"✓ {model_name} already exists ({file_size / (1024*1024):.1f}MB), skipping")
            return True
    
    # Create temp file path for download
    temp_path = model_path + ".tmp"
    
    if download_file(url, temp_path):
        # Check file size
        file_size = os.path.getsize(temp_path)
        if file_size > 0:
            # Move temp file to final location
            if os.path.exists(model_path):
                os.remove(model_path)
            os.rename(temp_path, model_path)
            print(f"✓ {model_name} saved successfully ({file_size / (1024*1024):.1f}MB)")
            return True
        else:
            print(f"✗ Downloaded file is empty")
            if os.path.exists(temp_path):
                os.remove(temp_path)
            return False
    
    if os.path.exists(temp_path):
        os.remove(temp_path)
    return False

# ========== INSIGHTFACE MODELS ==========
print("=" * 70)
print("DOWNLOADING INSIGHTFACE MODELS")
print("=" * 70)

# 1. Download Pikachu Model (Lightweight)
print("\n[1/3] Pikachu Model (Lightweight - ~50MB)...")
if "Pikachu" in INSPIREFACE_MODELS:
    model_info = INSPIREFACE_MODELS["Pikachu"]
    download_model_file(model_info["filename"], model_info["url"], PIKACHU_DIR)
else:
    print("⚠️  Pikachu model configuration not found")

# 2. Download Megatron Model (Full-featured)
print("\n[2/3] Megatron Model (Full-featured - ~300MB)...")
if "Megatron" in INSPIREFACE_MODELS:
    model_info = INSPIREFACE_MODELS["Megatron"]
    download_model_file(model_info["filename"], model_info["url"], MEGATRON_DIR)
else:
    print("⚠️  Megatron model configuration not found")

# ========== DEEPINSIGHT INSIGHTFACE MODELS ==========
print("\n" + "=" * 70)
print("DOWNLOADING DEEPINSIGHT INSIGHTFACE MODELS")
print("=" * 70)

# 3. Download Buffalo_L Model
print("\n[3/3] Buffalo_L Model (DeepInsight)...")
buffalo_zip_path = os.path.join(MODELS, "buffalo_l.zip")

if os.path.exists(BUFFALO_DIR) and os.listdir(BUFFALO_DIR):
    print(f"✓ {BUFFALO_DIR} already exists with files, skipping download")
else:
    buffalo_url = "https://github.com/deepinsight/insightface/releases/download/v0.7/buffalo_l.zip"
    if download_file(buffalo_url, buffalo_zip_path):
        try:
            print("📦 Extracting buffalo_l.zip...")
            with zipfile.ZipFile(buffalo_zip_path, 'r') as z:
                z.extractall(BUFFALO_DIR)
            print("✓ Successfully extracted buffalo_l.zip")
            os.remove(buffalo_zip_path)
        except Exception as e:
            print(f"✗ Error extracting: {e}")

# ========== OPTIONAL: Face Swap Model ==========
print("\n" + "=" * 70)
print("OPTIONAL: FACE SWAP MODEL")
print("=" * 70)

print("\n[Optional] InSwapper Model (Face Swap - 530MB)...")
inswapper_path = os.path.join(MODELS, "inswapper_128.onnx")

if os.path.exists(inswapper_path):
    file_size = os.path.getsize(inswapper_path)
    if file_size > 0:
        print(f"✓ InSwapper model already exists ({file_size / (1024*1024):.1f}MB)")
    else:
        print("⚠️  InSwapper file exists but is empty")
else:
    print("ℹ️  InSwapper model is optional and requires ~530MB")
    print("   Skipping automatic download to save bandwidth.")
    print("   If needed, download manually from:")
    print("   https://huggingface.co/deepinsight/inswapper/resolve/main/inswapper_128.onnx")

print("\n" + "=" * 70)
print("✓ MODEL DOWNLOAD PROCESS COMPLETED!")
print("=" * 70)
print("\nModel Directory Structure:")
print(f"  models/")
print(f"    ├── pikachu/              (Lightweight model)")
print(f"    ├── megatron/             (Full-featured model)")
print(f"    ├── buffalo_l/            (Face detection & recognition)")
print(f"    └── inswapper_128.onnx    (Optional: Face swap)")
print("\nIf models are still missing:")
print("1. Check your internet connection and firewall")
print("2. Try downloading manually from the URLs above")
print("3. Extract and place files in the corresponding directories")