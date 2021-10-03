from flask_wtf import FlaskForm
from wtforms import Form, BooleanField, PasswordField, StringField, DateField, validators
from wtforms.validators import DataRequired, Email, Length


class SignUpForm(FlaskForm):
    """ Form used to signup a new user. """

    email_address = StringField('Email Address', validators=[
                                DataRequired(), Email()])
    first_name = StringField('First Name', validators=[DataRequired()])
    last_name = StringField('Last Name', validators=[DataRequired()])
    img_url = StringField('Personal Image URL (Optional)')
    birthday = DateField('Birthday', validators=[DataRequired()])
    username = StringField('', validators=[DataRequired()])
    password = PasswordField('', validators=[DataRequired()])


class AddFriendForm(FlaskForm):
    """ Form used for a signedin user to add a friend. """

    email_address = StringField('Email Address', validators=[
                                DataRequired(), Email()])
    first_name = StringField('First Name', validators=[DataRequired()])
    last_name = StringField('Last Name', validators=[DataRequired()])
    img_url = StringField('Personal Image URL (Optional)')
    birthday = DateField('Birthday', validators=[DataRequired()])
