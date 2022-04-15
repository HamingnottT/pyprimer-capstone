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

# secret key for NameForm


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
# for mock index
import dev_utils.secret_key as sk           #this import is local

app.config['SECRET_KEY'] = sk.secret_key    #abstracted secret key

class NamerForm(FlaskForm):
    name = StringField("What's your name?", validators=[DataRequired()])
    submit = SubmitField("Submit")

@app.route("/name", methods=["GET", "POST"])
def name():
    name = None
    form = NamerForm()
    # validate form
    if form.validate_on_submit():
        name = form.name.data
        form.name.data = ""
    return render_template("mock_index.html",
        name = name,
        form = form)

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
        session["page"] = TOPICS[0]
        return redirect("/chat?page="+ session["page"])
    target_page = "/chat?page="+ session["page"]
    return redirect(target_page)

# ------------------------------------------------------
""" Not in use. May delete this code block. """

@app.route("/user/add", methods=["POST", "GET"])
def add_user():
    form = UserForm()
    return render_template("add_user.html", form=form)

# ------------------------------------------------------

@app.route("/chat", methods=["POST", "GET"])
def chat():
    if request.method == "POST":
        if  session["name"] != "":
            chat_message = request.form.get("message")
            username = session["name"]
            page = session["page"]
            new_chats = Chats(username=username, message=chat_message, topic=page)
            try:
                # print(new_chats.username)
                # print(new_chats.message)
                db.session.add(new_chats)
                db.session.commit()
                print("worked")
                return redirect("/chat?page="+page)
            except: 
                return render_template("error.html", message = "There was an error adding the user" )
        else:
            return render_template("error.html", message = "Username has to not be blank" )
    chatroom=False
    for topic in TOPICS:
        if topic == request.args.get("page"):
            session["page"] = request.args.get("page")
            chatroom=True
    if chatroom== False:
        return redirect("/chat?page="+ TOPICS[0])
    if not session.get("name"):
        session["name"]=""
    username = session.get("name")
    page = session.get("page")
    
    game_messages = Chats.query.filter_by(topic=page).order_by(Chats.id)
    return render_template("chat.html", topics = TOPICS, messages= game_messages, username = username, current_topic = page)


