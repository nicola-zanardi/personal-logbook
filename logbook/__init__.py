import os
from flask import Flask
from flask_assets import Environment, Bundle

app = Flask(__name__)
app.config.from_object("logbook.default_settings")
app.config.from_pyfile("../settings.cfg")

assets = Environment(app)
css = Bundle(
    "vendor/semantic-ui/semantic.css",
    "css/pygments.css",
    "css/main.css",
    filters="cleancss",
    output="gen/main.css",
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
