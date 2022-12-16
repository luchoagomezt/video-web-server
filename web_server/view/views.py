from flask import *
from web_server import app
from web_server.entity.xml_parser import XMLParser
import untangle
import os
from distutils.log import debug
from fileinput import filename

BASE_DIRECTORY = os.path.dirname(os.path.realpath(__file__))
VIDEO_FILE_NAME = "videos/<test case name>.webm"
VTT_FILE_NAME = "videos/<test case name>.vtt"

@app.route('/', methods = ['POST'])
def upload_file():
    if request.method == 'POST':
        f = request.files['xml file']
        f.save(os.path.join(app.config['UPLOAD_FOLDER'], f.filename))
        return show_video_with_track(f.filename)

@app.route('/')
def show_video_with_track(file_name="original.xml"):
    xml_file_name = file_name

    xml_file_path_name = os.path.join(os.path.dirname(BASE_DIRECTORY), f'model\{xml_file_name}')
    xml_object = untangle.parse(xml_file_path_name)
    xml_parser = XMLParser(xml_object)

    test_names = xml_parser.get_test_names()
    test_case_name = test_names[0]

    vtt = xml_parser.generate_vtt(test_case_name)
    vtt_file = os.path.join(os.path.dirname(BASE_DIRECTORY), "static/" +
                            VTT_FILE_NAME.replace("<test case name>", test_case_name))

    with open(vtt_file, 'w') as fp:
        for entry in vtt:
            fp.write(entry)
        fp.close()

    video_name = VIDEO_FILE_NAME.replace("<test case name>", test_case_name)
    track_name = VTT_FILE_NAME.replace("<test case name>", test_case_name)

    return render_template("index.html",
                           video_name=video_name,
                           track_name=track_name,
                           tests=test_names)