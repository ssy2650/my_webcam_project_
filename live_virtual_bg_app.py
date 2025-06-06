import cv2
import numpy as np
import streamlit as st
from PIL import Image
from streamlit_webrtc import webrtc_streamer, VideoProcessorBase
import mediapipe as mp
import os

st.set_page_config(page_title="실시간 가상 배경", layout="centered")
st.title("🎥 실시간 가상 배경 (MediaPipe + Streamlit)")

# 👉 모드 선택: 배경 이미지 / 흐림 배경
mode = st.radio("모드 선택", ["배경 이미지 모드", "배경 흐림 모드"])

# 👉 배경 이미지 선택 (이미지 모드일 때만 표시)
bg_np = None
if mode == "배경 이미지 모드":
    BACKGROUND_DIR = "backgrounds"
    image_files = [f for f in os.listdir(BACKGROUND_DIR) if f.endswith((".jpg", ".png"))]

    if image_files:
        selected_image = st.selectbox("📂 배경 이미지 선택", image_files)
        bg_path = os.path.join(BACKGROUND_DIR, selected_image)
        bg_img = Image.open(bg_path).convert("RGB")
        bg_np = np.array(bg_img)
    else:
        st.warning("❌ 배경 이미지가 없습니다. backgrounds 폴더에 추가해 주세요.")
        st.stop()

# 📸 카메라 ON/OFF
camera_on = st.toggle("📷 카메라 ON", value=False)

if camera_on:
    class VirtualProcessor(VideoProcessorBase):
        def __init__(self):
            self.segmentor = mp.solutions.selfie_segmentation.SelfieSegmentation(model_selection=1)

        def transform(self, frame):
            img = frame.to_ndarray(format="bgr24")
            h, w, _ = img.shape

            # 사람 분리 마스크
            rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
            results = self.segmentor.process(rgb)
            mask = results.segmentation_mask > 0.3

            # 마스크 후처리
            mask = mask.astype(np.uint8) * 255
            mask = cv2.GaussianBlur(mask, (15, 15), 0)
            mask = mask > 127
            kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (7, 7))
            mask = cv2.dilate(mask.astype(np.uint8), kernel, iterations=2)
            mask = mask > 0
            mask_3ch = np.stack((mask,) * 3, axis=-1)

            # 모드별 배경 처리
            if mode == "배경 이미지 모드" and bg_np is not None:
                bg_resized = cv2.resize(bg_np, (w, h))
                output = np.where(mask_3ch, img, bg_resized)
            else:  # 흐림 배경 모드
                blurred = cv2.GaussianBlur(img, (51, 51), 0)
                output = np.where(mask_3ch, img, blurred)

            return output

    webrtc_streamer(
        key="virtual-bg",
        video_processor_factory=VirtualProcessor,
        media_stream_constraints={"video": True, "audio": False},
        async_processing=True
    )
else:
    st.info("📴 카메라가 꺼져 있습니다. ON으로 켜보세요.")
