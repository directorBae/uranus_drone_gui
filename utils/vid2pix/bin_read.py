import numpy as np
import cv2
import os

# 파일 경로
dir_path = os.path.dirname(__file__)

URANUS_UR_16_SIZE = 4

def yield_frames(filepath, pixel_size=URANUS_UR_16_SIZE):
    try:
        with open(filepath, mode='rb') as file:
            data = file.read()

        frame_size = pixel_size * pixel_size * 3
        total_frames = len(data) // frame_size

        for i in range(total_frames):
            frame = data[i * frame_size : (i + 1) * frame_size]
            frame_np = np.frombuffer(frame, dtype=np.uint8).reshape(pixel_size, pixel_size, 3)
            frame_np = frame_np[:, :, [2,1,0]]  # BGR -> RGB 변환
            yield frame_np
    except FileNotFoundError as e:
        print(f"[ERROR] 파일을 찾을 수 없습니다: {filepath}")
        return 


if __name__ == '__main__':
    filepath = os.path.join(dir_path, '../../src/bin/KakaoTalk_20250223_110920955/raspberry_6.bin')

    with open(filepath, mode='rb') as file:
        data = file.read()

    frame_size = 4 * 4 * 3
    fps = 24

    total_frames = len(data) // frame_size
    
    # OpenCV 윈도우 생성
    cv2.namedWindow("BIN Video", cv2.WINDOW_NORMAL)
    cv2.resizeWindow("BIN Video", 4 * 20, 5 * 20)  # 보기 쉽게 확대

    for i in range(total_frames):
        frame = data[i * frame_size : (i + 1) * frame_size]
        print(frame)

        frame_np = np.frombuffer(frame, dtype=np.uint8).reshape(4, 4, 3)
        frame_np = frame_np[:, :, [0, 2, 1]]  # RBG -> RGB 변환
        cv2.imshow("BIN Video", frame_np)

        if cv2.waitKey(int(1000 / fps)) & 0xFF == ord('q'):
            break

        print(frame_np)