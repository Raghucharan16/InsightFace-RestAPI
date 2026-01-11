import cv2
import os
from tqdm import tqdm

def process_video(
    video_path,
    output_path,
    swapper,
    target_img
):
    cap = cv2.VideoCapture(video_path)

    fps = cap.get(cv2.CAP_PROP_FPS)
    w = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
    h = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))

    out = cv2.VideoWriter(
        output_path,
        cv2.VideoWriter_fourcc(*"mp4v"),
        fps,
        (w, h)
    )

    while cap.isOpened():
        ret, frame = cap.read()
        if not ret:
            break

        frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        swapped = swapper.swap_faces(frame_rgb, target_img)
        swapped_bgr = cv2.cvtColor(swapped, cv2.COLOR_RGB2BGR)

        out.write(swapped_bgr)

    cap.release()
    out.release()
