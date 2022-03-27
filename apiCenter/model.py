from flask_login import UserMixin
from sqlalchemy import PrimaryKeyConstraint
from . import db

class User(UserMixin,db.Model):
    id = db.Column(db.Integer, primary_key=True) # primary keys are required by SQLAlchemy
    username = db.Column(db.String(100), unique=True)
    password = db.Column(db.String(100))

class TestingValues(db.Model):
    id = db.Column(db.Integer, primary_key=True) # primary keys are required by SQLAlchemy
    type_ = db.Column(db.String(100))
    ph = db.Column(db.String(100))
    turbidity = db.Column(db.String(100))
    TDS = db.Column(db.String(100))
    DO = db.Column(db.String(100))
    conductivity = db.Column(db.String(100))
    temp = db.Column(db.String(100))
    decision = db.Column(db.String(100))

class TypeTest(db.Model):
    id = db.Column(db.Integer, primary_key=True) # primary keys are required by SQLAlchemy
    type_ = db.Column(db.String(100))
