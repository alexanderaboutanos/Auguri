from flask import Flask, render_template, redirect, request, session, flash, g
from models import Person, Relationship, Greeting, db, connect_db
from forms import SignUpForm, LoginForm, AddFriendForm

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
    return render_template('/not_auth/signup.html')


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

        return redirect('/')

    return render_template('/not_auth/login.html', form=form)


# AUTH PAGES TO FOLLOW

@app.route('/')
def birthdays():
    """show birthdays"""
    return render_template('/auth/birthdays.html')
