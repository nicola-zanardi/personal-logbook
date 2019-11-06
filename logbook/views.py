from flask import render_template

from logbook import app
from logbook.controllers import get_logs, store_log, get_log_content
from logbook.models import LogItem


@app.route("/", defaults={"page_nr": 1})
@app.route("/<page_nr>")
def index_next_pages(page_nr):
    items = get_logs(page_nr)
    return render_template("index.html", items=items, page_nr=int(page_nr))


@app.route("/logs/<log_id>/edit", methods=["GET"])
def get_log_entry(log_id):
    content = get_log_content(log_id)
    return render_template("edit_log.html", content=content, log_id=int(log_id))

