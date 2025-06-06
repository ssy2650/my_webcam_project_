# app.py
import streamlit as st
import cv2
import numpy as np
import mediapipe as mp
from PIL import Image
import tempfile

st.title("🧑‍💻 가상 배경 프로그램 (MediaPipe)")

# 파일 업로드
video_file = st.file_uploader("🎥 영상 파일 업로드 (.mp4)", type=["mp4"])
bg_file = st.file_uploader("🖼 배경 이미지 업로드", type=["jpg", "png"])

if video_file and bg_file:
    # 임시 파일로 저장
    tfile = tempfile.NamedTemporaryFile(delete=False)
    tfile.write(video_file.read())
    video_path = tfile.name

    bg = Image.open(bg_file).convert("RGB")

    # MediaPipe 초기화
    mp_selfie_segmentation = mp.solutions.selfie_segmentation
    segmentor = mp_selfie_segmentation.SelfieSegmentation(model_selection=1)

    stframe = st.empty()
    cap = cv2.VideoCapture(video_path)

    while cap.isOpened():
        ret, frame = cap.read()
        if not ret:
            break

        frame = cv2.resize(frame, (640, 360))
        bg_resized = cv2.resize(np.array(bg), (640, 360))

        rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        results = segmentor.process(rgb)
        condition = results.segmentation_mask > 0.5

        output = np.where(condition[..., None], frame, bg_resized)
        stframe.image(output, channels="BGR")

    cap.release()
