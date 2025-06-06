import cv2
import torch
import numpy as np
from PIL import Image
from torchvision import transforms
from model.u2net import U2NETP
import sys

# 배경 이미지 경로 인자 받기
if len(sys.argv) < 2:
    print("❌ 배경 이미지 경로를 인자로 전달하세요.")
    exit()

bg_path = sys.argv[1]
background_img = cv2.imread(bg_path)
if background_img is None:
    print("❌ 배경 이미지를 불러올 수 없습니다.")
    exit()

# 모델 로드
net = U2NETP(3, 1)
net.load_state_dict(torch.load('./saved_models/u2net/u2netp.pth', map_location='cpu'))
net.eval()

# ✅ 웹캠 열기
cap = cv2.VideoCapture(0)
if not cap.isOpened():
    print("❌ 웹캠을 열 수 없습니다.")
    exit()

transform = transforms.Compose([
    transforms.Resize((224, 224)),
    transforms.ToTensor(),
])

# 첫 프레임에서 해상도 확인
ret, frame = cap.read()
frame = cv2.resize(frame, (480, 270))
h, w, _ = frame.shape


# 저장 : 자동 파일명 생성
from datetime import datetime

timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
output_path = f"3. 실시간 날짜기록_{timestamp}.mp4"  # 현재 폴더에 저장
out = cv2.VideoWriter(output_path, cv2.VideoWriter_fourcc(*'mp4v'), 20, (w, h))
print(f"✅ 영상이 저장됩니다: {output_path}")



cv2.namedWindow("Virtual Background (Live)", cv2.WINDOW_NORMAL)
cv2.resizeWindow("Virtual Background (Live)", 800, 450)

while True:
    ret, frame = cap.read()
    if not ret:
        break

    frame = cv2.resize(frame, (320, 180))
    h, w, _ = frame.shape
    background = cv2.resize(background_img, (w, h))

    pil = Image.fromarray(cv2.cvtColor(frame, cv2.COLOR_BGR2RGB))
    tensor = transform(pil).unsqueeze(0)

    with torch.no_grad():
        d1, *_ = net(tensor)

    mask = d1[0][0].cpu().numpy()
    mask = (mask - mask.min()) / (mask.max() - mask.min())
    mask = cv2.resize(mask, (w, h))
    mask = cv2.GaussianBlur(mask, (11, 11), 0)
    mask = np.clip(mask, 0, 1)
    mask_3ch = np.stack([mask]*3, axis=-1)

    blended = (frame * mask_3ch + background * (1 - mask_3ch)).astype(np.uint8)
    cv2.imshow("Virtual Background (Live)", blended)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
