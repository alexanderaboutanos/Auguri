
# ***********************************************************************
# ***************************** CRON JOB ********************************
# ***********************************************************************

# This python file uses CRONJOB to run daily at 00:00 (midnight)
# If not already, the following cron job should be placed into the TERMINAL...
# 0 0 * * * /Users/alexanderaboutanos/Desktop/Coding/SpringBoard/Auguri/venv/bin/python3 /Users/alexanderaboutanos/Desktop/Coding/Springboard/Auguri/src/api.py

# SHOULD WE DO SOMETHING WITH THIS? cron = CronTab('username') ?????????

# ***********************************************************************
# **************************** START API ********************************
# ***********************************************************************


# using SendGrid's Python Library
# https://github.com/sendgrid/sendgrid-python
import os
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail
from models import db, Person, Greeting, Relationship
from app import app
from dotenv import load_dotenv
from functions import num_days_until_bday

# get the token from .env
load_dotenv()
token = os.environ.get("api-token")


def check_for_birthdays():
    """ check if today is someone's bday. compile list of todays bdays """

    # Filter through PEOPLE and compile a list of bdays (users and/or friends).
    People = (Person.query.all())
    todays_bdays = [
        person for person in People if num_days_until_bday(person.birthday) == 0]

    # if there are no bdays, just return
    if todays_bdays == []:
        return False

    # else, prep the appropriate emails and continue
    prep_appropriate_emails(todays_bdays)
    return todays_bdays


def prep_appropriate_emails(todays_bdays):
    """ determine which emails should be sent, and call those emails to be sent. """

    # prep two lists, one to contain user bdays and another to contain friend bdays.
    user_bdays = []
    friend_bdays = []

    # slot todays_bdays into either USER list or FRIEND list.
    for person in todays_bdays:
        if Person.is_user(person.username):
            user_bdays.append(person)
        else:
            friend_bdays.append(person)

    # grab all the greetings
    greetings = (Greeting.query.all())

    # call for the appropriate emails to be sent.

    # for friend bdays, if that friend has a custom greeting waiting for them, an email is sent directly to the friend, with that greeting. If that friend does not have a custom greeting waiting for them, that friend's user will be reminded of their friend's bday.
    for birthday_person in friend_bdays:

        # check if a personal greeting should be sent.
        for greeting in greetings:
            if birthday_person.id == greeting.recipient_id:

                # send birthday greeting to that friend
                send_email(
                    sender_id=0,
                    recipient_id=birthday_person.id,
                    subject="Happy Birthday!",
                    body=f"{greeting.greeting}")

                # tell the user that you sent this 'greeting' to the friend
                send_email(
                    sender_id=0,
                    recipient_id=greeting.sender_id,
                    subject="Email sent!",
                    body=f"Auguri sent the following email to {birthday_person.first_name} {birthday_person.last_name}. Message: {greeting.greeting}")

                # delete the greeting so it doesn't repeat next year
                db.session.delete(greeting)
                db.session.commit()

                continue

        # If no personal message was prepared to send the friend, remind their corresponding user to send them an email.

        relationship = Relationship.query.filter_by(
            friend_id=birthday_person.id).first()
        corresponding_user = relationship.person_user

        send_email(
            sender_id=0,
            recipient_id=corresponding_user,
            subject="Auguri Bday Reminder",
            body=f"Don't forget! {birthday_person.first_name} {birthday_person.last_name} has a birthday today. Send them a message!")

    # for user bdays, users will be congratulated from the auguri APP
    for birthday_person in user_bdays:
        send_email(
            sender_id=0,
            recipient_id=birthday_person.id,
            subject="Happy Birthday!",
            body="From everyone here at Auguri Inc, we want to wish you a happy birthday!")

    return {'user_bdays': user_bdays, 'friend_bdays': friend_bdays}


def send_email(sender_id, recipient_id, subject, body):
    """ send an email. """

    message = Mail(
        from_email='app.auguri@gmail.com',
        to_emails=f'{Person.recipient_id.email_address}',
        subject=subject,
        html_content=body)

    try:
        sg = SendGridAPIClient(token)
        response = sg.send(message)
        print(response.status_code)
        print(response.body)
        print(response.headers)
    except Exception as e:
        print(e.message)


# START THE API. Called each midnight.
check_for_birthdays()
