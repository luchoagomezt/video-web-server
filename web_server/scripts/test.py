class Test():
    def __init__(self, test_name):
        self.test_name = test_name

    def get_video_file_name(self):
        return self.test_name + '.webm'

    def get_track_file_name(self):
        return self.test_name + '.vtt'
