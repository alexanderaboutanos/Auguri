import datetime
from models import Relationship


def compile_birthday_friend_list(user_id):
    """ Make an array of all 'friends' of a given user.

    This function takes a given user id, and filters through the relationship list, creating an array of all people which that user has added as a friend. Using that array of relationships, the function turns the relationships into persons and returns that array. 
    """

    relationship_lst = (Relationship.query.filter(
        Relationship.user_id == user_id).all())

    birthday_lst = [r.person_friend for r in relationship_lst]
    return birthday_lst


def num_days_until_bday(birthday):
    """ This function calculates the # of days until the bday occurs. 
    The birthday object is received in a YYYY-MM-DD format."""

    # bday_year = int(birthday[0:4])
    # bday_month = int(birthday[5:7])
    # bday_day = int(birthday[8:10])

    today = datetime.date.today()
    # bday = datetime.date(bday_year, bday_month, bday_day)
    bday = birthday

    next_bday = bday.replace(year=today.year + 1)
    time_to_bday = next_bday - today
    num_days_until_bday = time_to_bday.days

    if num_days_until_bday == 365:
        num_days_until_bday = 0

    return num_days_until_bday
