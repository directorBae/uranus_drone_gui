import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QHBoxLayout, QWidget, QStackedWidget
from ui.common.sidebar import Sidebar
from pages.file_convert.view import FileConvertPage
from pages.vid_play.view import VidPlayPage

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
        self.stackedWidget = QStackedWidget(self)
        
        self.fileConvertPage = FileConvertPage(self)
        self.vidPlayPage = VidPlayPage(self)
        
        self.stackedWidget.addWidget(self.fileConvertPage)
        self.stackedWidget.addWidget(self.vidPlayPage)
        
        layout.addWidget(self.sidebar)
        layout.addWidget(self.stackedWidget)
        
        centralWidget.setLayout(layout)
        
        # 시그널 연결
        self.sidebar.page_changed.connect(self.change_page)

    def change_page(self, page_name):
        if page_name == 'file_convert':
            self.stackedWidget.setCurrentWidget(self.fileConvertPage)
        elif page_name == 'vid_play':
            self.stackedWidget.setCurrentWidget(self.vidPlayPage)
        # 다른 페이지 전환 로직 추가 가능

if __name__ == '__main__':
    app = QApplication(sys.argv)
    mainWindow = MainWindow()
    mainWindow.show()
    sys.exit(app.exec_())
