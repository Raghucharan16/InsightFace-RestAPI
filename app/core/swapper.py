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
        self.load_model()

    def load_model(self) -> None:
        model_file = "inswapper_128.onnx"
        # Direct Google Drive Link or mirror for inswapper
        url = "https://huggingface.co/deepinsight/inswapper/resolve/main/inswapper_128.onnx"
        
        weights_path = download_weights_if_necessary(model_file, url)
        
        self.model = get_model(weights_path, providers=['CPUExecutionProvider'])
        # Swapper doesn't need explicit prepare with size, it handles 128x128 internally

    def forward(self, img: Any) -> Any:
        # Not used in swapper standard flow
        pass

    def swap(self, source_face, target_img, target_face):
        """
        source_face: InsightFace object of source (must have embedding)
        target_img: CV2 image (numpy array)
        target_face: InsightFace object of target (must have kps)
        """
        # Execute swap
        res_img = self.model.get(target_img, target_face, source_face, paste_back=True)
        return res_img