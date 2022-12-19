from flask import Flask
from web_server.entity.xml_parser import XMLParser
import os

app = Flask(__name__)
app.config.from_object('web_server.config')

APP_ROOT = os.path.dirname(os.path.realpath(__file__))
UPLOAD_FOLD = "model"
UPLOAD_FOLDER = os.path.join(APP_ROOT, UPLOAD_FOLD)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

import web_server.view.views
