import streamlit as st
import os
import cv2
from PIL import Image
import numpy as np

from face_swapper import FaceSwapper, FaceEnhancer
from video_utils import process_video

st.set_page_config(page_title="Face Swap App", layout="centered")

st.title("🔁 AI Face Swap (Image & Video)")

swapper = FaceSwapper()
enhancer = FaceEnhancer()
source_file = st.file_uploader(
    "Upload Source (Image or Video)",
    type=["jpg", "png", "jpeg", "mp4"]
)

target_file = st.file_uploader(
    "Upload Target Face Image",
    type=["jpg", "png", "jpeg"]
)

if source_file and target_file:
    os.makedirs("temp/input", exist_ok=True)
    os.makedirs("temp/output", exist_ok=True)

    source_path = f"temp/input/{source_file.name}"
    target_path = f"temp/input/{target_file.name}"

    with open(source_path, "wb") as f:
        f.write(source_file.read())

    with open(target_path, "wb") as f:
        f.write(target_file.read())

    target_img = swapper.load_image(target_path)

    if st.button("Start Face Swap"):
        with st.spinner("Processing..."):
            if source_file.type.startswith("image"):
                source_img = swapper.load_image(source_path)
                output = swapper.swap_faces(source_img, target_img)
                output = enhancer.enhance(output)
                output_path = "temp/output/result.jpg"
                Image.fromarray(output).save(output_path)

                st.image(output, caption="Swapped Image")
                st.download_button(
                    "Download Image",
                    open(output_path, "rb"),
                    file_name="face_swap.jpg"
                )

            else:
                output_video = "temp/output/result.mp4"
                process_video(
                    source_path,
                    output_video,
                    swapper,
                    enhancer,
                    target_img
                )

                st.video(output_video)
                st.download_button(
                    "Download Video",
                    open(output_video, "rb"),
                    file_name="face_swap.mp4"
                )
