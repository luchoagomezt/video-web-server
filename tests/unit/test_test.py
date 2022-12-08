from video-web-server.web_server.entity.test import Test


def test_video_file_name():
    """
    """
    test = Test("MEDQA 339 Add a professional")
    assert test.get_video_file_name() == "videos/MEDQA 339 Add a professional.webm"


def test_video_file_name():
    """
    """
    test = Test("MEDQA 339 Add a professional")
    assert test.get_track_file_name() == "videos/MEDQA 339 Add a professional.vtt"
