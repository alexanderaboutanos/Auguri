from app import app
import os
from unittest import TestCase
from sqlalchemy import exc

from models import db, Greeting, Person, Relationship

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

    def test_1_person_model(self):
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

        # There should be no relationships, no greetings, and 3 test people.
        self.assertEqual(len(Greeting.query.all()), 0)
        self.assertEqual(len(Relationship.query.all()), 0)
        self.assertEqual(len(Person.query.all()), 3)

    def test_2_new_friend(self):
        p4 = Person.signup(email_address="test4@gmail.com", first_name="Test4_first",
                           last_name="Test4_last", username="", password="", img_url="", birthday="2004-04-04")
        pid4 = 1004
        p4.id = pid4
        db.session.commit()

        print('***********************************************')
        print(Person.query.all())
        print('***********************************************')

        new_rel = Relationship(user_id=1001, friend_id=1004)
        db.session.add(new_rel)
        db.session.commit()

        self.assertEqual(len(Relationship.query.all()), 1)
        self.assertEqual(p4.creator_rel[0].user_id, self.p1.id)

    def test_3_valid_signup(self):
        p5 = Person.signup(email_address="test5@gmail.com", first_name="Test5_first",
                           last_name="Test5_last", img_url="", birthday="2005-05-05", username="test5", password="password5")
        pid5 = 1005
        p5.id = pid5
        db.session.commit()

        p_test = Person.query.get(pid5)
        self.assertIsNotNone(p_test)
        self.assertEqual(p_test.username, "test5")
        self.assertEqual(p_test.email_address, "test5@gmail.com")
        self.assertNotEqual(p_test.password, "password5")
        # Bcrypt strings always start with $2b$
        self.assertTrue(p_test.password.startswith("$2b$"))

    def test_4_invalid_username_signup(self):
        invalid = Person.signup(email_address="test1@gmail.com", first_name="Test1_first",
                                last_name="Test1_last", img_url="", birthday="2001-01-01", username="test1", password="password1")
        with self.assertRaises(exc.IntegrityError) as context:
            db.session.commit()

    def test_5_valid_authentication(self):
        p = Person.authenticate(self.p1.username, "password1")
        self.assertIsNotNone(p)
        self.assertEqual(p.id, self.pid1)
