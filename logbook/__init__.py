import os
from flask import Flask, Blueprint, redirect
from flask_assets import Environment, Bundle

app = Flask(__name__)
app.config.from_object("logbook.default_settings")
app.config.from_pyfile("../settings.cfg")
app.jinja_env.trim_blocks = True
app.jinja_env.lstrip_blocks = True

# use blueprint to set base url
logbook_bp = Blueprint(
    "logbook", __name__, template_folder="templates", static_folder="static"
)


assets = Environment(app)
css = Bundle(
    "vendor/semantic-ui/semantic.css",
    "css/pygments.css",
    "css/main.css",
    filters="cleancss",
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
