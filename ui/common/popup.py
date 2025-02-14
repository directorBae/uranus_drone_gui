from PyQt5.QtWidgets import QDialog, QVBoxLayout, QLabel, QPushButton
from errors.errors import ErrorMessages

class ErrorPopup(QDialog):
    def __init__(self, error_code, parent=None):
        super().__init__(parent)
        self.error_code = error_code
        self.initUI()

    def initUI(self):
        layout = QVBoxLayout()
        
        # 오류 메시지 설정
        error_message = ErrorMessages.get_message(self.error_code)
        self.label = QLabel(error_message, self)
        
        # 확인 버튼
        self.okButton = QPushButton('확인', self)
        self.okButton.clicked.connect(self.accept)
        
        layout.addWidget(self.label)
        layout.addWidget(self.okButton)
        self.setLayout(layout)
        self.setWindowTitle('오류')
