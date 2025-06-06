import cv2
import torch
import numpy as np
from PIL import Image
from torchvision import transforms
from model.u2net import U2NETP
import sys
from datetime import datetime
import os
import sys

bg_path = sys.argv[1]

if not bg_path:
    print("❌ 배경 이미지 경로를 선택하지 않았습니다.")
    exit()


# 배경 이미지 경로를 외부 인자로 받기
if len(sys.argv) < 2:
    print("❌ 배경 이미지 경로를 인자로 전달하세요.")
    exit()

background_img = cv2.imread(bg_path)
if background_img is None:
    print("❌ 배경 이미지를 불러올 수 없습니다.")
    exit()

# 모델 로드
net = U2NETP(3, 1)
net.load_state_dict(torch.load('./saved_models/u2net/u2netp.pth', map_location='cpu'))
net.eval()


# mp4 동영상 파일 :
cap = cv2.VideoCapture("sample.mp4")


if not cap.isOpened():
    print("❌ 영상 파일을 열 수 없습니다.")
    exit()

transform = transforms.Compose([
    transforms.Resize((224, 224)),
    transforms.ToTensor(),
])

cv2.namedWindow("Virtual Background", cv2.WINDOW_NORMAL)
cv2.resizeWindow("Virtual Background", 800, 450)

frame_count = 0

# 첫 프레임으로 영상 크기 측정
ret, frame = cap.read()
frame = cv2.resize(frame, (480, 270))
h, w, _ = frame.shape

# 자동 저장 경로 및 이름
timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
output_path = f"2. 이미지합성 날짜기록_{timestamp}.mp4"
out = cv2.VideoWriter(output_path, cv2.VideoWriter_fourcc(*'mp4v'), 20, (w, h))
print(f"✅ 영상이 저장됩니다: {output_path}")

# 영상 처음부터 다시 읽게 설정
cap.set(cv2.CAP_PROP_POS_FRAMES, 0)


while True:
    ret, frame = cap.read()
    if not ret:
        break

    frame = cv2.resize(frame, (480, 270))  # 프레임 축소
    frame_count += 1
    if frame_count % 2 != 0:
        continue

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
    cv2.imshow("Virtual Background", blended)
    out.write(blended)

    if cv2.waitKey(8) & 0xFF == ord('q'):
        break

cap.release()
out.release()
cv2.destroyAllWindows()
