import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QPushButton, QLabel, QVBoxLayout, QWidget

class MyApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.setWindowTitle("PyQt5 Executable Example")
        self.setGeometry(100, 100, 400, 300)

        # 중앙 위젯 설정
        central_widget = QWidget()
        self.setCentralWidget(central_widget)

        layout = QVBoxLayout()

        # 라벨
        self.label = QLabel("Hello, PyQt5!", self)
        layout.addWidget(self.label)

        # 버튼
        btn = QPushButton("Click Me", self)
        btn.clicked.connect(self.on_click)
        layout.addWidget(btn)

        # 레이아웃 적용
        central_widget.setLayout(layout)

    def on_click(self):
        self.label.setText("Button Clicked!")

if __name__ == "__main__":
    app = QApplication(sys.argv)
    mainWin = MyApp()
    mainWin.show()
    sys.exit(app.exec_())
