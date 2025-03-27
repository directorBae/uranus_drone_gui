from PyQt5.QtWidgets import QDialog, QVBoxLayout, QLabel, QPushButton
from errors.errors import ErrorMessages
from utils.error_log import log_error

class ErrorPopup(QDialog):
    def __init__(self, error_code, parent=None, custom_message=None):
        super().__init__(parent)
        self.error_code = error_code
        self.custom_message = custom_message
        self.initUI()

    def initUI(self):
        layout = QVBoxLayout()
        
        # 오류 메시지 설정
        if self.custom_message:
            error_message = self.custom_message
        else:
            error_message = ErrorMessages.get_message(self.error_code)
        self.label = QLabel(error_message, self)
        
        # 에러 로그 기록
        log_error(error_message)
        
        # 확인 버튼
        self.okButton = QPushButton('확인', self)
        self.okButton.clicked.connect(self.accept)
        
        layout.addWidget(self.label)
        layout.addWidget(self.okButton)
        self.setLayout(layout)
        self.setWindowTitle('오류')
        self.setMinimumWidth(300)  # 최소 너비 설정
