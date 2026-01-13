# InsightFace RestAPI + Streamlit Demo

This repository implements a **face swap & restoration web app** based on:

- **InsightFace** for face detection and 128×128 face swapping (inswapper)
- **CodeFormer** for face restoration/enhancement
- **Streamlit** UI for interactive deployment
- Works on **Local Streamlit**

---

## 📌 What it Does

✔ Replace faces in source image with face from target image  
✔ Support multiple faces in source  
✔ Optional face restoration via CodeFormer  
✔ Provides web UI for easy interaction  
✔ Designed for **Local Streamlit** deployment  

---

## 🧠 Features

| Feature | Status |
|---------|--------|
| Image face swapping | ✅ |
| Multi-face support | ✅ |
| Face restoration (CodeFormer) | ✅ |
| Video support | ⚠️ (CPU only; may be slow) |
| Streamlit support | ❌ (not used here) |
| Gradio web UI | ✅ |

---

## 📁 Repo Structure
```
InsightFace-RestAPI/
├── app.py # Gradio app entrypoint
├── face_swapper.py # Face swap + enhancer logic
├── restoration.py # CodeFormer restoration backend
├── video_utils.py # Video face swap utilities
├── requirements.txt
├── checkpoints/
│ └── inswapper_128.onnx # ONNX model for face swap
├── CodeFormer/ # CodeFormer model & weights
  └── CodeFormer/weights/

```
---

## 🚀 Quick Start

### 1. Clone Repository

```bash
git clone https://github.com/Raghucharan16/InsightFace-RestAPI.git
cd InsightFace-RestAPI
```
2. Install Dependencies
```
pip install -r requirements.txt
```
3. Download Models
You need the following models:

✔ InsightFace (inswapper)

inswapper_128.onnx
Place inside:
```
models/inswapper_128.onnx
```
✔ CodeFormer (weights)
Download and place:
```
CodeFormer/CodeFormer/weights/CodeFormer/codeformer.pth
CodeFormer/CodeFormer/weights/facelib/detection_Resnet50_Final.pth
CodeFormer/CodeFormer/weights/facelib/parsing_parsenet.pth
CodeFormer/CodeFormer/weights/realesrgan/RealESRGAN_x2plus.pth
Tip: Use Git LFS for these weight files if pushing to GitHub.
```
💻 How to Run Locally
Start the Streamlit app:

```
streamlit run app.py
```

## Check this Huggingface Space if you don't want to setup:)
```
https://huggingface.co/spaces/VenkataRaghuCharan/FaceSwap
```
