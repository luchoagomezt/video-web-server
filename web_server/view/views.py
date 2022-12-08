from flask import request, redirect, url_for, render_template, flash, session
from web_server import app
from web_server.entity.video import Video


@app.route('/')
def show_video_with_track():
    video = Video("MEDQA 339 Add a professional")
    video_name = video.get_video_file_name()
    track_name = video.get_track_file_name()
    return render_template("index.html", video_name=video_name, track_name=track_name)
