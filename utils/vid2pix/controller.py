import subprocess
import os

from typing import TypedDict

class Vid2PixConfig(TypedDict):
    filename: str
    height: int
    width: int
    drone_type: str
    fps: int

class Vid2PixController:
    def __init__(self, config: Vid2PixConfig):
        self.pathway = os.path.join(os.path.dirname(__file__), 'vid2pix.exe')
        self.config = config

    def run(self):
        command = [
            self.pathway,
            self.config["filename"],
            str(self.config["height"]),
            str(self.config["width"]),
            self.config["drone_type"],
            str(self.config["fps"])
        ]
        print("Running command:", " ".join(command))
        try:           
            result = subprocess.run(command, capture_output=True, text=True, check=True)
            print("✅ 실행 성공!")
            print("출력 결과:", result.stdout)  # 표준 출력
        except subprocess.CalledProcessError as e:
            print("❌ 실행 실패!")
            print("오류 메시지:", e.stderr)
