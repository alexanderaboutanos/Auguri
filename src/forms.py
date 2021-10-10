from flask_wtf import FlaskForm
from wtforms import Form, BooleanField, PasswordField, StringField, DateField, validators
from wtforms.validators import DataRequired, Email, Length, Optional


class SignUpForm(FlaskForm):
    """ Form used to signup a new user. """

    email_address = StringField('Email Address', validators=[
                                DataRequired(), Email()])
    first_name = StringField('First Name', validators=[DataRequired()])
    last_name = StringField('Last Name', validators=[DataRequired()])
    img_url = StringField('Personal Image URL (Optional)',
                          validators=[Optional()])
    birthday = DateField('Birthday', validators=[DataRequired()])
    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])


class LoginForm(FlaskForm):
    """ Form used to login an existing user. """
    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])


class AddFriendForm(FlaskForm):
    """ Form used for a signedin user to add a friend. """

    email_address = StringField('Email Address', validators=[
                                DataRequired(), Email()])
    first_name = StringField('First Name', validators=[DataRequired()])
    last_name = StringField('Last Name', validators=[DataRequired()])
    img_url = StringField('Image URL (Optional)', validators=[Optional()])
    birthday = DateField('Birthday', validators=[DataRequired()])


class EditFriendForm(FlaskForm):
    """ Form used for a signedin user to add a friend. """

    email_address = StringField('Email Address', validators=[
                                DataRequired(), Email()])
    first_name = StringField('First Name', validators=[DataRequired()])
    last_name = StringField('Last Name', validators=[DataRequired()])
    img_url = StringField('Image URL (Optional)', validators=[Optional()])
    birthday = DateField('Birthday', validators=[DataRequired()])
