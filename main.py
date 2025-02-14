import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QHBoxLayout, QWidget
from ui.common.sidebar import Sidebar
from pages.file_convert.view import FileConvertPage

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.setWindowTitle('Main Window')
        self.setGeometry(100, 100, 800, 600)
        
        centralWidget = QWidget(self)
        self.setCentralWidget(centralWidget)
        
        layout = QHBoxLayout()
        
        self.sidebar = Sidebar(self)
        self.fileConvertPage = FileConvertPage(self)
        
        layout.addWidget(self.sidebar)
        layout.addWidget(self.fileConvertPage)
        
        centralWidget.setLayout(layout)

    def change_page(self, page_name):
        if page_name == 'file_convert':
            self.fileConvertPage.show()
        # 다른 페이지 전환 로직 추가 가능

if __name__ == '__main__':
    app = QApplication(sys.argv)
    mainWindow = MainWindow()
    mainWindow.show()
    sys.exit(app.exec_())
