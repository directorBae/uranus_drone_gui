from PyQt5.QtWidgets import QWidget, QVBoxLayout, QLabel

from model.store import VideoStore
import cv2

class VidPlayPage(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.initUI()
        self.videoStore = VideoStore()

    def initUI(self):
        layout = QVBoxLayout()
        
        # 간단한 목업 텍스트 추가
        self.label = QLabel('영상 재생 페이지', self)
        layout.addWidget(self.label)
        
        self.setLayout(layout)