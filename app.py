from flask import Flask, redirect, render_template, request, session
from flask_sqlalchemy import SQLAlchemy
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

class Chats(db.Model):
    __tablename__ = 'chat'
    id= db.Column(db.Integer, primary_key = True)
    message= db.Column(db.String(200), nullable = False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    topic= db.Column(db.String(200), nullable = False)
    time_created = db.Column(db.DateTime(timezone=True), server_default=func.now())

    def __repr__(self):
        return '<Name %r>' % self.id


class User(db.Model):
    __tablename__ = 'user'
    id= db.Column(db.Integer, primary_key = True)
    username= db.Column(db.String(200), nullable = False, unique = True)
    password= db.Column(db.String(200), nullable = False)
    # adimin= db.Column(db.String(200), nullable = False)
    # one to many
    chats = db.relationship("Chats", backref="user")
    def __repr__(self):
        return '<Name %r>' % self.id

# Topics can be it's own table
TOPICS = [
    "games",
    "sports",
    "entertainment",
    "other", 
]




@app.route("/")
def index():
    return render_template("index.html", topics = TOPICS)

@app.route("/new-user", methods=["POST", "GET"])
def new_user():
    if request.method == "POST": 
        # getting the information
        username = request.form.get("username")
        password = request.form.get("password")
        # checking user
        existing_check = User.query.filter_by(username=username).first()
        if existing_check:
            return render_template("newuser.html", error = "User already exists with that name")
        user = User(username=username, password = password)
        try:
            db.session.add(user)
            db.session.commit()
            print("worked")
            users = User.query
            for user in users:
                print(user.username)
                print(user.password)
            return render_template("index.html", message = "Registration Successful. Please sign in." )
        except: 
            return render_template("error.html", message = "There was an error adding the user" )
    return render_template("newuser.html")

@app.route("/sign-in", methods=["POST"])
def sign_in():
    username = request.form.get("username")
    password = request.form.get("password")
    user = User.query.filter_by(username=username).first()
    if user is None:
        return render_template("index.html", error = "No such user exists. Please try again." )
    if user.username == username and user.password == password:
        session["name"]=user.username
        session["id"]=user.id
        session["page"] =TOPICS[0]
        target_page = "/chat?page="+ session["page"]
        return redirect(target_page)
    return render_template("index.html", error = "Invalid Credentials. Try again." )


@app.route("/sign-out")
def sign_out():
    session["name"]=None
    session["id"]=None
    return redirect("/")


@app.route("/changename",  methods=["POST"])
def changename():
    session["name"]= request.form.get("username")
    if not session.get("page"):
        session["page"] = TOPICS[0]
        return redirect("/chat?page="+ session["page"])
    target_page = "/chat?page="+ session["page"]
    return redirect(target_page)


@app.route("/chat", methods=["POST", "GET"])
def chat():
    if request.method == "POST":
        if  session["id"] != None:
            chat_message = request.form.get("message")
            id = session["id"]
            page = session["page"]
            new_chats = Chats(user_id=id, message=chat_message, topic=page)
            try:
                db.session.add(new_chats)
                db.session.commit()
                return redirect("/chat?page="+page)
            except: 
                return render_template("error.html", message = "There was an error adding the user" )
        else:
            return render_template("error.html", message = "Username has to not be blank" )
    chatroom=False
    for topic in TOPICS:
        # getting the end of get query
        if topic == request.args.get("page"):
            session["page"] = request.args.get("page")
            chatroom=True
    if chatroom== False:
        return redirect("/chat?page="+ TOPICS[0])
    # checking if there is a user logged in
    if not session.get("name") or not session.get("id") :
        return render_template("index.html", message = "You must sign in to continue chatting." )
    username = session.get("name")
    page = session.get("page")
    game_messages = Chats.query.filter_by(topic=page).order_by(Chats.id).join(User)
    return render_template("chat.html", topics = TOPICS, messages= game_messages, username = username, current_topic = page)