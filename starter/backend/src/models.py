
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

class Stylist(db.Model):
    __tablename__ = 'stylist'
    id = Column(Integer, primary_key=True)
    name = Column(String)
    speciality = Column(String(120))
    image_link = Column(String(500))
    rating = db.relationship('Rating', backref='stylist', cascade="all, delete, delete-orphan",lazy=True)  # a venue can have multiple shows
    def __init__(self, name, speciality, image_link):
        self.name = name
        self.speciality = speciality
        self.image_link = image_link
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
            'speciality':self.image_link,
            # 'rating':[dict(self.rating)]
        }

    def __repr__(self):
        return f'<Stylist {self.name}>'


class Customer(db.Model):
    __tablename__='customer'
    id=Column(Integer,primary_key=True)
    name=Column(String)
    ratings =  db.relationship('Rating', backref='customer', cascade="all, delete, delete-orphan",lazy=True)



class Rating(db.Model):
    __tablename__ = 'rating'

    id = Column(Integer, primary_key=True)
    rate = Column(Integer)
    stylist_id = Column(Integer, ForeignKey('stylist.id'))
    customer_id = Column(Integer, ForeignKey('customer.id'))
    comment = Column(String(255))


    def __init__(self, rate, stylist_id, customer_id, comment):
        self.rate = rate
        self.stylist_id = stylist_id
        self.customer_id = customer_id
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
            'stylist_id': self.stylist_id,
            'customer_id': self.customer_id,
            'comment':self.comment
        }

    def __repr__(self):
        return f'<id: {self.id}, rate: {self.rate}, comment:{self.comment} rated by id: {self.customer_id} stylist id {self.stylist_id}>'