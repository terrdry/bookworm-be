import os
basedir = os.path.abspath(os.path.dirname(__file__))

SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(basedir, '../books-tst.db')+'?check_same_thread=False'
SQLALCHEMY_TRACK_MODIFICATIONS = False
DEBUG = True
