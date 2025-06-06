import cv2
import numpy as np
import mediapipe as mp
import sys

# 배경 이미지 인자
if len(sys.argv) < 2:
    print("❌ 배경 이미지 경로를 전달하세요.")
    exit()

bg_path = sys.argv[1]
background_img = cv2.imread(bg_path)
if background_img is None:
    print("❌ 배경 이미지를 불러올 수 없습니다.")
    exit()

# MediaPipe 세그먼테이션 초기화
mp_selfie_segmentation = mp.solutions.selfie_segmentation
segmentor = mp_selfie_segmentation.SelfieSegmentation(model_selection=1)


# 웹캠 시작
cap = cv2.VideoCapture(0)
if not cap.isOpened():
    print("❌ 웹캠을 열 수 없습니다.")
    exit()

"""
# 영상 파일로 대체
cap = cv2.VideoCapture("sample.mp4")  
if not cap.isOpened():
    print("❌ sample.mp4 파일을 열 수 없습니다.")
    import os
    print("📂 현재 경로:", os.getcwd())
    print("📁 존재하는 파일 목록:", os.listdir())
    exit()
"""

cap = cv2.VideoCapture(0) 
# cap = cv2.VideoCapture("sample.mp4")  # 또는 웹캠: 0
if not cap.isOpened():
    print("❌ 웹캠을 열 수 없습니다.")
    exit()

# 영상 저장
ret, frame = cap.read()
frame = cv2.resize(frame, (640, 360))
h, w, _ = frame.shape

from datetime import datetime
timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
output_path = f"5. 미디어 파이프_mediapipe 날짜기록_{timestamp}.mp4"
out = cv2.VideoWriter(output_path, cv2.VideoWriter_fourcc(*'mp4v'), 20, (w, h))
print(f"✅ 저장 경로: {output_path}")

cap.set(cv2.CAP_PROP_POS_FRAMES, 0)



cv2.namedWindow("MediaPipe Background", cv2.WINDOW_NORMAL)
cv2.resizeWindow("MediaPipe Background", 800, 450)

while True:
    ret, frame = cap.read()
    if not ret:
        break

    frame = cv2.resize(frame, (640, 360))
    h, w, _ = frame.shape
    background = cv2.resize(background_img, (w, h))

    rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    results = segmentor.process(rgb)
    mask = results.segmentation_mask
    condition = mask > 0.3  # True: 사람, False: 배경

    output = np.where(condition[..., None], frame, background)
    cv2.imshow("MediaPipe Background", output)
    out.write(output)

    if cv2.waitKey(15) & 0xFF == ord('q'):
        break

cap.release()
out.release() 
cv2.destroyAllWindows()