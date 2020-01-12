import os
basedir = os.path.abspath(os.path.dirname(__file__))

SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(basedir, '../books.db')
SQLALCHEMY_TRACK_MODIFICATIONS = False
DEBUG = False
