import cv2
import os
import uuid
from codeformer.app import inference_app
import insightface
from insightface.app import FaceAnalysis

class FaceSwapper:
    def __init__(self):
        self.app = FaceAnalysis(name='buffalo_l',root='~/.insightface')
        self.app.prepare(ctx_id=0, det_size=(640, 640))

        self.swapper = insightface.model_zoo.get_model(
            "models/inswapper_128.onnx",
            download=False
        )

    def _import_cv2():
        import cv2
        return cv2
    
    def load_image(self, path):
        cv2 = self._import_cv2()
        img = cv2.imread(path)
        return cv2.cvtColor(img, cv2.COLOR_BGR2RGB)

    def get_faces(self, img):
        return self.app.get(img)

    def swap_faces(self, source_img, target_img):
        source_faces = self.get_faces(source_img)
        target_faces = self.get_faces(target_img)

        if len(target_faces) == 0:
            raise ValueError("No face detected in target image")

        target_face = target_faces[0]
        result = source_img.copy()

        for face in source_faces:
            result = self.swapper.get(
                result,
                face,
                target_face,
                paste_back=True
            )

        return result

class FaceEnhancer:
    def __init__(self):
        os.makedirs("temp/codeformer", exist_ok=True)

    def _import_cv2():
        import cv2
        return cv2

    def enhance(self, img_rgb, fidelity=0.7):
        # Convert to BGR
        cv2 = self._import_cv2()
        img_bgr = cv2.cvtColor(img_rgb, cv2.COLOR_RGB2BGR)

        # Write temp input
        input_path = f"temp/codeformer/in_{uuid.uuid4().hex}.png"
        output_path = "output/out.png"  # CodeFormer hardcodes this

        cv2.imwrite(input_path, img_bgr)

        # Call CodeFormer (expects PATH)
        restored_path = inference_app(
            input_path,
            background_enhance=False,
            face_upsample=True,
            upscale=1,
            codeformer_fidelity=fidelity
        )

        # Read restored image
        restored_bgr = cv2.imread(restored_path)
        restored_rgb = cv2.cvtColor(restored_bgr, cv2.COLOR_BGR2RGB)

        return restored_rgb


