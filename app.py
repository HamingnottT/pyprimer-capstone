from flask import Flask, redirect, render_template, request, session
from flask_sqlalchemy import SQLAlchemy
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired
from datetime import datetime
from flask_session import Session
from sqlalchemy.sql import func

app = Flask(__name__)


app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///chats.db'
# setting up the session
app.config['SESSION_PERMANENT']= False
app.config['SESSION_TYPE']= "filesystem" 



# initialize the database
db = SQLAlchemy(app)
Session(app)
#Create DB Model

#New Admin table in db for username and password storage
class User(db.Model):
    id= db.Column(db.Integer, primary_key = True)
    username= db.Column(db.String(200), nullable = False, unique = True)
    password= db.Column(db.String(200), nullable = False)

class Chats(db.Model):
    id= db.Column(db.Integer, primary_key = True)
    message= db.Column(db.String(200), nullable = False)
    username= db.Column(db.String(200), db.ForeignKey("user.username"), nullable = False)
    topic= db.Column(db.String(200), nullable = False)
    time_created = db.Column(db.DateTime(timezone=True), server_default=func.now())

    # created_at= db.Column(db.DateTime, default= datetime)


# function to return a string when we addsomething
    def __repr__(self):
        return '<Name %r>' % self.id

# ------------------Jake was here-----------------------
# Form classes to add usernames to database

class UserForm(FlaskForm):
    username = StringField("Username", validators=[DataRequired()])
    password = StringField("Password", validators=[DataRequired()])
    submit = SubmitField("Submit")

# ------------------------------------------------------

TOPICS = [
    "games",
    "sports",
    "entertainment",
    "other"
]




@app.route("/")
def index():
    return render_template("index.html", topics = TOPICS)

@app.route("/changename",  methods=["POST"])
def changename():
    session["name"]= request.form.get("username")
    if not session.get("page"):
        session["page"] = "games"
        return redirect("/games")
    target_page = "/"+ session["page"]
    return redirect(target_page)

# ------------------------------------------------------

@app.route("/user/add", methods=["POST", "GET"])
def add_user():
    form = UserForm()
    return render_template("add_user.html", form=form)

# ------------------------------------------------------

@app.route("/games", methods=["POST", "GET"])
def games():
    if request.method == "POST":
        if  session["name"] != "":
            chat_message = request.form.get("message")
            username = session["name"]
            new_chats = Chats(username=username, message=chat_message, topic="games")
            try:
                # print(new_chats.username)
                # print(new_chats.message)
                db.session.add(new_chats)
                db.session.commit()
                print("worked")
                return redirect("/games")
            except: 
                return render_template("error.html", message = "There was an error adding the user" )
        else:
            return render_template("error.html", message = "Username has to not be blank" )
    if not session.get("name"):
        session["name"]=""
    username = session.get("name")
    session["page"] = "games"
    game_messages = Chats.query.filter_by(topic='games').order_by(Chats.id)
    return render_template("games.html", topics = TOPICS, messages= game_messages, username = username)




@app.route("/sports", methods=["POST", "GET"])
def sports():
    if request.method == "POST":
        if  session["name"] != "":
            chat_message = request.form.get("message")
            username = session["name"]
            new_chats = Chats(username=username, message=chat_message, topic="sports")
            try:
                db.session.add(new_chats)
                db.session.commit()
                return redirect("/sports")
            except: 
                return render_template("error.html", message = "There was an error adding the user" )
        else:
            return render_template("error.html", message = "Username has to not be blank" )
    if not session.get("name"):
        session["name"]=""
    username = session.get("name")
    session["page"] = "sports"
    game_messages = Chats.query.filter_by(topic='sports').order_by(Chats.id)
    return render_template("sports.html", topics = TOPICS, messages= game_messages, username = username)

@app.route("/entertainment", methods=["POST", "GET"])
def entertaiment():
    if request.method == "POST":
        if  session["name"] != "":
            chat_message = request.form.get("message")
            username =  session["name"]
            new_chats = Chats(username=username, message=chat_message, topic="entertainment")
            try:
                db.session.add(new_chats)
                db.session.commit()
                return redirect("/entertainment")
            except: 
                return render_template("error.html", message = "There was an error adding the user" )
        else:
            return render_template("error.html", message = "Username has to not be blank" )
    if not session.get("name"):
        session["name"]=""
    username = session.get("name")
    session["page"] = "entertainment"
    game_messages = Chats.query.filter_by(topic='entertainment').order_by(Chats.id)
    return render_template("entertainment.html", topics = TOPICS, messages= game_messages, username = username)


@app.route("/other", methods=["POST", "GET"])
def other():
    if request.method == "POST":
        if  session["name"] != "":
            chat_message = request.form.get("message")
            username = session["name"]
            new_chats = Chats(username=username, message=chat_message, topic="other")
            try:
                db.session.add(new_chats)
                db.session.commit()
                return redirect("/other")
            except: 
                return render_template("error.html", message = "There was an error adding the user" )
        else:
            return render_template("error.html", message = "Username has to not be blank" )
    if not session.get("name"):
        session["name"]=""
    username = session.get("name")
    session["page"] = "other"
    game_messages = Chats.query.filter_by(topic='other').order_by(Chats.id)
    return render_template("other.html", topics = TOPICS, messages= game_messages, username = username)
