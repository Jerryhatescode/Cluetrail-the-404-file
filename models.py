from extensions import db
from flask_login import UserMixin

class Case(db.Model):
    __tablename__ = "case"

    id = db.Column(db.String, primary_key=True)
    title = db.Column(db.String, nullable=False)
    genre = db.Column(db.String)
    status = db.Column(db.String)
    location = db.Column(db.String)  # can store JSON string or text
    year = db.Column(db.Integer)
    desc = db.Column(db.Text)
    image = db.Column(db.String)

    # Coordinates
    lat = db.Column(db.Float)
    lng = db.Column(db.Float)

    # Complex JSON-based fields
    evidence = db.Column(db.Text)
    suspects = db.Column(db.Text)
    gallery = db.Column(db.Text)
    podcast = db.Column(db.Text)
    reddit = db.Column(db.Text)
    suggestions = db.Column(db.Text)
    story = db.Column(db.Text)
    rumors = db.Column(db.Text)
    timeline = db.Column(db.Text)
    impact = db.Column(db.Text)
    unsplash_queries = db.Column(db.Text)

    # Relationship
    reviews = db.relationship("Review", backref="case", lazy=True)


class Review(db.Model):
    __tablename__ = "review"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    case_id = db.Column(db.String, db.ForeignKey("case.id"), nullable=False)
    user = db.Column(db.String, default="Anonymous")
    text = db.Column(db.Text)


class Leaderboard(db.Model):
    __tablename__ = "leaderboard"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    user = db.Column(db.String, nullable=False)
    points = db.Column(db.Integer, default=0)


class User(UserMixin, db.Model):
    __tablename__ = "user"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    email = db.Column(db.String, unique=True, nullable=False)
    password = db.Column(db.String, nullable=False)
    username = db.Column(db.String, unique=True, nullable=False)
    first_login = db.Column(db.Boolean, default=True)
