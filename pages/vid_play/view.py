from PyQt5.QtWidgets import QWidget, QVBoxLayout, QLabel, QProgressBar, QPushButton
from model.store import VideoStore
from ui.common.pixels import MultiColorGrid
from utils.vid2pix.bin_read import yield_frames
import os
from ui.common.popup import ErrorPopup
from errors.errors import ErrorCodes
from utils.error_log import log_error

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
                
            frame_generators = [
                generator for binname in self.binfile_name_list
                if (generator := yield_frames(filepath=binname))
            ]

            if not frame_generators:  # 유효한 제너레이터가 없는 경우
                raise FileNotFoundError("BIN 파일을 읽는 중 오류가 발생했습니다.")

        except Exception as e:
            error_message = str(e)
            print('Error:', error_message)
            log_error(error_message)  # 에러 로그 기록
            ErrorPopup(ErrorCodes.FILE_NOT_FOUND, self, error_message).exec_()  # 에러 팝업 띄우기
            self.label.setText('영상 파일을 불러오는 중 오류가 발생했습니다.')
            return
        
        if hasattr(self, 'multiColorGrid'):
            self.layout.removeWidget(self.multiColorGrid)
            self.multiColorGrid.deleteLater()
        
        # 비디오 데이터를 가져와서 프레임 생성
        video_data = self.videoStore.get_video_data()
        ratio = video_data['ratio']
        multiplier = self.videoStore.get_multiplier()  # store에서 multiplier 가져오기
        fps = video_data['fps']

        print('ratio:', ratio, 'multiplier:', multiplier)

        try:        
            if ratio and multiplier:  # 유효한 데이터가 있는 경우에만 실행
                width, height = map(int, ratio.split(':'))
                
                # 픽셀을 곱해진 만큼 화면에 추가
                self.multiColorGrid = MultiColorGrid(frame_generators, width, height, fps, self.progressBar)
                self.layout.addWidget(self.multiColorGrid)

        except Exception as e:
            error_message = str(e)
            print('Error:', error_message)
            log_error(error_message)  # 에러 로그 기록
            ErrorPopup(ErrorCodes.CUSTOM_ERROR, self, error_message).exec_()