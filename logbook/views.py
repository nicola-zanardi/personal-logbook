from flask import render_template

from logbook import app
from logbook.controllers import get_logs, store_log


@app.route("/", defaults={"page_nr": 1})
@app.route("/<page_nr>")
def index_next_pages(page_nr):
    items = get_logs(page_nr)
    return render_template("index.html", items=items, page_nr=int(page_nr))
