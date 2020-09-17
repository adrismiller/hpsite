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

db.init_app(app)

#from models import *
@app.route("/", methods=["GET", "POST"])
def index():
    """
    Displays home page. 
    If POST method, it means that a user is trying to 
    logout, so the session information is updated. 

    """ 
    # logging out automatically takes user to Homepage, so if POST, user is logging out 
    if request.method == "POST":
        session['logged'] = 0
        session['user'] = ''
    return render_template("index.html")


@app.route('/login/', methods = ["POST", "GET"])
def login(): 
    """ 
    If the user is posting login information, this page 
    checks if the information is valid, logging the user in if so, 
    and prompting them to try again if not. Dispplays the blank 
    login page if GET request 

    """ 
        if request.method == "POST": # if submitting form 
            user = request.form.get("username") 
            passw = request.form.get("password")
            u = User.query.filter_by(user_id=user, passw=passw).first() 
            # if no matching user for the inputed id and password 
            if not u: 
                return render_template("login.html", message= "Username or password inccorect. Try again. ")
            else: 
                # login the user
                session['logged'] = 1
                session['user'] = user
                return render_template("login.html", message= "Login Sucessful!") 
        else:
            return render_template("login.html")

@app.route('/library/register', methods=["POST", "GET"])
def register():
    """ 
    Users can register for the libary site on this page.
    If the username they have selected isn't taken, 
    the user is added to the database.

    """
    # if GET request, just display registration page 
    if request.method == "GET": 
        return render_template("register.html")
    else: 
        user_id = request.form.get("username")
        passw = request.form.get("password") 
        u = User.query.get(user_id)
        # if the username isn't taken 
        if not u: 
            # create new user and add to database 
            new_user = User(user_id=user_id, passw=passw)
            db.session.add(new_user)
            db.session.commit()
            return render_template("register.html", message="Registration sucessful!")
        else: 
            # try again 
           return render_template("register.html", message="Username taken. Try again.")


@app.route("/library/search", methods=["POST", "GET"])
def search(): 
    """ 
    Libary search page allowes a logged in user to search 
    for a book by isbn, author, or title. If the book exists, 
    the user can view goodreads info and leave a review

    """ 
    # must be logged in to acess page 
    if ('logged' not in session) or session['logged'] == 0:
        return render_template("error.html", message='ERROR! You must be logged in to access this page.' )
    else:
        if request.method=="GET":
            return render_template("lsearch.html")
        else: 
            search = request.form.get("search")
            # find results from possible isbn, title and author matches 
            isbn_search = Book.query.filter(Book.isbn.ilike(f"%{search}%")).all()
            title_search = Book.query.filter(Book.title.ilike(f"%{search}%")).all()
            author_search = Book.query.filter(Book.author.ilike(f"%{search}%")).all()
            titles = []
            authors = []
            isbns = []
            # don't want to show repeated results (ie book's author is in name of book)
            results = set()
            for book in title_search: 
                results.add(book)
            for book in author_search:
                results.add(book)
            for book in isbn_search: 
                results.add(book)
            # if no matches 
            if len(results) == 0:
                return render_template("lsearch.html", message = "No results found")
            else: 
                # display all books that match search 
                return render_template("lsearch.html",results=(results), message="SEARCH Results: ")

@app.route('/library/search/<id>/', methods=["GET", "POST"])

def book_page(id): 
    """ 
    This page enables the user to search by book id (different than isbn)
    and view goodreads info about that book (if there is info)

    """ 
    # must be logged in to acess this page
    if ('logged' not in session) or session['logged'] == 0:
        return render_template("error.html", message='ERROR! You must be logged in to access this page.' )
    # get book with id number
    b = Book.query.get(id)
    # check to make sure book exists 
    if b is None: 
        return render_template('error.html', message='Book does not exist in archives')
    reviews = b.reviews
    # books that are Hogwarts books (do not exist) have been given an isbn of 00000000
    if b.isbn != "0000000000":
        res = requests.get("https://www.goodreads.com/book/review_counts.json", params={"key":  "uquafaKgwxta8EFeNDyw", "isbns": b.isbn})
        avg_rating = res.json()['books'][0]["average_rating"]
        num_reviews = res.json()['books'][0]['work_ratings_count']
    else: 
        # if it's a hogwarts book, there's no goodreads info on it 
        avg_rating = 'No Goodreads Info'
        num_reviews= 'No Goodreads Info'
    # if posting a review 
    if request.method=="POST": 
        # display review and add to review database 
        review_text = request.form.get("review")
        b.add_review(user=session["user"], review=review_text, score=3)
    else:
        return render_template('bookpage.html',title=b.title, id=id, author=b.author, isbn=b.isbn, year=b.datep, reviews=b.reviews, rating=avg_rating,num_reviews=num_reviews) 

@app.route("/library/api/<isbn>")
def api(isbn):
    """ 
    Users can request json response through 
    the libary site api. If isbn is 00000000, 
    the book is a Hogwarts Book (ie it is fake) 
    and an error will display. If the book isn't
    Hogwarts and doens't exist on goodreads, 
    error page will display
    """ 
    if isbn == "0000000000": # this means its a hogwarts book (has no goodreads isbn number)
        return render_template('error.html', message="Hogwarts books don't have ISBN numbers :( ") 
    else: 
        b = Book.query.filter_by(isbn=isbn).first()
        # book isnt a hogwarts book and it doesnt exist on goodreads
        if b is None: 
            return render_template('error.html', message="Book doesn't exist in our database :(")
        else: 
            title = b.title
            author = b.author
            year = b.datep 
            # get information from goodreads api 
            res = requests.get("https://www.goodreads.com/book/review_counts.json", params={"key":  "uquafaKgwxta8EFeNDyw", "isbns": b.isbn})
            avg_rating = res.json()['books'][0]["average_rating"]
            num_reviews = res.json()['books'][0]['work_ratings_count']
            # return JSON response of relavent book info 
            return jsonify({'title':title, 'author':author, 'year':year, 'isbn':isbn, 'review_count':num_reviews, 'average_score':avg_rating})


# main pages of website 
@app.route("/resources/")
def resources(): 
    return render_template("resources.html")

@app.route("/library/", methods=["GET"])
def library(): 
    return render_template("library.html")

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