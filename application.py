import os

from flask import Flask, session, render_template, request
from flask_session import Session
from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker


app = Flask(__name__)

# Check for environment variable
if not os.getenv("DATABASE_URL"):
    raise RuntimeError("DATABASE_URL is not set")

# Configure session to use filesystem
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

# Set up database
engine = create_engine(os.getenv("DATABASE_URL"))
db = scoped_session(sessionmaker(bind=engine))


@app.route("/")
def index():
    return render_template("index.html")

@app.route("/resources/")
def resources(): 
    return render_template("resources.html")

@app.route("/library/")
def library():   
    return render_template("library.html")

@app.route("/library/search", methods=["POST"])
def search(): 
    search = request.form.get("search")
    return render_template("lsearch.html", search=search)

@app.route("/aboutus/")
def aboutus():
    return render_template("aboutus.html")

@app.route("/academics/")
def academics():
    return render_template("academics.html")

@app.route("/admissions/")
def admissions():
    return render_template("admissions.html")

@app.route("/athletics/")
def athletics():
    return render_template("athletics.html")

@app.route("/houses/")
def houses():
    return render_template("houses.html")

@app.route("/studentlife/")
def studentlife():
    return render_template("studentlife.html")