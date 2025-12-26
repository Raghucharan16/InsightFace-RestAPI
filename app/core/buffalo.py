import os
import numpy as np
from numpy.typing import NDArray
from typing import Any, List, Union
from insightface.model_zoo import get_model
from app.utils import download_weights_if_necessary
from app.core.base import FacialRecognition

class Buffalo_L(FacialRecognition):
    def __init__(self) -> None:
        self.model = None
        self.input_shape = (112, 112)
        self.output_shape = 512
        self.load_model()

    def load_model(self) -> None:
        sub_dir = "buffalo_l"
        model_file = "w600k_r50.onnx" # The recognition model in buffalo_l pack
        model_rel_path = os.path.join(sub_dir, model_file)

        # Direct link to the ONNX file if available, or the zip
        # This is a placeholder link; usually these come in the zip pack
        url = "https://github.com/deepinsight/insightface/releases/download/v0.7/buffalo_l.zip"
        
        weights_path = download_weights_if_necessary(model_rel_path, url)

        self.model = get_model(weights_path, providers=['CPUExecutionProvider'])
        self.model.prepare(ctx_id=-1)

    def preprocess(self, img: NDArray[Any]) -> NDArray[Any]:
        if len(img.shape) == 3:
            img = np.expand_dims(img, axis=0)
        img = img[:, :, :, ::-1] # RGB to BGR
        return img

    def forward(self, img: NDArray[Any]) -> Union[List[float], List[List[float]]]:
        # img here expects a 112x112 aligned face crop, not a full raw image
        img = self.preprocess(img)
        batch_size = img.shape[0]
        embeddings = []
        for i in range(batch_size):
            embedding = self.model.get_feat(img[i])
            embeddings.append(embedding.flatten().tolist())
        return embeddings[0] if batch_size == 1 else embeddings