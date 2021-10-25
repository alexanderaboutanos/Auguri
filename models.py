""" This python file holds the SQLAlchemy models for the Auguri app. """

from enum import unique
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from sqlalchemy.orm import backref

db = SQLAlchemy()
bcrypt = Bcrypt()


class Person(db.Model):
    """ This is the model for all people (account holders and non-account holders). """

    __tablename__ = 'people'

    id = db.Column(
        db.Integer,
        primary_key=True,
        autoincrement=True
    )

    email_address = db.Column(
        db.Text,
        nullable=False
    )

    first_name = db.Column(
        db.Text,
        nullable=False
    )

    last_name = db.Column(
        db.Text,
        nullable=False
    )

    img_url = db.Column(
        db.Text,
        default='../static/images/default_person_img.jpeg'
    )

    birthday = db.Column(
        db.Date,
        nullable=False
    )

    username = db.Column(
        db.Text,
        nullable=True,
        unique=True
    )

    password = db.Column(
        db.Text,
        nullable=False
    )

    def __repr__(self):
        return f"Person #{self.id}: {self.first_name} {self.last_name}, {self.email_address}, {self.birthday}"

    @classmethod
    def signup(cls, email_address, first_name, last_name, img_url, birthday, username, password):
        """ Creates a new person in the database.

        If no username and password are present, the person is added as a 'friend'. 
        If a username or password is present, the person is added as a 'user'.

        Users will have their passwords hashed. """

        if username != "":
            pwd = bcrypt.generate_password_hash(password).decode('UTF-8')
        else:
            username = None
            pwd = ""

        person = Person(
            email_address=email_address,
            first_name=first_name,
            last_name=last_name,
            img_url=img_url,
            birthday=birthday,
            username=username,
            password=pwd
        )

        db.session.add(person)
        return person

    @classmethod
    def authenticate(cls, username, password):
        """ Attempts to find a person with the input username and password. """

        person = cls.query.filter_by(username=username).first()

        if person:
            is_auth = bcrypt.check_password_hash(person.password, password)
            if is_auth:
                return person

        return False

    @staticmethod
    def is_user(username):
        """ checks if a Person is a user (account-holder). 

        returns True if the Person has a username
        returns False if the Person does not.

        """

        if username:
            return True
        return False


class Relationship(db.Model):
    """ This is the model for the relationships between people """

    __tablename__ = 'relationships'

    id = db.Column(
        db.Integer,
        primary_key=True,
        autoincrement=True
    )

    user_id = db.Column(
        db.Integer,
        db.ForeignKey('people.id', ondelete='CASCADE')
    )

    friend_id = db.Column(
        db.Integer,
        db.ForeignKey('people.id', ondelete='CASCADE')
    )

    person_user = db.relationship(
        'Person', foreign_keys=[user_id])
    person_friend = db.relationship(
        'Person', backref='creator_rel', foreign_keys=[friend_id])


class Greeting(db.Model):
    """ This is the model for all greetings. """

    __tablename__ = 'greetings'

    id = db.Column(
        db.Integer,
        primary_key=True,
        autoincrement=True
    )

    recipient_id = db.Column(
        db.Integer,
        db.ForeignKey('people.id', ondelete='CASCADE')
    )

    greeting = db.Column(
        db.Text
    )


def connect_db(app):
    """ Connect this database with the Flask app."""
    db.app = app
    db.init_app(app)
    return app
