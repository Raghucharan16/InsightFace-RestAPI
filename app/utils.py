import os
import urllib.request
from logging import getLogger

logger = getLogger("insightface_api")

def get_weights_dir():
    # Returns absolute path to 'models' folder in project root
    root_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    models_dir = os.path.join(root_dir, "models")
    os.makedirs(models_dir, exist_ok=True)
    return models_dir

def download_weights_if_necessary(file_name: str, source_url: str) -> str:
    models_dir = get_weights_dir()
    # Handle subdirectories (e.g. buffalo_l/model.onnx)
    target_path = os.path.join(models_dir, file_name)
    target_dir = os.path.dirname(target_path)
    
    if not os.path.exists(target_dir):
        os.makedirs(target_dir, exist_ok=True)

    if os.path.exists(target_path):
        return target_path

    logger.info(f"Downloading {file_name} from {source_url}...")
    try:
        urllib.request.urlretrieve(source_url, target_path)
        logger.info("Download completed.")
    except Exception as e:
        logger.error(f"Failed to download: {e}")
        if os.path.exists(target_path):
            os.remove(target_path)
        raise e
        
    return target_path