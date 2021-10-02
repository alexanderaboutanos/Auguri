from flask import Flask, render_template

from models import Person, Relationship, Greeting, db, connect_db

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///auguri'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ECHO'] = False
app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = True
app.config['SECRET_KEY'] = "abc123"


# to show paths
# app.config['EXPLAIN_TEMPLATE_LOADING'] = True

connect_db(app)

# db.drop_all()
# db.create_all()


def var1():
    print('10')


@app.route('/')
def homepage():
    """show homepage"""
    return render_template('base.html')
