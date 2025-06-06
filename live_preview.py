# live_preview.py
import streamlit as st
from streamlit_webrtc import webrtc_streamer
import av

st.title("🎥 실시간 카메라 미리보기")

def video_frame_callback(frame):
    img = frame.to_ndarray(format="bgr24")  # OpenCV 스타일로 변환
    return av.VideoFrame.from_ndarray(img, format="bgr24")

webrtc_streamer(
    key="camera",
    video_frame_callback=video_frame_callback,
    media_stream_constraints={"video": True, "audio": False}
)
