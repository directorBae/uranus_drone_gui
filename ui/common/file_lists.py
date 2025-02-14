from PyQt5.QtWidgets import QWidget, QPushButton, QHBoxLayout, QFileDialog, QListWidget
import os
from PyQt5.QtCore import Qt

class FileListWidget(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.initUI()
        # 선택된 파일 경로
        self.selected_file_path = ''

    def initUI(self):
        # 폴더 선택 버튼
        self.folderButton = QPushButton('폴더 열기', self)
        self.folderButton.clicked.connect(self.openFolderDialog)
        
        # 횡스크롤박스
        self.fileListBox = QListWidget(self)
        self.fileListBox.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOn)
        self.fileListBox.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        
        # 파일 선택 시 호출되는 메서드 연결
        self.fileListBox.itemClicked.connect(self.onFileSelected)
        
        # 레이아웃 설정
        layout = QHBoxLayout()
        layout.addWidget(self.folderButton)
        layout.addWidget(self.fileListBox)
        self.setLayout(layout)
        
        # 영상 파일 확장자 목록
        self.videoExtensions = ['.mp4', '.avi', '.mov', '.mkv']
        
        # 선택된 폴더 경로
        self.selectedFolderPath = ''

    def openFolderDialog(self):
        folder = QFileDialog.getExistingDirectory(self, '폴더 선택', '')
        if folder:
            self.selectedFolderPath = folder
            self.updateFileList()

    def updateFileList(self):
        self.fileListBox.clear()
        if self.selectedFolderPath:
            for file in os.listdir(self.selectedFolderPath):
                if any(file.endswith(ext) for ext in self.videoExtensions):
                    self.fileListBox.addItem(file)

    def onFileSelected(self, item):
        self.selected_file_path = os.path.join(self.selectedFolderPath, item.text())
        print(f'Selected file: {self.selected_file_path}')

if __name__ == '__main__':
    import sys
    from PyQt5.QtWidgets import QApplication
    app = QApplication(sys.argv)
    w = FileListWidget()
    w.show()
    sys.exit(app.exec_())