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


@app.route("/process-login", methods=["POST"])
def process_user_login():
    """Log in existing users, otherwise redirect to sign up page."""

    # EXISTING USERS
    # adding userid to session. 
    # Redirect back to homepage, with flash message saying "logged in"
    # Logged out route is flash message, removing userid from session. 
    email = request.form.get("email")
    password = request.form.get("password")
    
    # If user is found in database (TRUE), add to sesssion, redirect to homepage
    # Else, add user to database, add to session, redirect to homepage
    user = User.query.filter_by(email=email, password=password).first()
    if user:
        user_id = user.user_id
        # print "user_id: %d" % (user_id)
        session[user_id] = True
        flash("Logged In")
        return redirect("/")
    else:
        flash("Sorry, you're not a registered user. Please sign up.")
        return redirect("/sign-up-form")

        
@app.route("/sign-up-form")
def show_sign_up_form():
    """Show sign up form for new users."""

    return render_template("sign_up_form.html")

    
@app.route("/sign-up", methods=["POST"])
def sign_up_new_user():
    """Add a new user to the database and session."""

    email = request.form.get("email")
    password = request.form.get("password")
    age = int(request.form.get("age"))
    zipcode = request.form.get("zipcode")
    
    new_user = User(email=email, password=password, age=age, zipcode=zipcode)
    # print "new_user: %s" % (new_user)
    db.session.add(new_user)
    db.session.commit()
    new_user_id = new_user.user_id
    # print "new_user_id: %d" % (new_user_id)
    session[new_user_id] = True 

    # NEW USERS
    # check if user with username exists in database (should not)
    # add user to database

    return redirect("/")



if __name__ == "__main__":
    # We have to set debug=True here, since it has to be True at the point
    # that we invoke the DebugToolbarExtension
    app.debug = True

    connect_to_db(app)

    # Use the DebugToolbar
    DebugToolbarExtension(app)

    app.run()
