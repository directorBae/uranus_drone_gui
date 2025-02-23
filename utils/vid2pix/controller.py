import subprocess
import os

from typing import TypedDict

class Vid2PixConfig(TypedDict):
    filename: str
    unexpectednumber: int
    drone_number: int
    drone_type: str
    fps: int

class Vid2PixController:
    def __init__(self, config: Vid2PixConfig):
        self.pathway = os.path.join(os.path.dirname(__file__), 'vid2pix.exe')
        self.config = config

    def run(self):
        command = [
            self.pathway,
            self.config["filename"],
            str(self.config["unexpectednumber"]),
            str(self.config["drone_number"]),
            self.config["drone_type"],
            str(self.config["fps"])
        ]
        print("Running command:", " ".join(command))
        subprocess.run(command)