# import os

# from flask import Flask, session, render_template, request
# from flask_session import Session
# from sqlalchemy import create_engine
# from sqlalchemy.orm import scoped_session, sessionmaker
# #from models import *
# #import os 
# #from flask import Flask 
# from flask_sqlalchemy import SQLAlchemy 

# app = Flask(__name__)
# # Check for environment variable
# if not os.getenv("DATABASE_URL"):
#     raise RuntimeError("DATABASE_URL is not set")

# # Configure session to use filesystem
# app.config["SESSION_PERMANENT"] = False
# app.config["SESSION_TYPE"] = "filesystem"
# Session(app)

# # new stuff
# app.config["SQLALCHEMY_DATABASE_URI"] = os.getenv("DATABASE_URL")
# app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

 
# # Set up database old stuff
# #engine = create_engine(os.getenv("DATABASE_URL"))
# #db = scoped_session(sessionmaker(bind=engine))
# db = SQLAlchemy(app) 
# db.init_app(app)

from models import *

@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST": # if logout button was put here
        session['logged'] = 0
        session['user'] = ''
    return render_template("index.html")

@app.route("/resources/")
def resources(): 
    return render_template("resources.html")

@app.route("/library/", methods=["POST", "GET"])
def library(): 
    if request.method == "POST":
        user = request.form.get("username")
        passw = request.form.get("password")
        u = User.query.filter_by(user_id=user).first()
        if not u: 
            return render_template("library.html", message= "Username or password inccorect. Try again. ")
        else: 
            session['logged'] = 1
            session['user'] = user
            return render_template("library.html", message= "Login Sucessful!") 
    else:
        return render_template("library.html")




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
        return render_template("error.html")
    else:
        if request.method=="GET":
            return render_template("lsearch.html")
        else: 
            search = request.form.get("search")
            isbnSearch = Book.query.filter(Book.isbn.ilike(f"%{search}%")).all()
            titleSearch = Book.query.filter(Book.title.ilike(f"%{search}%")).all()
            authorSearch = Book.query.filter(Book.author.ilike(f"%{search}%")).all()
            results = set()
            for book in titleSearch: 
                results.add(book.title)
            for book in authorSearch:
                results.add(book.title)
            for book in isbnSearch: 
                results.add(book.title)
            if len(results) == 0: 
                message = "No results found"
            else: 
                message = "SEARCH Results: "
            return render_template("lsearch.html",results=sorted(results), message=message)
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

@app.route("/news/")
def news():
    return render_template('news.html')

@app.route("/secrecy/")
def secrecy():
    return render_template('secrecy.html')

@app.route("/underage/")
def underage(): 
    return render_template('underage.html')

@app.route("/hogsmeade/")
def hogsmeade(): 
    return render_template('hogsmeade.html')

@app.route("/alumni/")
def alumni(): 
    return render_template("alumni.html")