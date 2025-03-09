from PyQt5.QtWidgets import QWidget, QVBoxLayout, QLabel, QProgressBar, QPushButton
from model.store import VideoStore
from ui.common.pixels import MultiColorGrid
from utils.vid2pix.bin_read import yield_frames
import os

class VidPlayPage(QWidget):
    def __init__(self, parent=None, videoStore=None):
        super().__init__(parent)
        self.videoStore = videoStore or VideoStore()  # VideoStore 인스턴스 받기
        self.initUI()

    def initUI(self):
        self.layout = QVBoxLayout()
        
        # 간단한 목업 텍스트 추가
        self.label = QLabel('영상 재생 페이지', self)
        self.layout.addWidget(self.label)
        
        # 프로그레스바 추가
        self.progressBar = QProgressBar(self)
        self.layout.addWidget(self.progressBar)
        
        # 다시 재생 버튼 추가
        self.replayButton = QPushButton('다시 재생', self)
        self.replayButton.clicked.connect(self.updateMultiColorGrid)
        self.layout.addWidget(self.replayButton)
        
        self.setLayout(self.layout)

    def updateMultiColorGrid(self):
        try:
            self.filename = self.videoStore.get_video_file().split('/')[-1].split('.')[0]
            self.pathname = os.path.join(os.path.dirname(__file__), f'../../src/bin/{self.filename}')
            self.binfile_name_list = []
            
            for i in range(int(self.videoStore.get_video_data()['ratio'].split(':')[0])
            * self.videoStore.get_video_data()['multiplier']
            * int(self.videoStore.get_video_data()['ratio'].split(':')[1])
                        ):
                self.binfile_name_list.append(f'{self.pathname}/raspberry_{i}.bin')
                
            frame_generators = [yield_frames(filepath=binname) for binname in self.binfile_name_list]

        except Exception as e:
            print('Error:', e)
            self.label.setText('영상 파일을 불러오는 중 오류가 발생했습니다.')
        
        if hasattr(self, 'multiColorGrid'):
            self.layout.removeWidget(self.multiColorGrid)
            self.multiColorGrid.deleteLater()
        
        # 비디오 데이터를 가져와서 프레임 생성
        video_data = self.videoStore.get_video_data()
        ratio = video_data['ratio']
        multiplier = self.videoStore.get_multiplier()  # store에서 multiplier 가져오기
        fps = video_data['fps']

        print('ratio:', ratio, 'multiplier:', multiplier)
        
        if ratio and multiplier:
            width, height = map(int, ratio.split(':'))
            width *= multiplier
            height *= multiplier
            
            # 픽셀을 곱해진 만큼 화면에 추가
            self.multiColorGrid = MultiColorGrid(frame_generators, width, height, fps, self.progressBar)
            self.layout.addWidget(self.multiColorGrid)