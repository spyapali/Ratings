"""Movie Ratings."""

from jinja2 import StrictUndefined

from flask import Flask, render_template, redirect, request, flash, session
from flask_debugtoolbar import DebugToolbarExtension

from model import User, Rating, Movie, connect_to_db, db


app = Flask(__name__)

# Required to use Flask sessions and the debug toolbar
app.secret_key = "ABC"

# Normally, if you use an undefined variable in Jinja2, it fails silently.
# This is horrible. Fix this so that, instead, it raises an error.
app.jinja_env.undefined = StrictUndefined


@app.route("/")
def index():
    """Homepage."""

    return render_template("homepage.html")


@app.route("/users")
def user_list():
    """Show list of users."""

    users = User.query.all()
    return render_template("user_list.html", users=users)


@app.route("/login")
def show_login_form():
    """Show login form."""

    return render_template("login.html")


@app.route("/process_login", methods=["POST"])
def process_user_login():
    """Log in existing users, otherwise add new user."""

    # EXISTING USERS
    # adding userid to session. 
    # Redirect back to homepage, with flash message saying "logged in"
    # Logged out route is flash message, removing userid from session. 
    username = request.form.get("username")
    password = request.form.get("password")
    user = User.query.filter_by(email=username).one()   # naming variables username vs. email?
    user.user_id


    # NEW USERS
    # check if user with username exists in database (should not)
    # add user to database


if __name__ == "__main__":
    # We have to set debug=True here, since it has to be True at the point
    # that we invoke the DebugToolbarExtension
    app.debug = True

    connect_to_db(app)

    # Use the DebugToolbar
    DebugToolbarExtension(app)

    app.run()
