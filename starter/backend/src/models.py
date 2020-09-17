
import os
from sqlalchemy import Column, String, Integer, create_engine, ForeignKey
from flask_sqlalchemy import SQLAlchemy
import json
import os
database_name = "hairstylist_api"
DBUSER = os.environ.get('DBUSER')
DBPASS = os.environ.get('DBPASS')
#database_path = "postgresql://{}:{}@{}/{}".format(DBUSER, DBPASS, 'localhost:5432', database_name)
database_path = "postgresql://postgres:0000@{}/{}".format('localhost:5432', database_name)
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


def db_drop_and_create_all():
    db.drop_all()
    db.create_all()
def create_db():
    db.create_all()

class Artist(db.Model):
    __tablename__ = 'artist'
    id = Column(Integer, primary_key=True)
    name = Column(String)
    speciality = Column(String(120))
    image_link = Column(String(500))
    auth_user_id = Column(String)
    email = Column(String)
    rating = db.relationship('Rating', backref='artist', cascade="all, delete, delete-orphan",lazy=True)
    def __init__(self, name, email, speciality='', auth_user_id=''):
        self.name = name
        self.speciality = speciality
        self.auth_user_id = auth_user_id
        self.email = email

    def insert(self):
        db.session.add(self)
        db.session.commit()
    def update(self):
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()

    def format(self):
        return {
            'id':self.id,
            'name':self.name,
            'speciality':self.speciality,
            'email': self.email,
            'auth_user_id': self.auth_user_id,
            # 'rating':[dict(self.rating)]
        }

    def __repr__(self):
        return f' artist {self.name}, {self.id}, {self.speciality}, {self.email}>'

#
class Customer(db.Model):
    __tablename__ = 'customer'
    id = Column(Integer, primary_key=True)
    auth_user_id = Column(String)
    name = Column(String)
    email = Column(String)
    rating = db.relationship('Rating', backref='customer', cascade="all, delete, delete-orphan", lazy=True)

    def __init__(self, name, email, auth_user_id=''):
        self.auth_user_id = auth_user_id
        self.name = name
        self.email = email

    def insert(self):
        db.session.add(self)
        db.session.commit()

    def update(self):
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()

    def format(self):
        return {
            'id': self.id,
            'name': self.name,
            'email': self.email,
            'auth_user_id': self.auth_user_id,

        }




class Rating(db.Model):
    __tablename__ = 'rating'

    id = Column(Integer, primary_key=True)
    rate = Column(Integer)
    artist_id = Column(Integer, ForeignKey('artist.id'))
    customer_id = Column(Integer, ForeignKey('customer.id'))
    comment = Column(String(255))


    def __init__(self, rate, comment, artist_id, customer_id):
        self.rate = rate
        self.customer_id = customer_id
        self.artist_id = artist_id
        self.comment = comment

    def insert(self):
        db.session.add(self)
        db.session.commit()

    def update(self):
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()

    def format(self):
        return {
            'id': self.id,
            'rate': self.rate,
            'artist_id': self.artist_id,
            'customer_id': self.customer_id,
            'comment':self.comment
        }

    def __repr__(self):
        return f'<id: {self.id}, rate: {self.rate}, comment:{self.comment} rated by id: {self.customer_id} artist id {self.artist_id}>'