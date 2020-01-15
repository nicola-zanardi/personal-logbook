import os
from flask import Flask, Blueprint, redirect, url_for
from flask_assets import Environment, Bundle
from flask_login import LoginManager
from logbook.models import User
from logbook.helpers import get_random_border_style

app = Flask(__name__)
app.config.from_object("logbook.default_settings")
app.config.from_pyfile("../settings.cfg")
app.jinja_env.trim_blocks = True
app.jinja_env.lstrip_blocks = True

login_manager = LoginManager()
login_manager.login_view = "auth.login"
login_manager.init_app(app)


@login_manager.user_loader
def load_user(user_id):
    # since the user_id is just the primary key of our user table, use it in the query for the user
    return User.get_or_none(User.id == user_id)


# use blueprint to set base url
logbook_bp = Blueprint(
    "logbook", __name__, template_folder="templates", static_folder="static"
)


assets = Environment(app)
css = Bundle(
    "vendor/tailwind-css/tailwind.css",
    "css/pygments.css",
    # "css/main.css",
    output="{}/gen/main.css".format(app.config["BASE_URL"]),
)
assets.register("main_css", css)

if not app.debug:
    import logging
    from logging.handlers import TimedRotatingFileHandler

    # https://docs.python.org/3.6/library/logging.handlers.html#timedrotatingfilehandler
    file_handler = TimedRotatingFileHandler(
        os.path.join(app.config["LOG_DIR"], "logbook.log"), "midnight"
    )
    file_handler.setLevel(logging.WARNING)
    file_handler.setFormatter(
        logging.Formatter("<%(asctime)s> <%(levelname)s> %(message)s")
    )
    app.logger.addHandler(file_handler)

from logbook import controllers, views

app.register_blueprint(logbook_bp, url_prefix="/{}".format(app.config["BASE_URL"]))

from logbook.auth import auth

app.register_blueprint(auth, url_prefix="/{}".format(app.config["BASE_URL"]))

app.jinja_env.globals.update(get_random_border_style=get_random_border_style)


@app.route("/", defaults={"path": ""})
@app.route("/<path:path>")
def catch_all(path):
    """ Send any unmatched route to the login page """
    return redirect(url_for("auth.login"))
