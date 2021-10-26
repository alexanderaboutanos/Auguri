import time
from flask import Flask, render_template, redirect, request, session, flash, g
from sqlalchemy.orm import relationship
from models import Person, Relationship, Greeting, db, connect_db
from forms import EditFriendForm, SignUpForm, LoginForm, AddFriendForm, EditUserForm
from functions import get_friend_list, compile_flask_bday_objs, make_flask_bday_obj
from sqlalchemy.exc import IntegrityError
import os

app = Flask(__name__)

CURR_USER_KEY = "curr_user"

# app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get(
#     'DATABASE_URL', 'postgresql://auguri')
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get(
    'DATABASE_URL').replace("://", "ql://", 1)
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ECHO'] = False
app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = True
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', 'hellosecret1')


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
        except IntegrityError as e:
            flash("Username already taken", 'danger')
            return render_template('/not_auth/signup.html', form=form)

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

        if person:
            execute_login(person)
            return redirect('/birthdays')

        flash("Invalid credentials.", 'danger')

    return render_template('/not_auth/login.html', form=form)


@app.route('/logout')
def logout():
    """Handle logout of user."""
    execute_logout()
    return redirect("/")


###############################################################
#################### AUTH PAGES TO FOLLOW #####################
###############################################################

##########################  ABOUT  ############################

@app.route('/about')
def about():
    """show a quick about page explaining what Auguri is capable of. """

    if not g.person:
        return redirect("/")

    return render_template('/auth/about.html')

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

    greeting = Greeting.query.filter_by(recipient_id=friend.id).first()

    return render_template('/auth/friend_indv.html', friend=flask_bday_obj, greeting=greeting)


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

        if form.greeting.data != "":
            Greeting.query.filter_by(
                recipient_id=friend.id).delete()
            new_greeting = Greeting(
                recipient_id=friend.id,
                greeting=form.greeting.data
            )
            db.session.add(new_greeting)
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

        # if the user wanted to include a birthday greeting, add it here.
        if form.greeting:
            new_greeting = Greeting(
                recipient_id=new_friend.id,
                greeting=form.greeting.data
            )
            db.session.add(new_greeting)
            db.session.commit()

        new_rel = Relationship(
            user_id=g.person.id, friend_id=new_friend.id)
        db.session.add(new_rel)
        db.session.commit()

        return redirect("/")

    return render_template('/auth/friend_add.html', form=form)


@app.route('/friend/<int:friend_id>/delete', methods=['POST'])
def delete_friend(friend_id):
    """ delete friend. """

    # send back to homepage if not signed in.
    if not g.person:
        return redirect("/")

    # send to birthdays if user tries to delete himself
    if friend_id == g.person.id:
        return redirect("/")

    # get the info for the friend
    friend = Person.query.get(friend_id)

    # if the friend isn't actually a friend of the user.
    if friend not in get_friend_list(g.person.id):
        return redirect("/birthdays")

    # delete the friend
    db.session.delete(friend)
    db.session.commit()

    return redirect("/")

##########################  USER  ############################


@app.route('/user')
def user_details():
    """ Show personal user information. """

    # send back to homepage if not signed in.
    if not g.person:
        return redirect("/")

    # get your personal info
    user = g.person

    # prepare the user object for flask
    flask_bday_obj = make_flask_bday_obj(user)

    return render_template('/auth/user.html', user=flask_bday_obj)


@app.route('/user/edit', methods=['GET', 'POST'])
def edit_user():
    """ Edit information for your own account. """

    # send back to homepage if not signed in.
    if not g.person:
        return redirect("/")

    # load the form
    form = EditUserForm(obj=g.person)

    # Handle POST request with new friend data
    if form.validate_on_submit():
        try:
            g.person.email_address = form.email_address.data
            g.person.first_name = form.first_name.data
            g.person.last_name = form.last_name.data
            g.person.username = form.username.data
            g.person.img_url = form.img_url.data
            g.person.birthday = form.birthday.data
            db.session.commit()

        except IntegrityError as e:
            flash("Username already taken", 'danger')
            return render_template('/auth/user_edit.html', form=form)

        return redirect("/birthdays")

    return render_template('/auth/user_edit.html', form=form)


##########################  MESSAGES  ############################

@app.route('/greeting/<int:friend_id>/delete', methods=['GET'])
def delete_greeting(friend_id):
    """ delete greeting. """

    # send back to homepage if not signed in.
    if not g.person:
        return redirect("/")

    # get the info for the greeting
    friend = Person.query.get(friend_id)

    # send back birthdays if user is not the creator of this greeting
    if friend not in get_friend_list(g.person.id):
        return redirect("/birthdays")

    # delete the greeting
    Greeting.query.filter_by(
        recipient_id=friend.id).delete()
    db.session.commit()

    return redirect("/")
