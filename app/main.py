from fastapi import FastAPI, UploadFile, File, HTTPException
import cv2
import numpy as np
from app.core.buffalo import Buffalo_L
from app.core.detector import Buffalo_S_Detector
from app.core.swapper import FaceSwapper
# from app.core.inspire import InspireFaceWrapper # Uncomment if resource pack is present

app = FastAPI(title="InsightFace & InspireFace API")

# Initialize models globally (lazy loading recommended for production)
detector = Buffalo_S_Detector()
recognizer = Buffalo_L()
swapper = FaceSwapper()

def read_image(file: UploadFile):
    contents = file.file.read()
    nparr = np.frombuffer(contents, np.uint8)
    img = cv2.imdecode(nparr, cv2.IMREAD_COLOR)
    return img

@app.post("/recognition/embedding")
async def get_embedding(file: UploadFile = File(...)):
    img = read_image(file)
    
    # 1. Detect
    dets = detector.forward(img)
    bboxes, kpss = dets
    
    if len(kpss) == 0:
        return {"error": "No face detected"}

    # 2. Align & Crop (Simplified logic, usually you need affine transform here)
    # For this demo, we assume the user might send a cropped 112x112 or we take raw
    # Proper InsightFace alignment uses face_align.norm_crop(img, kps)
    from insightface.utils import face_align
    aligned_face = face_align.norm_crop(img, kpss[0])
    
    # 3. Recognize
    emb = recognizer.forward(aligned_face)
    return {"embedding": emb}

@app.post("/swap")
async def swap_faces(source: UploadFile = File(...), target: UploadFile = File(...)):
    source_img = read_image(source)
    target_img = read_image(target)

    # 1. Get Source Face (need embedding)
    src_dets = detector.forward(source_img)
    if len(src_dets[1]) == 0: raise HTTPException(400, "No source face")
    
    # Construct a Mock Face Object for the swapper (it needs .embedding and .kps)
    # In a full impl, use a Face() class structure
    from insightface.app.common import Face
    from insightface.utils import face_align
    
    # Process Source
    src_kps = src_dets[1][0]
    src_align = face_align.norm_crop(source_img, src_kps)
    src_emb = recognizer.forward(src_align)
    
    source_face_obj = Face(bbox=src_dets[0][0], kps=src_kps, embedding=np.array(src_emb))

    # 2. Get Target Face
    tgt_dets = detector.forward(target_img)
    if len(tgt_dets[1]) == 0: raise HTTPException(400, "No target face")
    target_face_obj = Face(bbox=tgt_dets[0][0], kps=tgt_dets[1][0], embedding=None)

    # 3. Swap
    result = swapper.swap(source_face_obj, target_img, target_face_obj)

    # Return image (encode to jpg)
    _, im_png = cv2.imencode(".png", result)
    return Response(content=im_png.tobytes(), media_type="image/png")