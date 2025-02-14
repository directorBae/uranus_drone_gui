from PyQt5.QtWidgets import QWidget, QVBoxLayout, QLabel
from model.store import VideoStore
from ui.common.pixels import ColorGrid
import numpy as np

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
        
        # 테스트 데이터를 통해 ColorGrid 추가
        frames = [
            np.random.randint(0, 256, (4, 4, 3), dtype=np.uint8) for _ in range(10)
        ]
        self.colorGrid = ColorGrid(frames)
        layout.addWidget(self.colorGrid)
        
        self.setLayout(layout)