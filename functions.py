import datetime
from models import Relationship, Greeting
from flask import g


def get_friend_list(user_id):
    """ Make an array of all 'friends' of a given user.

    This function takes a given user id, and filters through the relationship list, creating an array of all people which that user has added as a friend. Using that array of relationships, the function turns the relationships into persons and returns that array. 
    """

    relationship_lst = (Relationship.query.filter(
        Relationship.user_id == user_id).all())

    friend_lst = [r.person_friend for r in relationship_lst]
    return friend_lst


def compile_flask_bday_objs(friend_lst):
    """ prepare birthday object data which will be sent to flask. """

    # add yourself to list
    friend_lst.append(g.person)

    # for each friend, pull only certain information to be sent to flask
    unsorted_bday_objs = []
    for person in friend_lst:
        bday_obj = make_flask_bday_obj(person)
        unsorted_bday_objs.append(bday_obj)

    # sort birthday objects by the num days until their birthday
    flask_bday_objs = sorted(
        unsorted_bday_objs, key=lambda d: d['countdown'])

    # if the countdown is 0, replace the number with 'happy birthday'!
    for obj in flask_bday_objs:
        if obj['countdown'] == 0:
            obj['countdown'] = 'HAPPY BIRTHDAY!!!'

    return flask_bday_objs


def make_flask_bday_obj(person):
    """ take certain pieces from the 'person' class to be sent to flask."""
    bday_obj = {
        'id': person.id,
        'first_name': person.first_name,
        'last_name': person.last_name,
        'img_url': person.img_url,
        'countdown': num_days_until_bday(person.birthday),
        'age': how_old(person.birthday),
        'birthday': person.birthday.strftime("%B %d, %Y"),
        'greeting': Greeting.query.filter_by(recipient_id=person.id).first(),
        'username': person.username
    }
    return bday_obj


def num_days_until_bday(birthday):
    """ This function calculates the # of days until the bday occurs. 
    The birthday object is received in datetime format."""

    today = datetime.date.today()
    next_bday = birthday.replace(year=today.year)
    if next_bday < today:
        next_bday = birthday.replace(year=today.year + 1)

    time_to_bday = next_bday - today
    num_days_until_bday = time_to_bday.days

    if num_days_until_bday == 365:
        num_days_until_bday = 0

    return num_days_until_bday


def how_old(birthday):
    """ This function calculates age."""

    today = datetime.date.today()
    age = today.year - birthday.year - \
        ((today.month, today.day) < (birthday.month, birthday.day))

    return age
