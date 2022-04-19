from email.policy import default
from pydoc_data.topics import topics
from flask import Flask, redirect, render_template, request, session, flash
from flask_sqlalchemy import SQLAlchemy
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, PasswordField
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
# class User(db.Model):
#     id= db.Column(db.Integer, primary_key = True)
#     email= db.Column(db.String(500), nullable = False, unique = True)
#     username= db.Column(db.String(200), nullable = False, unique = True)
#     password= db.Column(db.String(200), nullable = False)
#     date_added= db.Column(db.DateTime, default=datetime.utcnow)

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

# UserForm for index
class UserForm(FlaskForm):
    username = StringField("", validators=[DataRequired()])
    email = StringField("", validators=[DataRequired()])
    password = PasswordField("", validators=[DataRequired()])
    submit = SubmitField("Submit")

# sign-in portal
@app.route("/")
def signin():
    # for credential screening to verify account is valid
    username = None
    password = None
    form = UserForm

    return render_template("signin.html", form = form)

# sign up page
@app.route("/add/user")
def signup():
    # for Regex to sign up
    username = None
    password = None
    form = UserForm()

    # validate form
    if form.validate_on_submit():
        # queries User db for any matches on inputed email info
        user = User.query.filter_by(email=form.email.data).first()
        if user is None:
            user = User(username=form.username.data, password=form.username.data, email=form.email.data)
            db.session.add(user)
            db.session.commit()
        username = form.username.data
        form.username.data = ''
        form.email.data = ''
        form.password.data = ''
        flash("User Added Successfully!")
    
    our_users = User.query.order_by(User.date_added)
    return render_template("test_add.html", 
        form = form,
        username = username,
        our_users = our_users)

@app.route("/index")
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


