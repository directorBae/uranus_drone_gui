from PyQt5.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QLabel, QLineEdit, QRadioButton, QButtonGroup, QPushButton
from PyQt5.QtCore import pyqtSignal
from ui.specified.file_convert.upload_file import UploadFileWidget
from ui.specified.file_convert.show_file_data import ShowFileDataWidget
from ui.common.popup import ErrorPopup
from errors.errors import ErrorCodes
from model.store import VideoStore
import cv2
import math

class FileConvertPage(QWidget):
    video_uploaded = pyqtSignal()
    video_converted = pyqtSignal()

    def __init__(self, parent=None, videoStore=None):
        super().__init__(parent)
        self.initUI()
        self.videoStore = videoStore or VideoStore()

    def initUI(self):
        layout = QVBoxLayout()
        
        self.uploadWidget = UploadFileWidget(self)
        self.uploadWidget.uploadButton.clicked.connect(self.checkVideoRatio)
        
        self.showFileDataWidget = ShowFileDataWidget(self)
        
        self.ratioInputLayout = QHBoxLayout()
        self.widthLabel = QLabel('너비: ', self)
        self.widthInput = QLineEdit(self)
        self.heightLabel = QLabel('높이: ', self)
        self.heightInput = QLineEdit(self)
        
        self.widthInput.textChanged.connect(self.updateDimensions)
        self.heightInput.textChanged.connect(self.updateDimensions)
        
        self.ratioInputLayout.addWidget(self.widthLabel)
        self.ratioInputLayout.addWidget(self.widthInput)
        self.ratioInputLayout.addWidget(self.heightLabel)
        self.ratioInputLayout.addWidget(self.heightInput)
        
        self.multiplierLabel = QLabel('배수: ', self)
        self.multiplierInput = QLineEdit(self)
        self.multiplierInput.textChanged.connect(self.updateDimensions)
        
        self.ratioInputLayout.addWidget(self.multiplierLabel)
        self.ratioInputLayout.addWidget(self.multiplierInput)
        
        # 드론 타입 선택 토글 추가
        self.droneTypeLayout = QHBoxLayout()
        self.droneTypeLabel = QLabel('드론 타입: ', self)
        self.ur16RadioButton = QRadioButton('UR-16', self)
        self.ur25RadioButton = QRadioButton('UR-25', self)
        self.ur36RadioButton = QRadioButton('UR-36', self)
        
        self.ur25RadioButton.setEnabled(False)
        self.ur36RadioButton.setEnabled(False)
        
        self.droneTypeGroup = QButtonGroup(self)
        self.droneTypeGroup.addButton(self.ur16RadioButton)
        self.droneTypeGroup.addButton(self.ur25RadioButton)
        self.droneTypeGroup.addButton(self.ur36RadioButton)
        
        self.droneTypeLayout.addWidget(self.droneTypeLabel)
        self.droneTypeLayout.addWidget(self.ur16RadioButton)
        self.droneTypeLayout.addWidget(self.ur25RadioButton)
        self.droneTypeLayout.addWidget(self.ur36RadioButton)
        
        self.droneTypeGroup.buttonClicked.connect(self.updateConvertButtonState)
        
        self.convertButton = QPushButton('변환하기', self)
        self.convertButton.setEnabled(False)
        self.convertButton.clicked.connect(self.convertVideo)
        
        layout.addWidget(self.uploadWidget)
        layout.addWidget(self.showFileDataWidget)
        layout.addLayout(self.ratioInputLayout)
        layout.addLayout(self.droneTypeLayout)
        layout.addWidget(self.convertButton)
        self.setLayout(layout)

    def checkVideoRatio(self):
        file_path = self.uploadWidget.fileLabel.text().replace('업로드된 파일: ', '')
        if not file_path or file_path == '선택된 파일 없음':
            self.showErrorPopup(ErrorCodes.FILE_NOT_FOUND)
            return
        
        cap = cv2.VideoCapture(file_path)
        if not cap.isOpened():
            self.showErrorPopup(ErrorCodes.INVALID_FILE_FORMAT)
            return
        
        def gcd(a, b):
            while b:
                a, b = b, a % b
            return a

        def simplify_ratio(width, height):
            common_divisor = gcd(width, height)
            return int(width / common_divisor), int(height / common_divisor)

        width = cap.get(cv2.CAP_PROP_FRAME_WIDTH)
        height = cap.get(cv2.CAP_PROP_FRAME_HEIGHT)
        frame_count = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
        fps = cap.get(cv2.CAP_PROP_FPS)
        cap.release()
        
        ratio = width / height
        if ratio in [5/4, 16/9, 16/10]:
            simplified_width, simplified_height = simplify_ratio(int(width), int(height))
            ratio_str = f'{simplified_width}:{simplified_height}'
            self.simplified_ratio = (simplified_width, simplified_height)
            self.ratio = (int(width), int(height))
        elif height / width in [5/4, 16/9, 16/10]:
            simplified_width, simplified_height = simplify_ratio(int(height), int(width))
            ratio_str = f'{simplified_width}:{simplified_height}'
            self.simplified_ratio = (simplified_width, simplified_height)
            self.ratio = (int(height), int(width))
        else:
            ratio_str = '지원되지 않는 형식'
            self.simplified_ratio = None
            self.ratio = None
        
        print(f'Video ratio: {ratio_str}')
        print(f'Frame count: {frame_count}')
        print(f'FPS: {fps}')
        
        self.showFileDataWidget.updateData(ratio_str, frame_count, fps)
        
        # Store video data
        self.videoStore.set_video_data(ratio_str, frame_count, fps)
        print("비디오 데이터 저장 완료", ratio_str, frame_count, fps)
        
        self.videoStore.set_video_file(file_path)
        
        # Update input fields
        if self.simplified_ratio:
            self.widthInput.setText(str(self.simplified_ratio[0]))
            self.heightInput.setText(str(self.simplified_ratio[1]))

        # Enable convert button if file is valid and drone type is selected
        self.updateConvertButtonState()
        
        # Emit video_uploaded signal
        self.video_uploaded.emit()

    def updateDimensions(self):
        if self.simplified_ratio:
            try:
                multiplier = int(self.multiplierInput.text())
                self.widthInput.setText(str(self.simplified_ratio[0] * multiplier))
                self.heightInput.setText(str(self.simplified_ratio[1] * multiplier))
                self.videoStore.set_multiplier(multiplier)  # multiplier 값을 저장
                # Update video data with multiplier
                self.videoStore.set_video_data(
                    f'{self.simplified_ratio[0] * multiplier}:{self.simplified_ratio[1] * multiplier}',
                    self.videoStore.get_video_data()['frame_count'],
                    self.videoStore.get_video_data()['fps'],
                    multiplier
                )
            except ValueError:
                pass

    def updateConvertButtonState(self):
        if self.ratio and self.droneTypeGroup.checkedButton():
            self.convertButton.setEnabled(True)
        else:
            self.convertButton.setEnabled(False)

    def convertVideo(self):
        print("변환합니다")
        # 실제로 영상을 픽셀로 변환하는 함수가 여기에 들어갈 예정입니다.
        
        # Emit video_converted signal
        self.video_converted.emit()

    def showErrorPopup(self, error_code):
        popup = ErrorPopup(error_code, self)
        popup.exec_()
