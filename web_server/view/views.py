from flask import request, render_template
import web_server
from web_server import app
from web_server.entity.xml_parser import XMLParser
import untangle
import os

BASE_DIRECTORY = os.path.dirname(os.path.realpath(__file__))
VIDEO_FILE_NAME = "videos/<test case name>.webm"
VTT_FILE_NAME = "videos/<test case name>.vtt"


@app.route('/select-test', methods = ['POST'])
def select_test():
    app.logger.debug(f"select_test: {request.values['test-case-name']}")
    if web_server.xml_parser is not None:
        web_server.test_case_name = request.values['test-case-name']

        vtt = web_server.xml_parser.generate_vtt(web_server.test_case_name)
        vtt_file = os.path.join(os.path.dirname(BASE_DIRECTORY), "static/" +
                                VTT_FILE_NAME.replace("<test case name>", web_server.test_case_name))

        with open(vtt_file, 'w') as fp:
            for entry in vtt:
                fp.write(entry)
            fp.close()

    return show_video_with_track(web_server.test_names, web_server.test_case_name)


@app.route('/upload-file', methods = ['POST'])
def upload_file():
    app.logger.debug(f'upload_file: {request}')

    f = request.files['xml file']
    file_name = os.path.join(app.config['UPLOAD_FOLDER'], f.filename)
    f.save(file_name)

    web_server.xml_parser = XMLParser(untangle.parse(file_name))
    web_server.test_names = web_server.xml_parser.get_test_names()

    return show_video_with_track(web_server.test_names, web_server.test_names[0])


@app.route('/')
def show_video_with_track(test_names="", test_case_name=""):
    video_name = VIDEO_FILE_NAME.replace("<test case name>", test_case_name)
    track_name = VTT_FILE_NAME.replace("<test case name>", test_case_name)

    return render_template("index.html",
                           video_name=video_name,
                           track_name=track_name,
                           tests=test_names)