import os
import inspireface as isf
from app.utils import get_weights_dir
from app.core.base import FacialRecognition

class InspireFaceWrapper(FacialRecognition):
    def __init__(self):
        self.session = None
        self.load_model()

    def load_model(self) -> None:
        # Ensure the resource pack exists (downloaded via script)
        models_dir = get_weights_dir()
        pack_path = os.path.join(models_dir, "InspireFace_Pikachu")
        
        if not os.path.exists(pack_path):
            raise FileNotFoundError(f"InspireFace pack not found at {pack_path}")

        # CPU Configuration
        self.session = isf.InspireFaceSession(
            opt=isf.HF_ENABLE_NONE, 
            detect_mode=isf.HF_DETECT_MODE_ALWAYS_DETECT
        )
        self.session.load_resource(pack_path)

    def forward(self, img):
        # InspireFace expects raw image data
        return self.session.face_detection(img)

    def get_features(self, img):
        # Full pipeline: Detect -> Analyze
        faces = self.session.face_detection(img)
        results = []
        for face in faces:
            feature = self.session.face_feature_extract(face)
            results.append(feature)
        return results