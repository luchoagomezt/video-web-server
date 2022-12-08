from web_server.entity.video import Video


def test_video_file_name():
    """
    """
    test = Video("MEDQA 339 Add a professional")
    assert test.get_video_file_name() == "videos/MEDQA 339 Add a professional.webm"


def test_track_file_name():
    """
    """
    test = Video("MEDQA 339 Add a professional")
    assert test.get_track_file_name() == "videos/MEDQA 339 Add a professional.vtt"
