# *gasp* It's in Flask!

from flask import Flask, flash, redirect, render_template, request, session
from flask_session import Session
from cs50 import SQL
from werkzeug.security import check_password_hash, generate_password_hash
import re
from helper import login_required
from datetime import date

app = Flask(__name__)

# Ensure templates are auto-reloaded
app.config["TEMPLATES_AUTO_RELOAD"] = True
app.config['SECRET_KEY'] = "Your_secret_string"

# Configure session to use filesystem (instead of signed cookies)
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

# Configure CS50 Library to use SQLite database
db = SQL("sqlite:///users.db")

@app.route('/', methods=["GET", "POST"])
def index():
    return render_template("index.html")

@app.route('/about', methods=["GET", "POST"])
def about():
    return render_template("about.html")

@app.route("/park", methods=["GET", "POST"])
def begin():
    return render_template("park.html")

@app.route("/den", methods=["GET", "POST"])
def den():

    # todo update methods 
    if request.method == "POST" and "inputTodo" in request.form:
        
        input = request.form.get('input')
        if input.isspace() or input == None or input == "":
            rows = db.execute("SELECT * FROM 'todo' WHERE user_id = ?", session["user_id"])
            print(rows)
            return render_template("den.html", open = True, rows=rows)
        db.execute("INSERT INTO todo (user_id, task, checked) VALUES(:user_id, :task, :checked)",
                user_id = session['user_id'], task = input, checked=0)
        rows = db.execute("SELECT * FROM 'todo' WHERE user_id = ?", session["user_id"])
        print(rows)
        return render_template("den.html", open = True, rows = rows)
    if request.method == "POST" and "del-todo" in request.form:
        id = request.form.get('del-todo')
        print("del-"+str(id)+" was clicked")
        db.execute("DELETE FROM 'todo' WHERE id = ?", id)
        rows = db.execute("SELECT * FROM 'todo' WHERE user_id = ?", session["user_id"])
        print(rows)
        return render_template("den.html", open = True, rows = rows)
    if request.method == "POST" and "check-todo" in request.form:
        id = request.form.get('id')
        checked = request.form.get('check-todo')
        print("check-" + id + " was passed" + checked)
        if checked == "0":
            
            db.execute("UPDATE 'todo' SET 'checked' = 1 WHERE id = ?", id)
        if checked == "1":
            
            db.execute("UPDATE 'todo' SET 'checked' = 0 WHERE id = ?", id)
        rows = db.execute("SELECT * FROM 'todo' WHERE user_id = ?", session["user_id"])
        print(rows)
        return render_template("den.html", open = True, rows = rows)

    # mood update methods 
    if request.method == "POST" and "mood" in request.form:
        input = request.form.get('moodInput')
        day = date.today()
        print(date)

        set = ""
        rows = db.execute("SELECT * FROM mood WHERE date = :date AND user_id = :user_id",
                                date=day, user_id=session['user_id'])
        
        try:
            db.execute("UPDATE 'mood' SET 'mood' = :mood WHERE user_id = :user_id AND date = :date", mood=input, user_id=session["user_id"], date=day)
            set = rows[0]['mood']
        except:
            db.execute("INSERT INTO 'mood' (user_id, via, date, mood) VALUES (:user_id, :via, :date, :mood)", user_id=session['user_id'], via='tracker', date=day, mood=int(input))
            set = ""

        set = ""
        mood = db.execute("SELECT * FROM mood WHERE date = :date AND user_id = :user_id",
                                    date=day, user_id=session['user_id'])
        try:
            set = mood[0]['mood']
        except:
            set = ""
        
            
        print(set)
        return render_template("den.html", open2 = True, set=set)

    # opening views 
    if request.method == "POST" and "updateView" in request.form:
        input = request.form.get('updateViewHid')
        
        if input == "open": #todo list
            rows = db.execute("SELECT * FROM 'todo' WHERE user_id = ?", session["user_id"])
            print(rows)
            return render_template("den.html", rows=rows, open=True)
            
        if input == "open2": #mood tracker
            
            day = date.today()
            set = ""
            mood = db.execute("SELECT * FROM mood WHERE date = :date AND user_id = :user_id",
                                        date=day, user_id=session['user_id'])
            try:
                set = mood[0]['mood']
            except:
                set = ""
            print(set)

            return render_template("den.html", set=set, open2 = True)
        
        if input == "open3": #journal
            return render_template("den.html", open3 = True)
        
        if input == "close": #open nothing
            return render_template("den.html")

  
    return render_template("den.html")


@app.route('/login', methods=["GET", "POST"])
def login():
    """Log user in"""
    if request.method == "POST":
        # Query database for username
        rows = db.execute("SELECT * FROM users WHERE email = :email",
                          email=request.form.get("email"))

        # Forget any user_id
        session.clear()

        # Ensure username was submitted
        if not request.form.get("email"):
            flash("Must provide email")
            return redirect("/login")

        # Ensure password was submitted
        elif not request.form.get("password"):
            flash("Must provide password")
            return redirect("/login")

        # Ensure username exists and password is correct
        elif len(rows) != 1 or not check_password_hash(rows[0]["password"], request.form.get("password")):
            flash("Invalid username and/or password")
            return redirect("/login")

        # Remember which user has logged in
        print(str(rows[0]["id"]))
        session['user_id'] = rows[0]["id"]
        print(session.get("user_id"))

        # Redirect user to home page
        return redirect("/")

    # User reached route via GET (as by clicking a link or via redirect)
    else:
        return render_template("login.html")

@app.route('/signup', methods=["GET", "POST"])
def signup():
    if request.method == "POST":
        session.clear()
        # some variables
        email = request.form.get('email')
        password = generate_password_hash(request.form.get('password'))
        first_name = request.form.get('firstname')
        last_name = request.form.get('lastname')

        # Check if email is valid
        if not re.match(r"[^@]+@[^@]+\.[^@]+", email):
            flash("Please enter a valid email address.")
            return redirect("/signup")
        # Check if email is already taken
        rows = db.execute("SELECT * FROM users WHERE email = :email", email=email)
        if len(rows) > 0:
            flash("This email is already taken.")
            return redirect("/signup")

        # Insert new user into database
        db.execute("INSERT INTO users (email, password, first_name, last_name) VALUES(:email, :password, :first_name, :last_name)",
                   email=email, password=password, first_name=first_name, last_name=last_name)

        # Auto Login
        rows = db.execute("SELECT * FROM users WHERE email = :email", email=email)
        session['user_id'] = rows[0]["id"]

        # Redirect user to home page
        return redirect("/")

    else:
        return render_template("signup.html")
    
@app.route("/logout")
@login_required
def logout():
    """Log user out"""
    # Forget any user_id
    session.clear()
    # Redirect user to login form
    return redirect("/")

@app.route("/todo", methods=["GET", "POST"])
@login_required
def todo():
    print("meow")

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000)
    