
from . import db
from flask_login import UserMixin
from datetime import datetime


class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key = True)
    username = db.Column(db.String(200))
    email = db.Column(db.String(50), unique = True)
    password = db.Column(db.String(50))
    todos = db.relationship('Todo')
    

class Todo(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    data = db.Column(db.String(200))
    date = db.Column(db.DateTime(timezone = True), default = datetime.utcnow())
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))