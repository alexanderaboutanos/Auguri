""" This python file holds the SQLAlchemy models for the Auguri app. """

from enum import unique
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt

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
        db.String(75),
        nullable=False
    )

    first_name = db.Column(
        db.String(50),
        nullable=False
    )

    last_name = db.Column(
        db.String(50),
        nullable=False
    )

    img_url = db.Column(
        db.Text,
        default='static/images/default_person_img.jpeg'
    )

    birthday = db.Column(
        db.Date,
        nullable=False
    )

    username = db.Column(
        db.String(75),
        nullable=False,
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
        """ Creates a new person (remembering to hash the password). """

        hash_pwd = bcrypt.generate_password_hash(password).decode('UTF-8')

        person = Person(
            email_address=email_address,
            first_name=first_name,
            last_name=last_name,
            img_url=img_url,
            birthday=birthday,
            username=username,
            password=hash_pwd
        )

        db.session.add(person)
        return person


class Relationship(db.Model):
    """ This is the model for the relationships between people """

    __tablename__ = 'relationships'

    id = db.Column(
        db.Integer,
        primary_key=True,
        autoincrement=True
    )

    person1_id = db.Column(
        db.Integer,
        db.ForeignKey('people.id')
    )

    person2_id = db.Column(
        db.Integer,
        db.ForeignKey('people.id')
    )

    relationship = db.Column(
        db.Text
    )


class Greeting(db.Model):
    """ This is the model for all greetings. """

    __tablename__ = 'greetings'

    id = db.Column(
        db.Integer,
        primary_key=True,
        autoincrement=True
    )

    sender_id = db.Column(
        db.Integer,
        db.ForeignKey('people.id')
    )

    recipient_id = db.Column(
        db.Integer,
        db.ForeignKey('people.id')
    )

    greeting = db.Column(
        db.Text
    )


def connect_db(app):
    """ Connect this database with the Flask app."""
    db.app = app
    db.init_app(app)
    return app
