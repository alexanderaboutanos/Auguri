from app import app
import os
from unittest import TestCase
from sqlalchemy import exc

from models import db, Person

# use a test db
os.environ['DATABASE_URL'] = "postgresql:///auguri-test"


# create the tables, once for all tests. for each test, we will delete all data and add new.
db.create_all()


class PersonModelTestCase(TestCase):
    """ Test the Person Model """

    def setUp(self):
        db.drop_all()
        db.create_all()

        p1 = Person.signup(email_address="test1@gmail.com", first_name="Test1_first",
                           last_name="Test1_last", img_url="", birthday="2001-01-01", username="test1", password="password1")
        pid1 = 1001
        p1.id = pid1

        p2 = Person.signup(email_address="test2@gmail.com", first_name="Test2_first",
                           last_name="Test2_last", img_url="", birthday="2002-02-02", username="test2", password="password2")
        pid2 = 1002
        p2.id = pid2

        db.session.commit()

        p1 = Person.query.get(pid1)
        p2 = Person.query.get(pid2)

        self.p1 = p1
        self.pid1 = pid1

        self.p2 = p2
        self.pid2 = pid2

        self.client = app.test_client()

    def tearDown(self):
        res = super().tearDown()
        db.session.rollback()
        return res

    def test_person_model(self):
        """Does the basic model work?"""

        p = Person(
            email_address="test3@gmail.com",
            first_name="Test3_first",
            last_name="Test3_last",
            img_url="",
            birthday="2003-03-03",
            username="test3",
            password="password3")

        db.session.add(p)
        db.session.commit()

        # Person should only have 1 listed birthday
        self.assertEqual(len(u.messages), 0)
