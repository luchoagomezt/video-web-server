from flask import request, redirect, url_for, render_template, flash, session
from web_server import app
from web_server.scripts.test import Test

@app.route('/')
def show_entries():
    test = Test("MEDQA 306 Modify and save professional s file")
    video = test.get_video_file_name()
    track = test.get_track_file_name()
    return render_template("index.html", video_name=video, track_name=track)
