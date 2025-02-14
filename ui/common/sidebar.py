from PyQt5.QtWidgets import QWidget, QVBoxLayout, QPushButton, QApplication
from PyQt5.QtCore import pyqtSignal
import sys

# 전역변수로 페이지 상태 저장
current_page = None

class Sidebar(QWidget):
    page_changed = pyqtSignal(str)

    def __init__(self, parent=None):
        super().__init__(parent)
        self.initUI()

    def initUI(self):
        layout = QVBoxLayout()

        # 페이지 전환 버튼 생성
        self.file_conversion_btn = QPushButton('파일 변환', self)
        self.video_playback_btn = QPushButton('영상 재생', self)
        self.device_connection_btn = QPushButton('기기 연결', self)
        self.drone_upload_btn = QPushButton('드론 업로드', self)
        self.drone_video_playback_btn = QPushButton('드론에서 영상 재생', self)

        # 버튼 클릭 시 페이지 전환 함수 연결
        self.file_conversion_btn.clicked.connect(lambda: self.page_changed.emit('file_convert'))
        self.video_playback_btn.clicked.connect(lambda: self.page_changed.emit('vid_play'))
        self.device_connection_btn.clicked.connect(lambda: self.page_changed.emit('connect_device'))
        self.drone_upload_btn.clicked.connect(lambda: self.page_changed.emit('upload_drone'))
        self.drone_video_playback_btn.clicked.connect(lambda: self.page_changed.emit('play_on_drone'))

        # 레이아웃에 버튼 추가
        layout.addWidget(self.file_conversion_btn)
        layout.addWidget(self.video_playback_btn)
        layout.addWidget(self.device_connection_btn)
        layout.addWidget(self.drone_upload_btn)
        layout.addWidget(self.drone_video_playback_btn)

        self.setLayout(layout)

if __name__ == '__main__':
    app = QApplication(sys.argv)
    sidebar = Sidebar()
    sidebar.show()
    sys.exit(app.exec_())
