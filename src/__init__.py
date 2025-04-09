import os
from decouple import config
from flask import Flask, render_template
from flask_avatars import Avatars
from flask_moment import Moment
from flask_sqlalchemy import SQLAlchemy
from flask_caching import Cache


app = Flask(__name__)
app.config.from_object(config("APP_SETTINGS"))

db = SQLAlchemy(app)

app.config['SESSION_SQLALCHEMY'] = db

moment = Moment(app)


avatars = Avatars(app)

cache = Cache(app)

from src.api.routes import api
from src.web.routes import web

# Registering blueprints
app.register_blueprint(api, url_prefix='/api/')
app.register_blueprint(web, url_prefix='/')
