from PyQt5.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QLabel, QLineEdit, QRadioButton, QButtonGroup
from ui.specified.file_convert.upload_file import UploadFileWidget
from ui.specified.file_convert.show_file_data import ShowFileDataWidget
from ui.common.popup import ErrorPopup
from errors.errors import ErrorCodes
from model.store import VideoStore
import cv2

class FileConvertPage(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.initUI()
        self.videoStore = VideoStore()

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
        
        layout.addWidget(self.uploadWidget)
        layout.addWidget(self.showFileDataWidget)
        layout.addLayout(self.ratioInputLayout)
        layout.addLayout(self.droneTypeLayout)
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
        
        width = cap.get(cv2.CAP_PROP_FRAME_WIDTH)
        height = cap.get(cv2.CAP_PROP_FRAME_HEIGHT)
        frame_count = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
        fps = cap.get(cv2.CAP_PROP_FPS)
        cap.release()
        
        ratio = width / height
        if ratio in [5/4, 16/9, 16/10]:
            ratio_str = f'{int(width)}:{int(height)}'
            self.ratio = (int(width), int(height))
        elif height / width in [5/4, 16/9, 16/10]:
            ratio_str = f'{int(height)}:{int(width)}'
            self.ratio = (int(height), int(width))
        else:
            ratio_str = '지원되지 않는 형식'
            self.ratio = None
        
        print(f'Video ratio: {ratio_str}')
        print(f'Frame count: {frame_count}')
        print(f'FPS: {fps}')
        
        self.showFileDataWidget.updateData(ratio_str, frame_count, fps)
        
        # Store video data
        self.videoStore.set_video_data(ratio_str, frame_count, fps)
        self.videoStore.set_video_file(file_path)
        
        # Update input fields
        if self.ratio:
            self.widthInput.setText(str(self.ratio[0]))
            self.heightInput.setText(str(self.ratio[1]))

    def updateDimensions(self):
        if self.ratio:
            try:
                width_multiplier = int(self.widthInput.text()) // self.ratio[0]
                height_multiplier = int(self.heightInput.text()) // self.ratio[1]
                
                if width_multiplier == height_multiplier:
                    self.widthInput.setText(str(self.ratio[0] * width_multiplier))
                    self.heightInput.setText(str(self.ratio[1] * height_multiplier))
            except ValueError:
                pass

    def showErrorPopup(self, error_code):
        popup = ErrorPopup(error_code, self)
        popup.exec_()
