import sys
from PyQt5.QtWidgets import QApplication, QWidget, QGridLayout
from PyQt5.QtGui import QPainter, QColor
from PyQt5.QtCore import Qt, QTimer
import numpy as np

class ColorCircle(QWidget):
    def __init__(self, r=155, g=155, b=155, diameter=10):
        super().__init__()
        self.r = r
        self.g = g
        self.b = b
        self.diameter = diameter
        self.initUI()

    def initUI(self):
        pass

    def paintEvent(self, event):
        qp = QPainter()
        qp.begin(self)
        self.drawCircle(qp)
        qp.end()

    def drawCircle(self, qp):
        color = QColor(self.r, self.g, self.b)
        qp.setBrush(color)
        qp.setPen(Qt.NoPen)
        qp.drawEllipse(5, 5, self.diameter, self.diameter)

    def setColor(self, r, g, b):
        self.r = r
        self.g = g
        self.b = b
        self.update()  # 재렌더링을 위해 update() 호출

    def setDiameter(self, diameter):
        self.diameter = diameter
        self.update()  # 재렌더링을 위해 update() 호출

class ColorGrid(QWidget):
    def __init__(self, frames):
        super().__init__()
        self.frames = frames
        self.current_frame_index = 0
        self.initUI()
        self.startTimer()

    def initUI(self):
        self.grid = QGridLayout()
        self.grid.setSpacing(1)  # 그리드 간 간격을 좁힘
        self.setLayout(self.grid)
        self.updateGrid()
        self.setWindowTitle('Color Grid')
        self.show()  # ColorGrid에서만 창을 표시

    def updateGrid(self):
        for i in reversed(range(self.grid.count())): 
            self.grid.itemAt(i).widget().setParent(None)
        rows, cols, _ = self.frames[self.current_frame_index].shape
        for i in range(rows):
            for j in range(cols):
                r, g, b = self.frames[self.current_frame_index][i, j]
                circle = ColorCircle(r, g, b)
                self.grid.addWidget(circle, i, j)

    def startTimer(self):
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.nextFrame)
        self.timer.start(100)  # 1초마다 프레임 변경

    def nextFrame(self):
        self.current_frame_index = (self.current_frame_index + 1) % len(self.frames)
        self.updateGrid()

class MultiColorGrid(QWidget):
    def __init__(self, frames, width, height):
        super().__init__()
        self.frames = frames
        self.width = width
        self.height = height
        self.initUI()

    def initUI(self):
        self.grid = QGridLayout()
        self.grid.setSpacing(1)
        self.setLayout(self.grid)
        self.populateGrids()
        self.setGeometry(0, 0, 400 * self.width, 400 * self.height)
        self.setWindowTitle('Multi Color Grid')
        self.show()

    def populateGrids(self):
        for i in range(self.height):
            for j in range(self.width):
                color_grid = ColorGrid(self.frames)
                self.grid.addWidget(color_grid, i, j)

if __name__ == '__main__':
    app = QApplication(sys.argv)
    
    # 10프레임짜리 샘플 케이스 생성 (각 프레임은 4x4 numpy 행렬)
    frames = [
        np.random.randint(0, 256, (4, 4, 3), dtype=np.uint8) for _ in range(10)
    ]
    
    ex = MultiColorGrid(frames, 16, 9)
    
    sys.exit(app.exec_())
