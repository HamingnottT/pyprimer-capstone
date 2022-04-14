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
    "entertaiment",
    "other"
]


@app.route("/")
def index():
    return render_template("index.html", topics = TOPICS)



@app.route("/games", methods=["POST", "GET"])
def games():
    if request.method == "POST":
        chat_message = request.form.get("message")
        username = "John"
        topic = "games"
        new_chats = Chats(username="John", message=chat_message, topic="games")
        try:
            # print(new_chats.username)
            # print(new_chats.message)
            db.session.add(new_chats)
            db.session.commit()
            print("worked")
            return redirect("/games")
        except: 
            return render_template("error.html", message = "There was an error adding the user" )
    
    game_messages = Chats.query.filter_by(topic='games').order_by(Chats.id)

    return render_template("games.html", topics = TOPICS, messages= game_messages)