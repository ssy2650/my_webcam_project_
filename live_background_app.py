import cv2
import numpy as np
import streamlit as st
from PIL import Image
from streamlit_webrtc import webrtc_streamer, VideoTransformerBase
import mediapipe as mp

st.title("🎥 실시간 가상 배경 (MediaPipe + Streamlit)")

col1, col2 = st.columns([1, 2])
with col1:
    camera_on = st.toggle("📸 카메라 ON", value=False)
with col2:
    uploaded_bg = st.file_uploader("🖼 배경 이미지 업로드", type=["jpg", "png"])


if camera_on and uploaded_bg:
    bg_img = Image.open(uploaded_bg).convert("RGB")
    bg_np = np.array(bg_img)

    class VirtualBackground(VideoTransformerBase):
        def __init__(self):
            self.segmentor = mp.solutions.selfie_segmentation.SelfieSegmentation(model_selection=1)

        def transform(self, frame):
            img = frame.to_ndarray(format="bgr24")
            h, w, _ = img.shape
            bg_resized = cv2.resize(bg_np, (w, h))

            rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
            results = self.segmentor.process(rgb)
            mask = results.segmentation_mask > 0.3
            cv2.imshow("Mask", (mask * 255).astype(np.uint8))
            output = np.where(mask[..., None], img, bg_resized)
            return output

    with st.container():
        webrtc_streamer(
            key="virtual-bg",
            video_processor_factory=VirtualBackground,
            media_stream_constraints={"video": True, "audio": False},
            async_processing=True
        )

if not uploaded_bg:
    st.warning("⬆ 배경 이미지를 먼저 업로드하세요.")

elif not camera_on:
    st.info("📷 카메라가 꺼져 있습니다.")