import os
import numpy as np
import cv2
from typing import Any
from insightface.model_zoo import get_model
from app.utils import download_weights_if_necessary
from app.core.base import FacialRecognition

class FaceSwapper(FacialRecognition):
    def __init__(self) -> None:
        self.model = None
        self._model_loaded = False
        self.model_file = "inswapper_128.onnx"
        self.url = "https://huggingface.co/deepinsight/inswapper/resolve/main/inswapper_128.onnx"

    def load_model(self) -> None:
        """Load model on demand (lazy loading)"""
        if self._model_loaded:
            return
        
        try:
            weights_path = download_weights_if_necessary(self.model_file, self.url)
            self.model = get_model(weights_path, providers=['CPUExecutionProvider'])
            self._model_loaded = True
        except Exception as e:
            raise RuntimeError(f"Failed to load FaceSwapper model: {e}")

    def forward(self, img: Any) -> Any:
        # Not used in swapper standard flow
        pass

    def swap(self, source_face, target_img, target_face):
        """
        source_face: InsightFace object of source (must have embedding)
        target_img: CV2 image (numpy array)
        target_face: InsightFace object of target (must have kps)
        """
        # Ensure model is loaded before swapping
        if not self._model_loaded:
            self.load_model()
        
        # Execute swap
        res_img = self.model.get(target_img, target_face, source_face, paste_back=True)
        return res_img