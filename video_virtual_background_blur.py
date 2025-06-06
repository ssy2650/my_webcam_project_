import cv2
import torch
import numpy as np
from PIL import Image
from torchvision import transforms
from model.u2net import U2NETP

# 모델 로드
net = U2NETP(3, 1)
net.load_state_dict(torch.load('./saved_models/u2net/u2netp.pth', map_location='cpu'))
net.eval()

# 영상 열기
# cap = cv2.VideoCapture("sample.mp4")
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
output_path = f"4. 블러처리 날짜기록_{timestamp}.mp4"  # 현재 폴더에 저장
out = cv2.VideoWriter(output_path, cv2.VideoWriter_fourcc(*'mp4v'), 20, (w, h))
print(f"✅ 영상이 저장됩니다: {output_path}")


# ww다시 처음부터 시작
cap.set(cv2.CAP_PROP_POS_FRAMES, 0)

cv2.namedWindow("Blurred Background", cv2.WINDOW_NORMAL)
cv2.resizeWindow("Blurred Background", 800, 450)

frame_count = 0
while True:
    ret, frame = cap.read()
    if not ret:
        break

    # 프레임 크기 축소 → 속도 개선
    frame = cv2.resize(frame, (480, 270))
    frame_count += 1
    if frame_count % 2 != 0:
        continue 

    h, w, _ = frame.shape
    pil = Image.fromarray(cv2.cvtColor(frame, cv2.COLOR_BGR2RGB))
    tensor = transform(pil).unsqueeze(0)

    with torch.no_grad():
        d1, *_ = net(tensor)

    # 마스크 후처리
    mask = d1[0][0].cpu().numpy()
    mask = (mask - mask.min()) / (mask.max() - mask.min())
    mask = cv2.resize(mask, (w, h))
    mask = cv2.GaussianBlur(mask, (11, 11), 0)
    mask = np.clip(mask, 0, 1)
    mask_3ch = np.stack([mask] * 3, axis=-1)

    # 흐린 배경 만들기
    blurred_background = cv2.GaussianBlur(frame, (35, 35), 0)

    # 사람 + 흐린 배경 합성
    blended = (frame * mask_3ch + blurred_background * (1 - mask_3ch)).astype(np.uint8)

    cv2.imshow("Blurred Background", blended)

    # 프레임 저장
    out.write(blended)

    if cv2.waitKey(8) & 0xFF == ord('q'):
        break

cap.release()
out.release()
cv2.destroyAllWindows()