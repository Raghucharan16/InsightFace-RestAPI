import os
import cv2
import numpy as np
from insightface.model_zoo import get_model
from app.utils import download_weights_if_necessary
from app.core.base import FacialRecognition

class Buffalo_S_Detector(FacialRecognition):
    def __init__(self):
        self.model = None
        self.input_shape = (640, 640)
        self.load_model()

    def load_model(self) -> None:
        # SCRFD 10G KPS (Keypoints) is part of buffalo_l/s pack
        # We download just the detection model
        model_file = "det_10g.onnx"
        sub_dir = "buffalo_l"
        rel_path = os.path.join(sub_dir, model_file)
        
        # Using a public mirror for the buffalo_l detection model
        url = "https://github.com/deepinsight/insightface/releases/download/v0.7/buffalo_l.zip"
        # Note: In a real app, unzip the pack. For simplicity, assuming file exists 
        # or logic in download script handles zips.
        
        # For this specific class, we assume the user puts the .onnx there 
        # or we use the standard insightface auto-loader.
        # To match your specific class style, we load the ONNX directly.
        
        weights_path = download_weights_if_necessary(rel_path, url) 
        
        # providers=['CPUExecutionProvider'] forces CPU
        self.model = get_model(weights_path, providers=['CPUExecutionProvider'])
        self.model.prepare(ctx_id=-1, input_size=self.input_shape, det_thresh=0.5)

    def forward(self, img: np.ndarray):
        # Returns list of Face objects with bbox and kps
        detections = self.model.detect(img, max_num=0, metric='default')
        # detections is a tuple (bboxes, kpss)
        return detections