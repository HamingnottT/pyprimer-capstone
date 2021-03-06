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

# secret key for UserForm
from dev_utils import secret_key as sk

app = Flask(__name__)


app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///chats.db'
# setting up the session
app.config['SESSION_PERMANENT']= False
app.config['SESSION_TYPE']= "filesystem"

app.config['SECRET_KEY'] = sk.secret_key    #abstracted secret key


# initialize the database
db = SQLAlchemy(app)
Session(app)
#Create DB Model

#New Admin table in db for username and password storage
class User(db.Model):
    id= db.Column(db.Integer, primary_key = True)
    email= db.Column(db.String(500), nullable = False, unique = True)
    username= db.Column(db.String(200), nullable = False, unique = True)
    password= db.Column(db.String(200), nullable = False)
    date_added= db.Column(db.DateTime, default=datetime.utcnow)

class Chats(db.Model):
    id= db.Column(db.Integer, primary_key = True)
    message= db.Column(db.String(200), nullable = False)
    username= db.Column(db.String(200), db.ForeignKey("user.username"), nullable = False)
    topic= db.Column(db.String(200), nullable = False)
    time_created = db.Column(db.DateTime(timezone=True), server_default=func.now())


# function to return a string when we addsomething
    def __repr__(self):
        return '<Name %r>' % self.id

TOPICS = [
    "games",
    "sports",
    "entertainment",
    "other"
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
        if  session["name"] != "":
            chat_message = request.form.get("message")
            username = session["name"]
            page = session["page"]
            new_chats = Chats(username=username, message=chat_message, topic=page)
            try:
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


