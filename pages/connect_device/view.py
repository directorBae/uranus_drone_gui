from PyQt5.QtWidgets import QWidget, QHBoxLayout, QVBoxLayout, QLabel, QScrollArea, QPushButton, QSlider, QListWidget
from PyQt5.QtCore import Qt
import requests
from ui.common.device_lists import DeviceListWidget
from ui.common.pixels import ColorGrid
import numpy as np

class DeviceDetailWidget(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        mainLayout = QVBoxLayout()
        self.label = QLabel("디바이스 상세정보", self)
        mainLayout.addWidget(self.label)

        # 4×4 pixel grid for device visualization
        self.pixelGrid = ColorGrid(frames=np.array([[[[255, 255, 255]]*4]*4]), fps=1, progressBar=None)
        self.pixelGrid.hide()  # Will show after device selection
        mainLayout.addWidget(self.pixelGrid)

        # Color buttons
        self.colorButtonsLayout = QHBoxLayout()
        self.redButton = QPushButton("빨강", self)
        self.greenButton = QPushButton("초록", self)
        self.blueButton = QPushButton("파랑", self)
        self.colorButtonsLayout.addWidget(self.redButton)
        self.colorButtonsLayout.addWidget(self.greenButton)
        self.colorButtonsLayout.addWidget(self.blueButton)
        mainLayout.addLayout(self.colorButtonsLayout)

        # Custom color + sliders
        self.customLayout = QHBoxLayout()
        self.customButton = QPushButton("색 테스트", self)
        self.rSlider = QSlider(Qt.Horizontal)
        self.gSlider = QSlider(Qt.Horizontal)
        self.bSlider = QSlider(Qt.Horizontal)
        self.rSlider.setRange(0, 255)
        self.gSlider.setRange(0, 255)
        self.bSlider.setRange(0, 255)
        self.customLayout.addWidget(self.customButton)
        self.customLayout.addWidget(self.rSlider)
        self.customLayout.addWidget(self.gSlider)
        self.customLayout.addWidget(self.bSlider)
        mainLayout.addLayout(self.customLayout)

        self.currentIP = None

        # Create a file list widget inside a scroll area
        self.fileListWidget = QListWidget(self)
        self.fileListScroll = QScrollArea()
        self.fileListScroll.setWidgetResizable(True)
        self.fileListScroll.setWidget(self.fileListWidget)

        # Add a refresh button
        self.refreshFileListButton = QPushButton("파일 목록 갱신", self)

        # Replace the original horizontal layout usage
        layoutWrapper = QHBoxLayout()
        layoutWrapper.addLayout(mainLayout)

        # Create a vertical layout for the file list + refresh button
        fileListLayout = QVBoxLayout()
        fileListLayout.addWidget(self.fileListScroll)
        fileListLayout.addWidget(self.refreshFileListButton)
        layoutWrapper.addLayout(fileListLayout)
        self.setLayout(layoutWrapper)

        # Connect refresh button to a file list refresh method
        self.refreshFileListButton.clicked.connect(self.refreshFileList)

    def updateDetail(self, device_info):
        self.pixelGrid.show()
        self.label.setText(f"선택된 디바이스: {device_info}")
        self.currentIP = device_info.split(" - ")[0]

    def fetchFileList(self, ip):
        self.fileListWidget.clear()
        try:
            response = requests.get(f"http://{ip}:8000/files/list")
            files = response.json().get("files list")
            for filename in files:
                self.fileListWidget.addItem(filename)
        except Exception as e:
            self.fileListWidget.addItem(f"Error: {e}")

    def refreshFileList(self):
        if self.currentIP:
            self.fetchFileList(self.currentIP)

    def setUpSignals(self, ip):
        self.redButton.clicked.connect(lambda: self.sendColorRequest(ip, 255, 0, 0))
        self.greenButton.clicked.connect(lambda: self.sendColorRequest(ip, 0, 255, 0))
        self.blueButton.clicked.connect(lambda: self.sendColorRequest(ip, 0, 0, 255))
        self.customButton.clicked.connect(self.sendCustomColor(ip))

    def sendColorRequest(self, ip, r, g, b):
        try:
            response = requests.post(f"http://{ip}:8001/set_rgb", json={
                "r": r,
                "g": g,
                "b": b
            })
            print(response.json())
        except Exception as e:
            print(f"Error calling API: {e}")

    def sendCustomColor(self, ip):
        def handler():
            r = self.rSlider.value()
            g = self.gSlider.value()
            b = self.bSlider.value()
            self.sendColorRequest(ip, r, g, b)
        return handler

class ConnectDevicePage(QWidget):
    def __init__(self, parent=None, videoStore=None):
        super().__init__(parent)
        self.videoStore = videoStore
        self.initUI()

    def initUI(self):
        mainLayout = QHBoxLayout()

        self.scrollArea = QScrollArea()
        self.scrollArea.setWidgetResizable(True)

        self.deviceListWidget = DeviceListWidget(self)
        self.scrollArea.setWidget(self.deviceListWidget)

        self.detailWidget = DeviceDetailWidget(self)

        mainLayout.addWidget(self.scrollArea, 1)
        mainLayout.addWidget(self.detailWidget, 3)

        self.setLayout(mainLayout)
        self.setFixedSize(900, 600)  # Reduce overall size

        self.deviceListWidget.deviceList.itemClicked.connect(self.showDeviceDetail)

    def showDeviceDetail(self, item):
        ip_str = item.text().split(" - ")[0]  # Example: "192.168.1.10"
        self.detailWidget.updateDetail(item.text())
        self.detailWidget.fetchFileList(ip_str)
        self.detailWidget.setUpSignals(ip_str)
