from flask import Flask,  jsonify, request
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_cors import CORS
import uuid
#from  import Config

app = Flask(__name__, instance_relative_config=True)

#app.config.from_object(Config)

app.config.from_object('config.default')
app.config.from_pyfile('config.py')
app.config.from_envvar('APP_CONFIG_FILE')


# enable CORS
CORS(app, resources={r'/*': {'origins': '*'}})

db = SQLAlchemy(app)
migrate = Migrate(app, db)

BOOKS = [
    {
        'book_id': uuid.uuid4().hex,
        'title': 'The Fifth Season',
        'author': 'N.K. Jemesin',
        'read': True
    },
    {
        'book_id': uuid.uuid4().hex,
        'title': 'The Warrior who carried Life',
        'author': 'Geoff Ryman',
        'read': True
    },
    {
        'book_id': uuid.uuid4().hex,
        'title': 'Words of Radiance',
        'author': 'Brandon Sanderson',
        'read': True
    },
    {
        'book_id': uuid.uuid4().hex,
        'title': 'Roadside Picnic',
        'author': 'Arkady Strugatsky',
        'read': True
    },
    {
        'book_id': uuid.uuid4().hex,
        'title': 'Perdido Street Station',
        'author': 'China Mieville',
        'read': True
    },
]

from bookworm.models import Books
from bookworm.views import *
