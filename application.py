import requests
import os
from flask import Flask, session, render_template, request, jsonify
from flask_session import Session
from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker
from models import * 

# initialize app! 

app = Flask(__name__)
# Check for environment variable
if not os.getenv("DATABASE_URL"):
    raise RuntimeError("DATABASE_URL is not set")

# Configure session to use filesystem
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
app.config["SECRET_KEY"] = os.getenv("SECRET_KEY")

Session(app)

app.config["SQLALCHEMY_DATABASE_URI"] = os.getenv("DATABASE_URL")
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

#db = SQLAlchemy(app) 
db.init_app(app)

#from models import *
@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST": # if logging out 
        session['logged'] = 0
        session['user'] = ''
    return render_template("index.html")


@app.route("/resources/")
def resources(): 
    return render_template("resources.html")

@app.route("/library/", methods=["GET"])
def library(): 
    return render_template("library.html")



@app.route('/login/', methods = ["POST", "GET"])
def login(): 
        if request.method == "POST":
            user = request.form.get("username")
            passw = request.form.get("password")
            u = User.query.filter_by(user_id=user).first()
            if not u: 
                return render_template("login.html", message= "Username or password inccorect. Try again. ")
            else: 
                session['logged'] = 1
                session['user'] = user
                return render_template("login.html", message= "Login Sucessful!") 
        else:
            return render_template("login.html")

@app.route('/library/register', methods=["POST", "GET"])
def register():
    if request.method == "GET": 
        return render_template("register.html")
    else: 
        user_id = request.form.get("username")
        passw = request.form.get("password") 
        u = User.query.get(user_id)
        if not u: 
            new_user = User(user_id=user_id, passw=passw)
            db.session.add(new_user)
            db.session.commit()
            return render_template("register.html", message="Registration sucessful!")
        else: 
           return render_template("register.html", message="Username taken. Try again.")
    # check if username in database: if not go through, add stuff to database 
    # is username in database: tell user that need to pick another username 
   # 


@app.route("/library/search", methods=["POST", "GET"])
def search(): 
    if ('logged' not in session) or session['logged'] == 0:
        return render_template("error.html", message='ERROR! You must be logged in to access this page.' )
    else:
        if request.method=="GET":
            return render_template("lsearch.html")
        else: 
            search = request.form.get("search")
            isbnSearch = Book.query.filter(Book.isbn.ilike(f"%{search}%")).all()
            titleSearch = Book.query.filter(Book.title.ilike(f"%{search}%")).all()
            authorSearch = Book.query.filter(Book.author.ilike(f"%{search}%")).all()
            titles = []
            authors = []
            isbns = []
            results = set()
            for book in titleSearch: 
                results.add(book)
            for book in authorSearch:
                results.add(book)
            for book in isbnSearch: 
                results.add(book)

            if len(results) == 0:
                return render_template("lsearch.html", message = "No results found")
            else: 
                return render_template("lsearch.html",results=(results), message="SEARCH Results: ")

@app.route('/library/search/<id>/', methods=["GET", "POST"])
def book_page(id): 
    if ('logged' not in session) or session['logged'] == 0:
        return render_template("error.html", message='ERROR! You must be logged in to access this page.' )
    b = Book.query.get(id)
    reviews = b.reviews
    if b.isbn != "0000000000":
        res = requests.get("https://www.goodreads.com/book/review_counts.json", params={"key":  "uquafaKgwxta8EFeNDyw", "isbns": b.isbn})
        avg_rating = res.json()['books'][0]["average_rating"]
        num_reviews = res.json()['books'][0]['work_ratings_count']
    else: 
        avg_rating = 'No Goodreads Info'
        num_reviews= 'No Goodreads Info'
    if request.method=="POST": 
        review_text = request.form.get("review")
        b.add_review(user=session["user"], review=review_text, score=3)
    if b is None: 
        return render_template('error.html', message='Book does not exist in archives')
    else:
        return render_template('bookpage.html',title=b.title, id=id, author=b.author, isbn=b.isbn, year=b.datep, reviews=b.reviews, rating=avg_rating,num_reviews=num_reviews) 

@app.route("/library/api/<isbn>")
def api(isbn):
    if isbn == "0000000000": 
        return render_template('error.html', message="Hogwarts books don't have ISBN numbers :( ") 
    else: 
        b = Book.query.filter_by(isbn=isbn).first()
        if b is None: 
            return render_template('error.html', message="Book doesn't exist in our database :(")
        else: 
            title = b.title
            author = b.author
            year = b.datep 
            res = requests.get("https://www.goodreads.com/book/review_counts.json", params={"key":  "uquafaKgwxta8EFeNDyw", "isbns": b.isbn})
            avg_rating = res.json()['books'][0]["average_rating"]
            num_reviews = res.json()['books'][0]['work_ratings_count']
            return jsonify({'title':title, 'author':author, 'year':year, 'isbn':isbn, 'review_count':num_reviews, 'average_score':avg_rating})


# main pages of website 
@app.route("/aboutus/")
def aboutus():
    return render_template("aboutus.html")

@app.route("/academics/")
def academics():
    return render_template("academics.html")

@app.route("/athletics/")
def athletics():
    return render_template("athletics.html")

@app.route("/houses/")
def houses():
    return render_template("houses.html")


# html files haven't been completed :(


@app.route("/studentlife/")
def studentlife():
    return render_template("nomuggles.html")

@app.route("/admissions/")
def admissions():
    return render_template("nomuggles.html")


@app.route("/news/")
def news():
    return render_template('nomuggles.html')

@app.route("/secrecy/")
def secrecy():
    return render_template('nomuggles.html')

@app.route("/underage/")
def underage(): 
    return render_template('nomuggles.html')

@app.route("/hogsmeade/")
def hogsmeade(): 
    return render_template('nomuggles.html')

@app.route("/alumni/")
def alumni(): 
    return render_template('nomuggles.html')