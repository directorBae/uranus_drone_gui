import os
from datetime import datetime

# error.log가 없을 경우 생성
if not os.path.exists(os.path.join(os.path.dirname(__file__), '../error.log')):
    with open(os.path.join(os.path.dirname(__file__), '../error.log'), 'w', encoding='utf-8') as log_file:
        log_file.write('')

LOG_FILE_PATH = os.path.join(os.path.dirname(__file__), '../error.log')

def log_error(message: str):
    """에러 메시지를 error.log 파일에 기록합니다."""
    timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    with open(LOG_FILE_PATH, 'a', encoding='utf-8') as log_file:
        log_file.write(f"[{timestamp}] {message}\n")
