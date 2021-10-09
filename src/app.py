import time
from flask import Flask, render_template, redirect, request, session, flash, g
from sqlalchemy.orm import relationship
from models import Person, Relationship, Greeting, db, connect_db
from forms import SignUpForm, LoginForm, AddFriendForm
from functions import num_days_until_bday, compile_birthday_friend_list

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


###############################################################
################### BEFORE EACH REQUEST #######################
###############################################################

@app.before_request
def update_global_variable():
    """ Check if the user is logged in on the session. If yes, add the user to Flask 'global'. Otherwise, keep the global value to None. """

    if CURR_USER_KEY in session:
        g.person = Person.query.get(session[CURR_USER_KEY])

    else:
        g.person = None


def execute_login(person):
    """ Login the person. """
    session[CURR_USER_KEY] = person.id


def execute_logout():
    """ Logout the person """
    if CURR_USER_KEY in session:
        del session[CURR_USER_KEY]

###############################################################
################# NOT-AUTH PAGES TO FOLLOW ####################
###############################################################


@app.route('/')
def welcome():
    """ Welcome page, with description of the app and with links to a login or signup. """
    return render_template('/not_auth/welcome.html')


@app.route('/signup', methods=['GET', 'POST'])
def signup():
    """ Shows page where user can sign up. Receives POST request upon signup attempt. """

    form = SignUpForm()

    if form.validate_on_submit():
        try:
            person = Person.signup(
                email_address=form.email_address.data,
                first_name=form.first_name.data,
                last_name=form.last_name.data,
                img_url=form.img_url.data,
                birthday=form.birthday.data,
                username=form.username.data,
                password=form.password.data
            )
            db.session.commit()
        except:
            return render_template('/not_auth/signup.html')

        execute_login(person)

        return redirect('/birthdays')

    return render_template('/not_auth/signup.html', form=form)


@app.route('/login', methods=['GET', 'POST'])
def login():
    """show homepage"""

    form = LoginForm()

    if form.validate_on_submit():
        try:
            person = Person.authenticate(
                username=form.username.data,
                password=form.password.data
            )
            db.session.commit()
        except:
            return render_template('/not_auth/login.html')

        execute_login(person)

        return redirect('/birthdays')

    return render_template('/not_auth/login.html', form=form)


###############################################################
#################### AUTH PAGES TO FOLLOW #####################
###############################################################

@app.route('/birthdays')
def birthdays():
    """show birthdays"""
    user_id = g.person.id
    birthday_lst = compile_birthday_friend_list(user_id)
    # The object is complete with first and last name, img_url, birthday, and a countdown # of days until their bday.
    return render_template('/auth/birthdays.html', birthday_lst=birthday_lst)
