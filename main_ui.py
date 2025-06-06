import tkinter as tk
from tkinter import filedialog
import subprocess
import glob
from PIL import Image, ImageTk
import os


background_path = ""
image_list = glob.glob("backgrounds/*.jpg") + glob.glob("backgrounds/*.png")


# 배경 선택 시 자동 적용
def on_dropdown_change():
    global background_path
    selected = selected_image.get()
    matches = [img for img in image_list if os.path.basename(img) == selected]
    if matches:
        background_path = matches[0]
        label.config(text=f"✅ 선택된 배경: {selected}")
    else:
        background_path = ""
        label.config(text="❌ 선택된 이미지가 없습니다.")

def run_virtual_background():
    if background_path == "":
        label.config(text="❌ 배경 이미지를 먼저 선택하세요.")
        return
    subprocess.run(["python", "video_virtual_background_gui.py", background_path])

def run_live_virtual_background():
    if background_path == "":
        label.config(text="❌ 배경 이미지를 먼저 선택하세요.")
        return
    subprocess.run(["python", "video_virtual_background_live.py", background_path])

def run_blur_background():
    subprocess.run(["python", "video_virtual_background_blur.py"])

def run_mediapipe_virtual_background(): #mediapipe 사용
    if background_path == "":
        label.config(text="❌ 배경 이미지를 먼저 선택하세요.")
        return
    subprocess.run(["python", "video_virtual_background_mediapipe.py", background_path])

def on_dropdown_change(): # 배경화면 조그맣게 미리ㅂㅗ기
    global background_path
    selected = selected_image.get()
    matches = [img for img in image_list if selected in img]
    if matches:
        background_path = matches[0]
        label.config(text=f"✅ 선택된 배경: {selected}")

        # 썸네일 이미지 표시
        img = Image.open(background_path)
        img.thumbnail((200, 120))  # 원하는 썸네일 크기
        img_tk = ImageTk.PhotoImage(img)
        thumbnail_label.config(image=img_tk)
        thumbnail_label.image = img_tk  # 이미지 참조 유지
    else:
        background_path = ""
        label.config(text="❌ 선택된 이미지가 없습니다.")
        thumbnail_label.config(image=None)



# 윈도우 만들기
root = tk.Tk()
root.title("가상 배경 프로그램")
root.geometry("400x500")

selected_image = tk.StringVar()
display_names = [os.path.basename(img) for img in image_list]

selected_image.trace_add("write", lambda *args: on_dropdown_change())



# 라벨
label = tk.Label(root, text="배경 이미지를 선택하세요", wraplength=380)
label.pack(pady=10)

# 배경이미지 폴더에서 선택하기
label_dropdown = tk.Label(root, text="📸 배경 이미지 선택하기(아래 버튼 누르세요)")
label_dropdown.pack(pady=3)
display_names = [os.path.basename(img) for img in image_list]
dropdown = tk.OptionMenu(root, selected_image, *display_names)
dropdown.pack(pady=5)

# 썸네일
thumbnail_label = tk.Label(root)
thumbnail_label.pack(pady=5)

# 버튼 1 - 실행
btn_run = tk.Button(root, text="▶️ 웹캠이 없을 경우 테스트 영상 실행 (종료 : Q 키)", command=run_virtual_background)
btn_run.pack(pady=10)

# 버튼 2 - 실시간 모드 시작 버튼
btn_live = tk.Button(root, text="🎥 실시간 모드 시작", command=run_live_virtual_background)
btn_live.pack(pady=5)

# 버튼 3 - 흐림 효과
btn_blur = tk.Button(root, text="🌫 (실시간만)흐림 효과 적용", command=run_blur_background)
btn_blur.pack(pady=5)

# 버튼 4 - 빠른 모드 (좀 더 영상이 빠르게 적용됨)
btn_fast = tk.Button(root, text="⚡ 빠른 영상 모드 (MediaPipe)", command=run_mediapipe_virtual_background)
btn_fast.pack(pady=5)


root.mainloop()