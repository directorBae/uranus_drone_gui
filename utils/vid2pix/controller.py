import subprocess
import os

from typing import TypedDict
from errors.errors import ErrorCodes
from ui.common.popup import ErrorPopup
from utils.error_log import log_error

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

    def run(self, parent=None):
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
            if not os.path.exists(self.pathway):
                error_message = f"파일을 찾을 수 없습니다: {self.pathway}"
                print("❌ 실행 실패! 에러 메시지:", error_message)
                log_error(error_message)
                ErrorPopup(ErrorCodes.FILE_NOT_FOUND, parent, error_message).exec_()
                return
            
            result = subprocess.run(command, capture_output=True, text=True, check=True)
            print("✅ 실행 성공!")
            print("출력 결과:", result.stdout)  # 표준 출력
            
            # 첫 번째 값이 0인지 확인
            output_lines = result.stdout.strip().split('\n')
            if output_lines and output_lines[0].startswith('0'):
                error_message = output_lines[0].split(',', 1)[1].strip() if ',' in output_lines[0] else "알 수 없는 오류"
                print("❌ 실행 실패! 에러 메시지:", error_message)
                log_error(error_message)
                ErrorPopup(ErrorCodes.CUSTOM_ERROR, parent, error_message).exec_()
                return
            
        except subprocess.CalledProcessError as e:
            print("❌ 실행 실패!")
            print("오류 메시지:", e.stderr)
            log_error(e.stderr)
            ErrorPopup(ErrorCodes.SUBPROCESS_ERROR, parent, e.stderr).exec_()
