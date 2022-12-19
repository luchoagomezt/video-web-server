from flask import request, render_template
from web_server import app
import os
from web_server.entity.vtt_video import VTTVideo

BASE_DIRECTORY = os.path.dirname(os.path.realpath(__file__))
VIDEO_FILE_NAME = "videos/<test case name>.webm"
VTT_FILE_NAME = "videos/<test case name>.vtt"
VTT_VIDEO = VTTVideo()

<<<<<<< HEAD
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
=======

@app.route('/select-test', methods = ['POST'])
def select_test():
    app.logger.debug(f"select_test: {request.values['test-case-name']}")

    test_case_name = request.values['test-case-name']
>>>>>>> d884849bc68b7392ffe4f866ebda3c8351c32a3b
    vtt_file = os.path.join(os.path.dirname(BASE_DIRECTORY), "static/" +
                            VTT_FILE_NAME.replace("<test case name>", test_case_name))

    VTT_VIDEO.set_test_case_name(test_case_name)
    VTT_VIDEO.generate_vtt_list()
    VTT_VIDEO.save_vtt_list_to_file(vtt_file)

    return show_video_with_track()


@app.route('/upload-file', methods = ['POST'])
def upload_file():
    app.logger.debug(f'upload_file: {request}')

    fp = request.files['xml file']
    file_name = os.path.join(app.config['UPLOAD_FOLDER'], fp.filename)
    fp.save(file_name)

    VTT_VIDEO.set_parser(file_name)

    return show_video_with_track()


@app.route('/')
def show_video_with_track():
    test_case_name = VTT_VIDEO.get_test_name()

    video_name = VIDEO_FILE_NAME.replace("<test case name>", test_case_name)
    track_name = VTT_FILE_NAME.replace("<test case name>", test_case_name)

    test_names = VTT_VIDEO.get_test_names()

    return render_template("index.html",
                           video_name=video_name,
                           track_name=track_name,
                           tests=test_names)