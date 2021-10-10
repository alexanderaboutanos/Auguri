import time
from flask import Flask, render_template, redirect, request, session, flash, g
from sqlalchemy.orm import relationship
from models import Person, Relationship, Greeting, db, connect_db
from forms import EditFriendForm, SignUpForm, LoginForm, AddFriendForm
from functions import get_friend_list, compile_flask_bday_objs, make_flask_bday_obj

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
def load_user():
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
    if CURR_USER_KEY in session:
        return redirect("/birthdays")

    return render_template('/not_auth/welcome.html')


@app.route('/signup', methods=['GET', 'POST'])
def signup():
    """ Shows page where user can sign up. Receives POST request upon signup attempt. """

    if CURR_USER_KEY in session:
        del session[CURR_USER_KEY]

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
        person = Person.authenticate(
            username=form.username.data,
            password=form.password.data
        )

        execute_login(person)

        return redirect('/birthdays')

    return render_template('/not_auth/login.html', form=form)


@app.route('/logout')
def logout():
    """Handle logout of user."""
    execute_logout()
    return redirect("/")


###############################################################
#################### AUTH PAGES TO FOLLOW #####################
###############################################################

##########################  BIRTHDAY  ############################

@app.route('/birthdays')
def birthdays():
    """show birthdays"""

    if not g.person:
        return redirect("/")

    friend_lst = get_friend_list(g.person.id)
    flask_bday_objs = compile_flask_bday_objs(friend_lst)
    return render_template('/auth/birthdays.html', flask_bday_objs=flask_bday_objs)

##########################  FRIEND  ############################


@app.route('/friend/<int:friend_id>')
def show_friend(friend_id):
    """ Show information for individual friend. """

    # send back to homepage if not signed in.
    if not g.person:
        return redirect("/")

    # send to user_edit if user tries to edit himself
    if friend_id == g.person.id:
        return redirect("/user/edit")

    # get the info for the friend
    friend = Person.query.get(friend_id)

    # if the friend isn't actually a friend of the user, send user back to birthday page.
    if friend not in get_friend_list(g.person.id):
        return redirect("/birthdays")

    # prepare the friend object for flask
    flask_bday_obj = make_flask_bday_obj(friend)

    return render_template('/auth/friend_indv.html', friend=flask_bday_obj)


@app.route('/friend/<int:friend_id>/edit', methods=['GET', 'POST'])
def edit_friend(friend_id):
    """ Edit information for individual friend. """

    # send back to homepage if not signed in.
    if not g.person:
        return redirect("/")

    # send to user_edit if user tries to edit himself
    if friend_id == g.person.id:
        return redirect("/user/edit")

    # get the info for the friend
    friend = Person.query.get(friend_id)

    # if the friend isn't actually a friend of the user, send user back to birthday page.
    if friend not in get_friend_list(g.person.id):
        return redirect("/birthdays")

    # load the form
    form = EditFriendForm(obj=friend)

    # Handle POST request with new friend data
    if form.validate_on_submit():
        friend.email_address = form.email_address.data
        friend.first_name = form.first_name.data
        friend.last_name = form.last_name.data
        friend.img_url = form.img_url.data
        friend.birthday = form.birthday.data
        db.session.commit()
        return redirect(f"/friend/{friend.id}")

    return render_template('/auth/friend_indv_edit.html', form=form)


@app.route('/friend/add', methods=['GET', 'POST'])
def add_friend():
    """ add friend. """

    # send back to homepage if not signed in.
    if not g.person:
        return redirect("/")

    # load the form
    form = AddFriendForm()

    # Handle POST request with new friend data
    if form.validate_on_submit():
        new_friend = Person(
            email_address=form.email_address.data,
            first_name=form.first_name.data,
            last_name=form.last_name.data,
            img_url=form.img_url.data,
            birthday=form.birthday.data,
            username=None,
            password=""
        )
        db.session.add(new_friend)
        db.session.commit()

        print(new_friend)

        new_rel = Relationship(
            user_id=g.person.id, friend_id=new_friend.id, relationship="")
        db.session.add(new_rel)
        db.session.commit()

        return redirect("/")

    return render_template('/auth/friend_add.html', form=form)

##########################  USER  ############################
