import os
import cv2
import torch
import numpy as np
from PIL import Image
from torchvision import transforms
from model.u2net import U2NETP  # U2NET 클래스 import

# 1. 모델 로드
model_path = './saved_models/u2net/u2netp.pth'
net = U2NETP(3, 1)
net.load_state_dict(torch.load(model_path, map_location='cpu'))
net.eval()

# 2. 이미지 불러오기
image_path = 'test.jpg'
image = Image.open(image_path).convert('RGB')

transform = transforms.Compose([
    transforms.Resize((320, 320)),
    transforms.ToTensor(),
])

input_tensor = transform(image).unsqueeze(0)

# 3. 추론
with torch.no_grad():
    d1, _, _, _, _, _, _ = net(input_tensor)

mask = d1[0][0].cpu().numpy()
mask = (mask - mask.min()) / (mask.max() - mask.min())
mask = cv2.resize(mask, image.size)

cv2.imshow('Mask', (mask * 255).astype(np.uint8))
cv2.waitKey(0)
cv2.destroyAllWindows()

# 4. 마스크를 사용해 배경 제거
original = np.array(image)
mask_3ch = np.stack((mask, mask, mask), axis=-1)
foreground = (original * mask_3ch).astype(np.uint8)

# 5. 결과 저장/보기
cv2.imshow('U2Net Result', foreground)
cv2.waitKey(0)
cv2.destroyAllWindows()