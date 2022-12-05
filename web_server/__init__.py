from flask import Flask

app = Flask(__name__)
app.config.from_object('web_server.config')

import web_server.view.views
