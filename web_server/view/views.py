from flask import request, redirect, url_for, render_template, flash, session
from web_server import app
from web_server.entity.test import Test


@app.route('/')
def show_video_with_track():
    test = Test("MEDQA 339 Add a professional")
    video = test.get_video_file_name()
    track = test.get_track_file_name()
    return render_template("index.html", video_name=video, track_name=track)
