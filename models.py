from extensions import db
from flask_login import UserMixin

class Case(db.Model):
    id = db.Column(db.String, primary_key=True)
    title = db.Column(db.String, nullable=False)
    genre = db.Column(db.String)
    status = db.Column(db.String)
    location = db.Column(db.String)
    year = db.Column(db.Integer)
    desc = db.Column(db.Text)
    image = db.Column(db.String)
    reviews = db.relationship("Review", backref="case", lazy=True)

class Review(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    case_id = db.Column(db.String, db.ForeignKey("case.id"), nullable=False)
    user = db.Column(db.String, default="Anonymous")
    text = db.Column(db.Text)

class Leaderboard(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    user = db.Column(db.String, nullable=False)
    points = db.Column(db.Integer, default=0)

class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    email = db.Column(db.String, unique=True, nullable=False)
    password = db.Column(db.String, nullable=False)
    username = db.Column(db.String, unique=True, nullable=False)
    first_login = db.Column(db.Boolean, default=True)
