from flask import Flask, redirect, render_template, request
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

# from sqlalchemy.sql import func

app = Flask(__name__)


app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///chats.db'


# initialize the database
db = SQLAlchemy(app)

#Create DB Model

class Chats(db.Model):
    id= db.Column(db.Integer, primary_key = True)
    message= db.Column(db.String(200), nullable = False)
    username= db.Column(db.String(200), nullable = False)
    topic= db.Column(db.String(200), nullable = False)

    # created_at= db.Column(db.DateTime, default= datetime)


# function to return a string when we addsomething
    def __repr__(self):
        return '<Name %r>' % self.id

TOPICS = [
    "games",
    "sports",
    "entertainment",
    "other"
]

name = ""

@app.route("/")
def index():
    return render_template("index.html", topics = TOPICS)

@app.route("/changename",  methods=["POST"])
def changename():
    global name
    name = request.form.get("username")
    print(name)
    return redirect("/games")


@app.route("/games", methods=["POST", "GET"])
def games():
    global name
    if request.method == "POST":
        if name != "":
            chat_message = request.form.get("message")
            username = name
            new_chats = Chats(username=name, message=chat_message, topic="games")
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
    
    game_messages = Chats.query.filter_by(topic='games').order_by(Chats.id)
    return render_template("games.html", topics = TOPICS, messages= game_messages, username = name)

@app.route("/sports", methods=["POST", "GET"])
def sports():
    global name
    if request.method == "POST":
        if name != "":
            chat_message = request.form.get("message")
            username = name
            new_chats = Chats(username=name, message=chat_message, topic="sports")
            try:
                db.session.add(new_chats)
                db.session.commit()
                return redirect("/sports")
            except: 
                return render_template("error.html", message = "There was an error adding the user" )
        else:
            return render_template("error.html", message = "Username has to not be blank" )
    
    game_messages = Chats.query.filter_by(topic='sports').order_by(Chats.id)
    return render_template("sports.html", topics = TOPICS, messages= game_messages, username = name)

@app.route("/entertainment", methods=["POST", "GET"])
def entertaiment():
    global name
    if request.method == "POST":
        if name != "":
            chat_message = request.form.get("message")
            username = name
            new_chats = Chats(username=name, message=chat_message, topic="entertainment")
            try:
                db.session.add(new_chats)
                db.session.commit()
                return redirect("/entertainment")
            except: 
                return render_template("error.html", message = "There was an error adding the user" )
        else:
            return render_template("error.html", message = "Username has to not be blank" )
    
    game_messages = Chats.query.filter_by(topic='entertainment').order_by(Chats.id)
    return render_template("entertainment.html", topics = TOPICS, messages= game_messages, username = name)


@app.route("/other", methods=["POST", "GET"])
def other():
    global name
    if request.method == "POST":
        if name != "":
            chat_message = request.form.get("message")
            username = name
            new_chats = Chats(username=name, message=chat_message, topic="other")
            try:
                db.session.add(new_chats)
                db.session.commit()
                return redirect("/other")
            except: 
                return render_template("error.html", message = "There was an error adding the user" )
        else:
            return render_template("error.html", message = "Username has to not be blank" )
    
    game_messages = Chats.query.filter_by(topic='other').order_by(Chats.id)
    return render_template("other.html", topics = TOPICS, messages= game_messages, username = name)