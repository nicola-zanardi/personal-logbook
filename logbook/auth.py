from flask import Blueprint, render_template, redirect, url_for, request, flash
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import login_user, logout_user, login_required
from logbook.models import User, db

auth = Blueprint("auth", __name__)


@auth.route("/login")
def login():
    return render_template("login.html")


@auth.route("/login", methods=["POST"])
def login_post():
    username = request.form.get("username")
    password = request.form.get("password")
    remember = True if request.form.get("remember") else False

    user = User.get_or_none(User.username == username)

    # check if user actually exists
    if user is None:
        return redirect(url_for("auth.login"))

    # take the user supplied password, hash it, and compare it to the hashed password in database
    if not user or not check_password_hash(user.password, password):
        flash("Please check your login details and try again.")
        return redirect(
            url_for("logbook.index_next_pages")
        )  # if user doesn't exist or password is wrong, reload the page

    # if the above check passes, then we know the user has the right credentials
    login_user(user, remember=remember)
    return redirect(url_for("logbook.index_next_pages"))


@auth.route("/signup")
def signup():
    return render_template("signup.html")


@auth.route("/signup", methods=["POST"])
def signup_post():

    username = request.form.get("username")
    password = request.form.get("password")

    user = User.get_or_none(
        User.username == username
    )  # if this returns a user, then the email already exists in database

    if user is not None:
        flash("Email address already exists")
        return redirect(url_for("auth.signup"))

    # create new user with the form data. Hash the password so plaintext version isn't saved.
    new_user = User(
        username=username, password=generate_password_hash(password, method="sha256")
    )
    new_user.save()

    return redirect(url_for("auth.login"))


@auth.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect(url_for("logbook.index_next_pages"))
