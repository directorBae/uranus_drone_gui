from PyQt5.QtWidgets import QWidget, QPushButton, QVBoxLayout, QFileDialog, QLabel

class UploadFileWidget(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.initUI()

    def initUI(self):
        # 파일 업로드 버튼
        self.uploadButton = QPushButton('파일 업로드', self)
        self.uploadButton.clicked.connect(self.uploadFile)
        
        # 업로드된 파일 경로를 표시할 라벨
        self.fileLabel = QLabel('선택된 파일 없음', self)
        
        # 레이아웃 설정
        layout = QVBoxLayout()
        layout.addWidget(self.uploadButton)
        layout.addWidget(self.fileLabel)
        self.setLayout(layout)

    def uploadFile(self):
        options = QFileDialog.Options()
        file, _ = QFileDialog.getOpenFileName(self, '파일 선택', '', '비디오 파일 (*.mp4 *.avi *.mov *.mkv)', options=options)
        if file:
            self.fileLabel.setText(f'업로드된 파일: {file}')
            print(f'Uploaded file: {file}')

if __name__ == '__main__':
    import sys
    from PyQt5.QtWidgets import QApplication
    app = QApplication(sys.argv)
    w = UploadFileWidget()
    w.show()
    sys.exit(app.exec_())
