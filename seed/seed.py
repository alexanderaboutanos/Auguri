
import sys
sys.path.append(
    r'/Users/alexanderaboutanos/Desktop/Coding/SpringBoard/Auguri/src')

from models import Person, Relationship, Greeting
from app import db


db.drop_all()
db.create_all()

Person.signup(email_address="m.smith@gmail.com", first_name="Matthew",
              last_name="Smith", img_url="", birthday="2000-01-01", username="m.smith", password="password1")
Person.signup(email_address="m.walker@gmail.com", first_name="Mark",
              last_name="Walker", img_url="", birthday="2001-02-02", username="m.walker", password="password2")
Person.signup(email_address="l.jenkins@gmail.com", first_name="Luke",
              last_name="Jenkins", img_url="", birthday="2002-03-03", username="l.jenkins", password="password3")
Person.signup(email_address="j.taylor@gmail.com", first_name="John",
              last_name="Taylor", img_url="", birthday="2003-04-04", username="j.taylor", password="password4")
Person.signup(email_address="j.rodriguez@gmail.com", first_name="James",
              last_name="Rodriguez", img_url="", birthday="2004-05-05", username="j.rodriguez", password="password5")

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
    person1_id=1, person2_id=2, relationship="brother")
relationship2 = Relationship(
    person1_id=1, person2_id=3, relationship="brother")
relationship3 = Relationship(
    person1_id=2, person2_id=3, relationship="brother")
relationship4 = Relationship(person1_id=4, person2_id=5, relationship="spouse")
relationship5 = Relationship(person1_id=4, person2_id=1, relationship="son")

db.session.add_all([relationship1, relationship2,
                   relationship3, relationship4, relationship5])
db.session.commit()
