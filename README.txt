📦 가상 배경 프로그램 (U²-Net + MediaPipe 기반)

🧾 프로그램 소개
이 프로젝트는 사용자의 웹캠 영상 또는 샘플 동영상에서 사람을 분리하고,  
선택한 배경 이미지로 합성하는 Python 기반 가상 배경 프로그램입니다.  
MediaPipe 또는 U²-Net 기반으로 다양한 속도와 정확도를 지원하며,  
영상 저장, 흐림 효과, 실시간 모드 등을 포함합니다.

✔ 주요 기능
- MediaPipe 또는 U²-Net 기반 사람 인식
- 웹캠 또는 영상 파일 기반 입력
- 흐림 배경 처리
- 합성 영상 저장 (자동 파일명 생성)
- 실시간 미리보기 또는 GUI 기반 선택 실행

📁 구성된 주요 파일
├── video_virtual_background.py               ← 기본 U²-Net 배경 합성
├── video_virtual_background_blur.py          ← 흐림 배경 합성
├── video_virtual_background_gui.py           ← 배경 이미지 인자 받아 실행 (이미지합성 저장)
├── video_virtual_background_live.py          ← 실시간 웹캠 모드 (U²-Net)
├── video_virtual_background_mediapipe.py     ← 빠른 모드 (MediaPipe)
├── sample.mp4                                ← 테스트용 영상 (직접 추가 필요)
├── backgrounds/                              ← 배경 이미지 폴더 (.jpg, .png)

🛠 설치 방법
1. Python 3.10.11 설치
2. 아래 명령어 또는 배치 파일로 필수 라이브러리 설치

   ▶ install_requirements.bat
   또는 수동 설치:
   pip install -r requirements.txt

💻 실행 방법

1. 배경 이미지를 `backgrounds/` 폴더에 넣습니다.
2. 실행하고 싶은 파일에 따라 아래처럼 실행합니다:

   ▶ 일반 영상 + 배경 합성: python video_virtual_background.py
   ▶ 흐림 효과 적용: python video_virtual_background_blur.py
   ▶ GUI에서 배경 이미지 선택 후 실행: python video_virtual_background_gui.py
   ▶ 실시간 웹캠 모드 (U²-Net): python video_virtual_background_live.py 
   ▶ 빠른 처리 모드 (MediaPipe): python video_virtual_background_mediapipe.py

📦 실행 결과
- 프로그램 실행 시 실시간 영상 창이 열리고,
- `q` 키를 누르면 종료됩니다.
- 일부 모드는 자동으로 `.mp4` 영상이 저장됩니다 (타임스탬프 포함 이름)

📌 참고 사항
- webcam이 없는 경우 모든 실시간 모드는 `sample.mp4`로 대체하여 테스트 가능합니다
- PyTorch 모델: `./saved_models/u2net/u2netp.pth` 필요
- `background.jpg` 또는 `backgrounds/폴더 내 이미지`가 필요

------------------------------[run_app README]--------------------------------
🧾 프로그램 소개
이 프로그램은 웹캠 또는 테스트 영상을 기반으로 사람과 배경을 자동으로 분리하고, 사용자가 선택한 배경 이미지로 합성하여 가상 배경처럼 보여주는 데스크탑 애플리케이션입니다.

✔ 주요 기능:
- 배경 이미지 실시간 합성
- 흐림 효과 적용 가능
- 실시간 웹캠 모드 및 영상 테스트 가능
- MediaPipe 기반 빠른 모드
- 배경 썸네일 미리보기 지원

🛠 설치 방법:
1. Python 3.10 이상 설치 (https://www.python.org/)
2. 아래 배치 파일 실행:

   📄 install_requirements.bat

   또는 수동 설치:

   pip install -r requirements.txt


▶ 실행 방법:
1. 아래 파일을 더블클릭하세요:

   📄 run_app(더블클릭하세요).bat

2. 또는 수동 실행:

   python main_ui.py

3. 프로그램에서 배경 이미지를 선택한 뒤 원하는 모드를 실행하세요:
   - [▶️ 영상 시작] : U²-Net 영상 합성
   - [🎥 실시간 모드 시작] : 실시간 웹캠 모드
   - [🌫 흐림 효과] : 흐린 배경 적용 (실시간만)
   - [⚡ 빠른 영상 모드] : MediaPipe 기반 고속 처리


📌 참고:
- 배경 이미지 폴더는 기본으로 `backgrounds/`로 설정되어 있습니다.
- webcam이 없는 경우 sample.mp4 등으로 테스트 가능합니다.
- 영상 저장 기능은 일부 모드에서 자동 적용됩니다.


----------------------[run_desktop_appREADME]-----------------------
📦 실시간 가상 배경 프로그램 (MediaPipe + Streamlit)

🧾 프로그램 소개
웹캠 또는 노트북 카메라에서 사람을 실시간으로 분리하여,
사용자가 선택한 배경 이미지로 합성해주는 웹 기반 가상 배경 앱입니다.

✔ 주요 기능
- 📷 카메라 ON/OFF
- 🖼 배경 이미지 선택 (backgrounds 폴더)
- 🌫 흐림 배경 체크
- 실시간 웹캠 화면 위에 가상 배경 합성 (MediaPipe 기반)

🛠️ 설치 방법
1. Python 3.10 이상 설치
2. 아래 파일을 더블클릭하여 필수 패키지 자동 설치:

   ▶ install_requirements.bat

   또는 수동 설치:

   pip install -r requirements.txt

▶ 실행 방법
1. 아래 파일을 더블클릭:

   ▶ run_desktop_app(더블클릭하세요).bat

2. 또는 수동 실행:

   streamlit run live_virtual_bg_app.py

3. 웹 브라우저가 열리면:
   - 배경 이미지 선택
   - 흐림 여부 체크
   - 카메라 ON → 가상 배경 적용 시작!

💡 참고 사항
- webcam이 없을 경우 실시간 기능은 제한됨
- 배경 이미지는 `backgrounds` 폴더에 넣어주세요
- 기본적으로 MediaPipe 모델을 사용하여 빠르고 정확하게 사람과 배경을 분리합니다
----------------------------------------------------------------------------------

📧 문의
- 개발자: 신수연
- 이메일: ssy2650@naver.com
