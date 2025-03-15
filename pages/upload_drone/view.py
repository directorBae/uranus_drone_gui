from PyQt5.QtWidgets import QWidget, QHBoxLayout, QVBoxLayout, QScrollArea, QPushButton, QListWidgetItem, QLabel
import os
import requests
from ui.common.device_lists import DeviceListWidget

class UploadDronePage(QWidget):
    def __init__(self, parent=None, videoStore=None):
        super().__init__(parent)
        self.videoStore = videoStore
        self.currentIP = None

        # Main layout
        mainLayout = QHBoxLayout()

        # Left side: device list in a scroll area
        self.scrollArea = QScrollArea()
        self.scrollArea.setWidgetResizable(True)
        self.deviceListWidget = DeviceListWidget(self)
        self.scrollArea.setWidget(self.deviceListWidget)
        mainLayout.addWidget(self.scrollArea, 2)

        # Right side: upload button
        rightLayout = QVBoxLayout()
        self.uploadButton = QPushButton("파일 업로드", self)
        self.uploadButton.clicked.connect(self.uploadBinFiles)
        rightLayout.addWidget(self.uploadButton)

        # Optional label
        self.infoLabel = QLabel("드론에게 보낼 파일들을 업로드합니다.", self)
        rightLayout.addWidget(self.infoLabel)

        # Add layouts
        mainLayout.addLayout(rightLayout, 1)
        self.setLayout(mainLayout)

        # When user clicks on a device in the list
        self.deviceListWidget.deviceList.itemClicked.connect(self.deviceSelected)

    def deviceSelected(self, item: QListWidgetItem):
        ip_mac = item.text()
        self.currentIP = ip_mac.split(" - ")[0]  # "192.168.1.10"

    def uploadBinFiles(self):
        if not self.currentIP or not self.videoStore:
            print("No IP or video store", self.currentIP, self.videoStore)
            return
        try:
            # Get ratio, multiplier, and video filename from store
            filename = self.videoStore.get_video_file()
            if not filename:
                return
            baseName = os.path.splitext(os.path.basename(filename))[0]

            ratio = self.videoStore.get_video_data().get("ratio")
            multiplier = self.videoStore.get_multiplier()
            if not ratio or not multiplier:
                return

            width, height = map(int, ratio.split(":"))
            width *= multiplier
            height *= multiplier

            binFolder = os.path.join(os.path.dirname(__file__), f"../../src/bin/{baseName}")
            print("Uploading bin files from", binFolder)
            for i in range(width * height):
                binPath = os.path.join(binFolder, f"raspberry_{i}.bin")
                if os.path.exists(binPath):
                    with open(binPath, 'rb') as f:
                        files = {'file': (os.path.basename(binPath), f, 'application/octet-stream')}
                        requests.post(f"http://{self.currentIP}:8000/files/upload/", files=files)
        except Exception as e:
            print("Upload error:", e)
