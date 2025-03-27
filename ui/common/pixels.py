import sys
from PyQt5.QtWidgets import QApplication, QWidget, QGridLayout, QProgressBar
from PyQt5.QtGui import QPainter, QColor
from PyQt5.QtCore import Qt, QTimer
import numpy as np
from utils.error_log import log_error

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
    def __init__(self, frames, fps, progressBar):
        super().__init__()
        self.frames = frames
        self.fps = fps
        self.progressBar = progressBar
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
        rows, cols = self.frames[self.current_frame_index].shape[:2]
        for i in range(rows):
            for j in range(cols):
                r, g, b = self.frames[self.current_frame_index][i, j]
                circle = ColorCircle(r, g, b)
                self.grid.addWidget(circle, i, j)
        if self.progressBar:
            self.progressBar.setValue(self.current_frame_index + 1)

    def startTimer(self):
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.nextFrame)
        self.timer.start(int(1000 / self.fps))  # FPS에 따라 프레임 간격 설정

    def nextFrame(self):
        self.current_frame_index = (self.current_frame_index + 1) % len(self.frames)
        self.updateGrid()

class MultiColorGrid(QWidget):
    def __init__(self, frame_generators, width, height, fps, progressBar):
        super().__init__()
        self.frame_generators = frame_generators
        self.width = width
        self.height = height
        self.fps = fps
        self.progressBar = progressBar
        self.frames = []

        # frame_generators가 비어 있는 경우 초기화 중단
        if not self.frame_generators:
            print("[ERROR] 유효한 frame_generators가 없습니다.")
            log_error("유효한 frame_generators가 없습니다.")
            return

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
                frames = list(self.frame_generators[i * self.width + j])
                self.frames.append(frames)
                color_grid = ColorGrid(frames, self.fps, self.progressBar)
                self.grid.addWidget(color_grid, i, j)
        total_frames = len(self.frames[0])
        self.progressBar.setMaximum(total_frames)

if __name__ == '__main__':
    app = QApplication(sys.argv)
    
    # 10프레임짜리 샘플 케이스 생성 (각 프레임은 4x4 numpy 행렬)
    frames = [
        np.random.randint(0, 256, (4, 4, 3), dtype=np.uint8) for _ in range(10)
    ]
    
    ex = MultiColorGrid([iter(frames)] * 16 * 9, 16, 9, 24, QProgressBar())
    
    sys.exit(app.exec_())
