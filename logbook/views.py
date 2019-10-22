from flask import render_template

from logbook import app
from logbook.controllers import get_logs, store_log


@app.route("/")
def index():
    items = get_logs()
    return render_template("index.html", items=items)
