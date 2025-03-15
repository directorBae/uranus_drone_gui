from PyQt5.QtWidgets import QWidget, QVBoxLayout, QLabel, QPushButton, QListWidget, QListWidgetItem
import subprocess
import requests
import re
from concurrent.futures import ThreadPoolExecutor

class DeviceListWidget(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.initUI()

    def initUI(self):
        layout = QVBoxLayout()
        self.devices = []

        self.label = QLabel('연결 가능한 디바이스 목록', self)
        layout.addWidget(self.label)

        self.deviceList = QListWidget(self)
        layout.addWidget(self.deviceList)

        self.refreshButton = QPushButton('새로고침', self)
        self.refreshButton.clicked.connect(self.scanDevices)
        layout.addWidget(self.refreshButton)

        self.setLayout(layout)
        self.scanDevices()

    def scanDevices(self):
        self.deviceList.clear()
        self.devices = []
        self.getConnectedDevices()
        self.filter_PI()
        for ip, mac in self.devices:
            item = QListWidgetItem(f'{ip} - {mac}')
            self.deviceList.addItem(item)

    def send_ping(self, ip):
        command = ["ping", "-n", "1", "-w", "500", ip]
        subprocess.run(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)

    def scan_devices(self):
        base_ip = "172.30.1."
        num_threads = 100  # 최대 100개씩 동시에 실행

        with ThreadPoolExecutor(max_workers=num_threads) as executor:
            executor.map(self.send_ping, [f"{base_ip}{i}" for i in range(1, 256)])

    def getConnectedDevices(self):
        try:
            result = subprocess.run(['arp', '-a'], capture_output=True, text=True)
            lines = result.stdout.splitlines()
            for line in lines:
                match = re.search(r'(\d+\.\d+\.\d+\.\d+)\s+([\da-fA-F-]+)\s+\w+', line)
                if match:
                    ip, mac = match.groups()
                    self.devices.append((ip, mac))
        except Exception as e:
            print(f'Error scanning devices: {e}')
        return 0

    def filter_PI(self):
        valid_devices = []  # 새로운 리스트에 정상 IP만 저장

        def check_and_store(ip_mac):
            ip, mac = ip_mac
            try:
                response = requests.get(f"http://{ip}:8000/identify", timeout=2)
                print(ip, response.json())
                if response.json().get("message") == "I am a Raspberry Pi!":
                    valid_devices.append((ip, mac))  # API 응답 성공 시만 추가
            except Exception as e:
                print(f"❌ API 요청 실패: {ip} - {e}")

        # 멀티스레딩으로 API 요청 실행
        with ThreadPoolExecutor(max_workers=100) as executor:
            executor.map(check_and_store, self.devices)

        self.devices = valid_devices  # 필터링된 리스트로 대체

        