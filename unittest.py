import sys
from PyQt5.QtWidgets import QApplication
from pages.file_convert.view import FileConvertPage

if __name__ == '__main__':
    app = QApplication(sys.argv)
    fileConvertPage = FileConvertPage()
    fileConvertPage.show()
    sys.exit(app.exec_())
