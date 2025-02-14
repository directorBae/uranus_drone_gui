# Component for showing video's ratio, frame per sec.
from PyQt5.QtWidgets import QWidget, QVBoxLayout, QLabel

class ShowFileDataWidget(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.initUI()

    def initUI(self):
        layout = QVBoxLayout()
        
        self.ratioLabel = QLabel('화면 비율: ', self)
        self.frameCountLabel = QLabel('프레임 수: ', self)
        self.fpsLabel = QLabel('프레임 per second: ', self)
        
        layout.addWidget(self.ratioLabel)
        layout.addWidget(self.frameCountLabel)
        layout.addWidget(self.fpsLabel)
        
        self.setLayout(layout)

    def updateData(self, ratio, frame_count, fps):
        self.ratioLabel.setText(f'화면 비율: {ratio}')
        self.frameCountLabel.setText(f'프레임 수: {frame_count}')
        self.fpsLabel.setText(f'프레임 per second: {fps}')