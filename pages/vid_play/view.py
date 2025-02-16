from PyQt5.QtWidgets import QWidget, QVBoxLayout, QLabel
from model.store import VideoStore
from ui.common.pixels import MultiColorGrid
import numpy as np

class VidPlayPage(QWidget):
    def __init__(self, parent=None, videoStore=None):
        super().__init__(parent)
        self.videoStore = videoStore or VideoStore()  # VideoStore 인스턴스 받기
        self.initUI()

    def initUI(self):
        self.layout = QVBoxLayout()        
        self.setLayout(self.layout)

    def updateMultiColorGrid(self):
        if hasattr(self, 'multiColorGrid'):
            self.layout.removeWidget(self.multiColorGrid)
            self.multiColorGrid.deleteLater()
        
        # 비디오 데이터를 가져와서 프레임 생성
        video_data = self.videoStore.get_video_data()
        ratio = video_data['ratio']
        multiplier = self.videoStore.get_multiplier()  # store에서 multiplier 가져오기

        print('ratio:', ratio, 'multiplier:', multiplier)
        
        if ratio and multiplier:
            width, height = map(int, ratio.split(':'))
            width *= multiplier
            height *= multiplier
            
            # 픽셀을 곱해진 만큼 화면에 추가
            frames = [
                np.random.randint(0, 256, (4, 4, 3), dtype=np.uint8) for _ in range(10)
            ]
            
            self.multiColorGrid = MultiColorGrid(frames, width, height)
            print('multicolorgrid created')
            self.layout.addWidget(self.multiColorGrid)
            print('multicolorgrid added to layout')

        else:
            self.label2 = QLabel('영상을 변환하세요', self)
            self.layout.addWidget(self.label2)
