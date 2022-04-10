from flask_login import UserMixin
from sqlalchemy import PrimaryKeyConstraint
from . import db

class User(UserMixin,db.Model):
    id = db.Column(db.Integer, primary_key=True) # primary keys are required by SQLAlchemy
    type_ = db.Column(db.String(100))
    username = db.Column(db.String(100), unique=True)
    password = db.Column(db.String(100))

class vehicleDetails(UserMixin,db.Model):
    id=db.Column(db.Integer, primary_key=True)
    gpsPointCurr_ = db.Column(db.String(100))