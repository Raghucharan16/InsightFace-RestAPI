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

def download_weights_if_necessary(file_name: str, source_url: str, skip_download: bool = False) -> str:
    """
    Download weights if necessary, with option to skip if file is optional.
    
    Args:
        file_name: Name of the file to download
        source_url: URL to download from
        skip_download: If True, don't raise error if download fails (for optional models)
    
    Returns:
        Path to the model file
    """
    models_dir = get_weights_dir()
    # Handle subdirectories (e.g buffalo_l/model.onnx)
    target_path = os.path.join(models_dir, file_name)
    target_dir = os.path.dirname(target_path)
    
    if not os.path.exists(target_dir):
        os.makedirs(target_dir, exist_ok=True)

    # If file already exists, return it
    if os.path.exists(target_path):
        file_size = os.path.getsize(target_path)
        if file_size > 0:
            return target_path
        else:
            # File exists but is empty, remove it
            os.remove(target_path)

    logger.info(f"Downloading {file_name} from {source_url}...")
    try:
        # Add headers to avoid 401 errors
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
        }
        request = urllib.request.Request(source_url, headers=headers)
        
        with urllib.request.urlopen(request, timeout=60) as response:
            with open(target_path, 'wb') as f:
                f.write(response.read())
        
        logger.info(f"Download completed: {file_name}")
        return target_path
        
    except Exception as e:
        logger.error(f"Failed to download {file_name}: {e}")
        
        # Clean up partial file
        if os.path.exists(target_path):
            os.remove(target_path)
        
        # If this is an optional model, don't raise error
        if skip_download:
            logger.warning(f"Skipping {file_name} (optional model)")
            return None
        
        raise e