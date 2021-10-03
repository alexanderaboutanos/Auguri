from flask import Flask, render_template, redirect, request, session, flash, g

from models import Person, Relationship, Greeting, db, connect_db

app = Flask(__name__)

CURR_USER_KEY = "curr_user"

app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///auguri'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ECHO'] = False
app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = True
app.config['SECRET_KEY'] = "abc123"

# to show paths
# app.config['EXPLAIN_TEMPLATE_LOADING'] = True

connect_db(app)


@app.before_request()
def update_global_variable():
    """ Check if the user is logged in on the session. If yes, add the user to Flask 'global'. Otherwise, keep the global value to None. """

    if CURR_USER_KEY in session:
        g.person = Person.query.get(session[CURR_USER_KEY])

    else:
        g.person = None


# NOT AUTH PAGES TO FOLLOW


@app.route('/')
def welcome():
    """ Welcome page, with description of the app and with links to a login or signup. """
    return render_template('/not_auth/welcome.html')


def execute_login():


def execute_logout():


@app.route('/signup', methods=['GET', 'POST'])
def signup():
    """ Shows page where user can sign up. Receives POST request upon signup attempt. """
    return render_template('/not_auth/signup.html')


@app.route('/login', methods=['GET', 'POST'])
def login():
    """show homepage"""
    return render_template('/not_auth/login.html')


# AUTH PAGES TO FOLLOW

@app.route('/')
def birthdays():
    """show birthdays"""
    return render_template('/auth/birthdays.html')
