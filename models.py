import os
from sqla_wrapper import SQLAlchemy

db = SQLAlchemy(os.getenv("DATABASE_URL", "sqlite:///db.sqlite").replace("postgres://", "postgresql://", 1))  # this connects to a database either on Heroku or on localhost

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, unique=False)
    email = db.Column(db.String, unique=True)
    password = db.Column(db.String)
    session_token = db.Column(db.String)

class Message(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    author = db.Column(db.String, unique=False)
    text = db.Column(db.String, unique=False)