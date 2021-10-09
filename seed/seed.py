import sys  # nopep8
sys.path.append(r'../src')  # nopep8

from app import db
from models import Person, Relationship, Greeting


db.drop_all()
db.create_all()

# create users (account holders)
Person.signup(email_address="m.smith@gmail.com", first_name="Matthew",
              last_name="Smith", img_url="", birthday="2000-01-01", username="m.smith", password="password1")
Person.signup(email_address="m.walker@gmail.com", first_name="Mark",
              last_name="Walker", img_url="", birthday="2001-02-02", username="m.walker", password="password2")
Person.signup(email_address="l.jenkins@gmail.com", first_name="Luke",
              last_name="Jenkins", img_url="", birthday="2002-03-03", username="l.jenkins", password="password3")
Person.signup(email_address="j.taylor@gmail.com", first_name="John",
              last_name="Taylor", img_url="", birthday="2003-04-04", username="j.taylor", password="password4")
Person.signup(email_address="j.rodriguez@gmail.com", first_name="James",
              last_name="Rodriguez", img_url="", birthday="2004-10-09", username="j.rodriguez", password="password5")

db.session.commit()

# create friends (non-account holders)
Person.signup(email_address="b.bauer@gmail.com", first_name="Beatrix",
              last_name="Bauer", img_url="", birthday="1976-10-09", username="", password="")
Person.signup(email_address="m.lyon@gmail.com", first_name="Marie",
              last_name="Lyon", img_url="", birthday="1999-04-22", username="", password="")
Person.signup(email_address="e.barrera@gmail.com", first_name="Erik",
              last_name="Barrera", img_url="", birthday="1982-10-12", username="", password="")
Person.signup(email_address="b.huerta@gmail.com", first_name="Bo",
              last_name="Huerta", img_url="", birthday="2010-05-02", username="", password="")
Person.signup(email_address="s.boyer@gmail.com", first_name="Susanna",
              last_name="Boyer", img_url="", birthday="1950-12-25", username="", password="")

db.session.commit()

greeting1 = Greeting(sender_id=1, recipient_id=2,
                     greeting="Hello! I'm so glad we met.")
greeting2 = Greeting(sender_id=1, recipient_id=3,
                     greeting="OH! It's been too long since we've seen each other.")
greeting3 = Greeting(sender_id=2, recipient_id=3, greeting="Miss you!")
greeting4 = Greeting(sender_id=4, recipient_id=5,
                     greeting="When is our next tea party?")
greeting5 = Greeting(sender_id=5, recipient_id=4,
                     greeting="Greetings! Let's meet up for coffee soon!")

db.session.add_all([greeting1, greeting2, greeting3, greeting4, greeting5])
db.session.commit()

relationship1 = Relationship(
    user_id=1, friend_id=2, relationship="brother")
relationship2 = Relationship(
    user_id=1, friend_id=3, relationship="brother")
relationship3 = Relationship(
    user_id=2, friend_id=3, relationship="brother")
relationship4 = Relationship(
    user_id=4, friend_id=5, relationship="spouse")
relationship5 = Relationship(user_id=4, friend_id=1, relationship="son")
relationship6 = Relationship(
    user_id=1, friend_id=8, relationship="cousin")
relationship7 = Relationship(
    user_id=1, friend_id=9, relationship="cousin")
relationship8 = Relationship(
    user_id=2, friend_id=10, relationship="cousin")
relationship9 = Relationship(
    user_id=4, friend_id=7, relationship="cousin")
relationship10 = Relationship(user_id=4, friend_id=6, relationship="cousin")

db.session.add_all([relationship1, relationship2,
                   relationship3, relationship4, relationship5, relationship6, relationship7, relationship8, relationship9, relationship10])
db.session.commit()
