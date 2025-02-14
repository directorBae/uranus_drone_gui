from PyQt5.QtWidgets import QWidget, QVBoxLayout
from ui.specified.file_convert.upload_file import UploadFileWidget
from ui.common.popup import ErrorPopup
from errors.errors import ErrorCodes
import cv2

class FileConvertPage(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.initUI()

    def initUI(self):
        layout = QVBoxLayout()
        
        self.uploadWidget = UploadFileWidget(self)
        self.uploadWidget.uploadButton.clicked.connect(self.checkVideoRatio)
        
        layout.addWidget(self.uploadWidget)
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
        cap.release()
        
        ratio = width / height
        print(f'Video ratio: {ratio}')

    def showErrorPopup(self, error_code):
        popup = ErrorPopup(error_code, self)
        popup.exec_()
