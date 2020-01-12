from flask import Flask,  jsonify, request
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_cors import CORS

app = Flask(__name__, instance_relative_config=True)


app.config.from_object('config.default')
app.config.from_pyfile('config.py')
app.config.from_envvar('APP_CONFIG_FILE')


# enable CORS
CORS(app, resources={r'/*': {'origins': '*'}})

db = SQLAlchemy(app)
migrate = Migrate(app, db)


from .models import Books
from .views import *
