class VideoStore:
    def __init__(self):
        self.video_data = {
            'ratio': None,
            'frame_count': None,
            'fps': None,
            'multiplier': None  # multiplier 추가
        }
        self.video_file = None

    def set_video_data(self, ratio, frame_count, fps, multiplier=None):
        self.video_data['ratio'] = ratio
        self.video_data['frame_count'] = frame_count
        self.video_data['fps'] = fps
        self.video_data['multiplier'] = multiplier  # multiplier 저장

    def get_video_data(self):
        return self.video_data

    def set_video_file(self, video_file):
        self.video_file = video_file

    def get_video_file(self):
        return self.video_file

    def set_multiplier(self, multiplier):
        self.video_data['multiplier'] = multiplier  # multiplier 저장

    def get_multiplier(self):
        return self.video_data['multiplier']  # multiplier 반환