# *gasp* It's in Flask!

# ONLY DO THIS ONCE
# import nltk 
# nltk.download("vader_lexicon")
try:
  from nltk.sentiment import SentimentIntensityAnalyzer
  sia = SentimentIntensityAnalyzer()
except LookupError as e:
  import nltk 
  nltk.download("vader_lexicon")
  from nltk.sentiment import SentimentIntensityAnalyzer
  sia = SentimentIntensityAnalyzer()


from flask import Flask, flash, redirect, render_template, request, session
from flask_session import Session
from cs50 import SQL
from werkzeug.security import check_password_hash, generate_password_hash
import re
from helper import login_required
from datetime import date as DT
from bardapi import Bard
import os


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
        day = DT.today()

        setMood = ""
        rows = db.execute("SELECT * FROM mood WHERE date = :date AND user_id = :user_id AND via = 'tracker' ",
                                date=day, user_id=session['user_id'])
        
        try:
            db.execute("UPDATE 'mood' SET 'mood' = :mood WHERE user_id = :user_id AND date = :date AND via = 'tracker'", mood=input, user_id=session["user_id"], date=day)
            setMood = rows[0]['mood']
        except:
            db.execute("INSERT INTO 'mood' (user_id, via, date, mood) VALUES (:user_id, :via, :date, :mood)", user_id=session['user_id'], via='tracker', date=day, mood=int(input))
            setMood = ""

        setMood = ""
        mood = db.execute("SELECT * FROM mood WHERE date = :date AND user_id = :user_id AND via = 'tracker' ",
                                    date=day, user_id=session['user_id'])
        try:
            setMood = mood[0]['mood']
        except:
            setMood = ""
        
            
        print(setMood)
        return render_template("den.html", open2 = True, setMood = setMood)
    
    #journal input 
    if request.method == "POST" and "journalQuestion" in request.form:
        # TODO add sentiment update 

        input = request.form.get('journalInput')
        day = DT.today()
        answer = ""
        journal_rows = []
        sentiment_results = {'neg': 0, 'neu': 0, 'pos': 0, 'compound': 0}


        userText = ""
        userText_rows = db.execute("SELECT * FROM journal WHERE date = :date AND user_id = :user_id AND author = 'Me' ",
                                    date=day, user_id=session['user_id'])
        for row in userText_rows:
            userText = userText + " " + row['text']

        print(userText)

        #based on the words used in the sentence, a sentiment is analyzed
        print("This is VADER")
        sentiment_results = sia.polarity_scores(userText)
        print(sentiment_results)
        print()
        sentiment =  (sentiment_results['compound'] + 1)/2*5 #use ai for this 

        apiKey = db.execute("SELECT * FROM journal WHERE date = :date AND user_id = :user_id AND author = 'api'",
                                        date=day, user_id=session['user_id'])
        
        # currently my Bard is not conversational TODO
        try:
            os.environ['_BARD_API_KEY']=apiKey[0]['text']
        except:
            flash("Oh no! Your bard API token is missing :( ")

        try: 
            answer = Bard().get_answer(input)['content']
        except: 
            flash("Oh no! Your bard API token may be inactive :( ")

        if not input.isspace() and answer != "":
            db.execute("INSERT INTO journal (user_id, text, date, author) VALUES(:user_id, :text, :date, 'Me')",
                 user_id = session['user_id'], text = input, date=day)
            db.execute("INSERT INTO journal (user_id, text, date, author) VALUES(:user_id, :text, :date, 'AI')",
                 user_id = session['user_id'], text = answer, date=day)
        

        journal_rows = db.execute("SELECT * FROM journal WHERE date = :date AND user_id = :user_id AND author <> 'api' ",
                                        date=day, user_id=session['user_id'])
        
        if sentiment_results['neg'] == 0 and sentiment_results['neu'] == 0 and sentiment_results['pos'] == 0 :
                sentiment_results = {'neg': 1, 'neu': 1, 'pos': 1, 'compound': 0}

        return render_template("den.html", open3 = True, journal_rows=journal_rows, sentiment_results = sentiment_results)
    
    if request.method == "POST" and "apiKey" in request.form:
        # TODO add sentiment update
        input = request.form.get('api')
        day = DT.today()
        journal_rows = []
        sentiment_results = {'neg': 0, 'neu': 0, 'pos': 0, 'compound': 0}


        userText = ""
        userText_rows = db.execute("SELECT * FROM journal WHERE date = :date AND user_id = :user_id AND author = 'Me' ",
                                    date=day, user_id=session['user_id'])
        for row in userText_rows:
            userText = userText + " " + row['text']

        print(userText)

        #based on the words used in the sentence, a sentiment is analyzed
        print("This is VADER")
        sentiment_results = sia.polarity_scores(userText)
        print(sentiment_results)
        print()
        sentiment =  (sentiment_results['compound'] + 1)/2*5 #use ai for this 


        if input.isspace() or input == None or input == "":
            #replace with date code
            flash("Plese enter an api key :)")  
        
        
        rows = db.execute("SELECT * FROM journal WHERE user_id = :user_id AND author = 'api' ", user_id=session["user_id"])
        if len(rows) > 0:
            print("updateed api key")
            db.execute("UPDATE 'journal' SET 'text' = :text WHERE user_id = :user_id AND date = :date AND author = 'api' ", text=input, user_id=session["user_id"], date=day)
        else:
            db.execute("INSERT INTO journal (user_id, text, date, author) VALUES(:user_id, :text, :date, 'api')",
                 user_id = session['user_id'], text = input, date=day)   
        
        journal_rows = db.execute("SELECT * FROM journal WHERE date = :date AND user_id = :user_id AND author <> 'api' ",
                                        date=day, user_id=session['user_id'])
        
        if sentiment_results['neg'] == 0 and sentiment_results['neu'] == 0 and sentiment_results['pos'] == 0 :
                sentiment_results = {'neg': 1, 'neu': 1, 'pos': 1, 'compound': 0}

        return render_template("den.html", open3 = True, journal_rows=journal_rows, sentiment_results = sentiment_results)

    # opening views 
    if request.method == "POST" and "updateView" in request.form:
        input = request.form.get('updateViewHid')
        
        if input == "open": #todo list
            rows = db.execute("SELECT * FROM 'todo' WHERE user_id = ?", session["user_id"])
            print(rows)
            return render_template("den.html", rows=rows, open=True)
            
        if input == "open2": #mood tracker
            
            day = DT.today()
            setMood = ""
            mood = db.execute("SELECT * FROM mood WHERE date = :date AND user_id = :user_id AND via = 'tracker'",
                                        date=day, user_id=session['user_id'])
            try:
                setMood = mood[0]['mood']
            except:
                setMood = ""
            print(setMood)

            return render_template("den.html", setMood=setMood, open2 = True)
        
        if input == "open3": #journal
            
            print("open3")
            day = DT.today()
            sentiment_results = {'neg': 0, 'neu': 0, 'pos': 0, 'compound': 0}

            journal_rows = db.execute("SELECT * FROM journal WHERE date = :date AND user_id = :user_id AND author <> 'api' ",
                                        date=day, user_id=session['user_id'])
            #delete all not in this date
            db.execute("DELETE FROM journal WHERE date <> :date", date=day) # ERROR? <> means not equal to 
            #mood setting TODO

            userText = ""
            userText_rows = db.execute("SELECT * FROM journal WHERE date = :date AND user_id = :user_id AND author = 'Me' ",
                                        date=day, user_id=session['user_id'])
            for row in userText_rows:
                userText = userText + " " + row['text']

            print(userText)

            #based on the words used in the sentence, a sentiment is analyzed
            print("This is VADER")
            sentiment_results = sia.polarity_scores(userText)
            print(sentiment_results)
            print()
            sentiment =  (sentiment_results['compound'] + 1)/2*5 #use ai for this 


            mood_rows = db.execute("SELECT * FROM mood WHERE user_id = :user_id AND date = :date AND via = 'journal' ", user_id=session["user_id"], date=day)
            if len(mood_rows) > 0:
                print("updateed mood")
                db.execute("UPDATE 'mood' SET 'mood' = :mood WHERE user_id = :user_id AND date = :date AND via = :via", mood=sentiment, user_id=session["user_id"], date=day, via="journal")
            else:
                db.execute("INSERT INTO 'mood' (user_id, via, date, mood) VALUES (:user_id, :via, :date, :mood)", user_id=session['user_id'], via='journal', date=day, mood=int(sentiment)) 
        
            if sentiment_results['neg'] == 0 and sentiment_results['neu'] == 0 and sentiment_results['pos'] == 0 :
                sentiment_results = {'neg': 1, 'neu': 1, 'pos': 1, 'compound': 0}
            return render_template("den.html", open3 = True, journal_rows = journal_rows, sentiment_results = sentiment_results)
        
        if input == "open4": #chart
            day = DT.today()
            trackerDict = {}
            journalDict = {}
            moodX_array = []
            trackerY_array = []
            journalY_array = []

            moodX = " "
            trackerY = " "
            journalY = " "

            journal_mood_rows = db.execute("SELECT * FROM mood WHERE user_id = :user_id AND via = 'journal' ", user_id=session["user_id"])
            tracker_mood_rows = db.execute("SELECT * FROM mood WHERE user_id = :user_id AND via = 'tracker' ", user_id=session["user_id"])

            
            for row in journal_mood_rows:
                moodX_array.append(row['date'])
                journalDict[row['date']] = row['mood']
            for row in tracker_mood_rows:
                moodX_array.append(row['date'])
                trackerDict[row['date']] = row['mood']
            
            moodX_array = list(set(moodX_array))
            moodX_array.sort()
            for x in moodX_array:
                try: 
                    print(x)
                    journalY_array.append(journalDict[x])
                except KeyError:
                    journalY_array.append("null")
                try:
                    trackerY_array.append(trackerDict[x])
                except KeyError:
                    trackerY_array.append("null")

            print(moodX_array)
            for x in moodX_array:
                moodX = moodX + " " + str(x)
            for mood in trackerY_array:
                trackerY = trackerY + " " + str(mood)
            for mood in journalY_array:
                journalY = journalY + " " + str(mood)                

            print(trackerY)
            print(journalY)
            
            print("open4")

            # update mood
            userText = ""
            userText_rows = db.execute("SELECT * FROM journal WHERE date = :date AND user_id = :user_id AND author = 'Me' ",
                                        date=day, user_id=session['user_id'])
            for row in userText_rows:
                userText = userText + " " + row['text']
            print("This is VADER")
            sentiment_results = sia.polarity_scores(userText)
            print(sentiment_results)
            print()
            sentiment =  (sentiment_results['compound'] + 1)/2*5 #use ai for this 
            print(sentiment)

            mood_rows = db.execute("SELECT * FROM mood WHERE user_id = :user_id AND date = :date AND via = 'journal' ", user_id=session["user_id"], date=day)
            if len(mood_rows) > 0:
                print("updateed mood")
                db.execute("UPDATE 'mood' SET 'mood' = :mood WHERE user_id = :user_id AND date = :date AND via = :via", mood=sentiment, user_id=session["user_id"], date=day, via="journal")
            else:
                db.execute("INSERT INTO 'mood' (user_id, via, date, mood) VALUES (:user_id, :via, :date, :mood)", user_id=session['user_id'], via='journal', date=day, mood=int(sentiment)) 
        


            return render_template("den.html", open4=True, moodX = moodX, journalY = journalY, trackerY = trackerY)
        
        
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
    