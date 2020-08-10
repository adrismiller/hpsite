import os

from flask import Flask, session, render_template, request
from flask_session import Session
from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker
from flask_socketio import SocketIO, emit
from flask_sqlalchemy import SQLAlchemy 

app = Flask(__name__)
# Check for environment variable
if not os.getenv("DATABASE_URL"):
    raise RuntimeError("DATABASE_URL is not set")

# Configure session to use filesystem
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
app.config["SECRET_KEY"] = os.getenv("SECRET_KEY")

socketio = SocketIO(app)
Session(app)


app.config["SQLALCHEMY_DATABASE_URI"] = os.getenv("DATABASE_URL")
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db = SQLAlchemy(app) 
db.init_app(app)

class User(db.Model):
    __tablename__ = "users"
    user_id = db.Column(db.String, primary_key=True)
    passw = db.Column(db.String, nullable=False)


class Book(db.Model): 
    __tablename__ = "books"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    isbn = db.Column(db.String, nullable=False)
    title = db.Column(db.String, nullable=False)
    author = db.Column(db.String, nullable=False)
    datep = db.Column(db.String, nullable=False)
    reviews = db.relationship('Review', backref = "books", lazy=True)

    def add_review(self, user, review, score):
        r = Review(book=self.title, user=user, review=review, score=score, book_id=self.id)
        db.session.add(r)
        db.session.commit()


class Review(db.Model): 
    __tablename__ = "reviews"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    book = db.Column(db.String, nullable=False)
    user = db.Column(db.String, nullable=False)
    review = db.Column(db.String, nullable=False)
    score = db.Column(db.Integer, nullable=False)
    book_id = db.Column(db.Integer, db.ForeignKey("books.id"), nullable=False)

  
