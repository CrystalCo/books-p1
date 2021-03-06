import os


from flask import Flask, render_template, request, session
from flask_session import Session
from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker

## Create the application object
app = Flask(__name__)

# Check for environment variable
if not ("postgres://paqubihkgzolaw:eb799f12a49889a8db4179144030e86e7920414e33e08503a78a8a02598caeb0@ec2-54-235-242-63.compute-1.amazonaws.com:5432/dcsd1tqompgjg2"):
    raise RuntimeError("DATABASE_URL is not set")

# Configure session to use filesystem
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

# Set up database
engine = create_engine("postgres://paqubihkgzolaw:eb799f12a49889a8db4179144030e86e7920414e33e08503a78a8a02598caeb0@ec2-54-235-242-63.compute-1.amazonaws.com:5432/dcsd1tqompgjg2")
db = scoped_session(sessionmaker(bind=engine))

## res = requests.get("https://www.goodreads.com/book/review_counts.json", params={"key": "mOzBjUPUddO5OgeRJwR1g", "isbns": "9781632168146"})
## print(res.json())

## Login Required decorator
##def login_required(f):
##    @wraps(f)
##    def wrap(*args, **kwargs):
##        if 'logged_in' in session:
##            return f(*args, **kwargs)
##        else:
##            return redirect(url_for('login'))
##    return wrap

@app.route("/")
def index():
    return render_template("index.html")

# use decorators to link the function to a url
@app.route("/home")
##@login_required
def home():
    books = db.execute("SELECT * FROM books").fetchone()
    return render_template("home.html", books=books)

@app.route("/login", methods=["GET", "POST"])
def login():
    error = None
    if request.method == 'POST':
        ## if  request.form['username'] != 'admin' or request.form['password'] != 'admin':
        if db.execute("SELECT * FROM users WHERE username != request.form['username'] OR password != request.form['password']", {"username": username, "password": password}).rowcount == 1:
            error = 'Invalid Credentials.  Please try again.'
        else:
            ## session['logged_in'] = True
            ## flash('You were just logged in!')
            return redirect(url_for('home'))
    return render_template('login.html', error=error)

@app.route("/logout")
##@login_required
def logout():
    session.pop("logged_in", None)
    flash("You were just logged out!")
    return render_template("index.html")

@app.route("/signup", methods=["GET", "POST"])
def signup():
        """Sign Up"""
        # Get form information.
        firstname = request.form.get("firstname")
        lastname = request.form.get("lastname")
        username = request.form.get("username")
        password = request.form.get("password")
        password2 = request.form.get("password2")

        # Make sure username does not already exist.
        if db.execute("SELECT * FROM users WHERE username = :username", {"username": username}).rowcount == 1:
            return render_template("error.html", message="That username already exists.")
        if password != password2:
            return render_template("error.html", message="Please make sure your passwords are the same.")
        db.execute("INSERT INTO users (firstname, lastname, username, password, password2) VALUES (:firstname, :lastname, :username, :password, :password2)",
                {"firstname": firstname, "lastname": lastname, "username": username, "password": password, "password2": password2})
        db.commit()
        return render_template("success.html")
