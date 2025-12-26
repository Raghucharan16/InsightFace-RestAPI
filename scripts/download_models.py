import os
import urllib.request
import zipfile

# Define paths
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
MODELS = os.path.join(ROOT, "models")
BUFFALO_DIR = os.path.join(MODELS, "buffalo_l")
os.makedirs(BUFFALO_DIR, exist_ok=True)

# 1. Download InSwapper
print("Downloading Swapper...")
urllib.request.urlretrieve(
    "https://huggingface.co/deepinsight/inswapper/resolve/main/inswapper_128.onnx",
    os.path.join(MODELS, "inswapper_128.onnx")
)

# 2. Download Buffalo_L Zip (contains w600k_r50.onnx and det_10g.onnx)
print("Downloading Buffalo_L...")
zip_path = os.path.join(MODELS, "buffalo_l.zip")
urllib.request.urlretrieve(
    "https://github.com/deepinsight/insightface/releases/download/v0.7/buffalo_l.zip",
    zip_path
)

with zipfile.ZipFile(zip_path, 'r') as z:
    z.extractall(BUFFALO_DIR)