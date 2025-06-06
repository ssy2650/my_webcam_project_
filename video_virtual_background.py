import cv2
import torch
import numpy as np
from PIL import Image
from torchvision import transforms
from model.u2net import U2NETP  # 또는 U2NET
import os

# 모델 로드
model_path = './saved_models/u2net/u2netp.pth'
net = U2NETP(3, 1)
net.load_state_dict(torch.load(model_path, map_location='cpu'))
net.eval()

# 배경 이미지 불러오기
background_img = cv2.imread("background.jpg")
if background_img is None:
    print("❌ background.jpg 파일을 찾을 수 없습니다.")
    exit()

# 영상 열기
cap = cv2.VideoCapture(0)
# cap = cv2.VideoCapture("sample.mp4")
if not cap.isOpened():
    print("❌ 웹캠을 열 수 없습니다.")
    exit()

cv2.namedWindow("U2Net Virtual Background", cv2.WINDOW_NORMAL)
cv2.resizeWindow("U2Net Virtual Background", 960, 540)

# 변환 함수 정의
transform = transforms.Compose([
    transforms.Resize((192, 192)),
    transforms.ToTensor(),
])

frame_count = 0
while True:
    ret, frame = cap.read()
    if not ret:
        break

    frame_count += 1
    if frame_count % 3 != 0:  # 3프레임 중 1프레임만 처리 (너무 렉 걸려서)
        continue  

    h, w, _ = frame.shape
    background = cv2.resize(background_img, (w, h))

    # PIL 변환
    pil_frame = Image.fromarray(cv2.cvtColor(frame, cv2.COLOR_BGR2RGB))
    input_tensor = transform(pil_frame).unsqueeze(0)

    # 추론
    with torch.no_grad():
        d1, *_ = net(input_tensor)

    # 마스크 후처리
    mask = d1[0][0].cpu().numpy()
    mask = (mask - mask.min()) / (mask.max() - mask.min())
    mask = cv2.resize(mask, (w, h))

    # 경계 부드럽게 처리 + 팔 잘림 방지
    mask = cv2.GaussianBlur(mask, (9, 9), 0)
    mask = np.clip(mask, 0, 1)

    # dilation (경계 확장 위해 커널 생성)
    kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (15, 15))
    mask = cv2.dilate(mask, kernel, iterations=1)

    # 다시 부드럽게
    mask = np.clip(mask, 0, 1)

    # 3채널 마스크 생성 및 합성
    mask_3ch = np.stack([mask]*3, axis=-1)
    blended = (frame * mask_3ch + background * (1 - mask_3ch)).astype(np.uint8)

    # . 실시간 출력 및 종료 조건
    cv2.imshow("U2Net Virtual Background", blended)
    if cv2.waitKey(8) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
