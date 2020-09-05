
import os
from sqlalchemy import Column, String, Integer, create_engine
from flask_sqlalchemy import SQLAlchemy
import json
import os
database_name = "hairstylist_api"
DBUSER = os.environ.get('DBUSER')
DBPASS = os.environ.get('DBPASS')
database_path = "postgresql://{}:{}@{}/{}".format(DBUSER, DBPASS, 'localhost:5432', database_name)
# database_path = "postgresql://postgres:0000@{}/{}".format('localhost:5432', database_name)
SQLALCHEMY_TRACK_MODIFICATIONS = False

db = SQLAlchemy()

'''
setup_db(app)
    binds a flask application and a SQLAlchemy service
'''


def setup_db(app, database_path=database_path):
    app.config["SQLALCHEMY_DATABASE_URI"] = database_path
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

    db.app = app
    db.init_app(app)
    db.create_all()


'''
Question

'''




