from flask import render_template
from flask_login import login_required, UserMixin

from logbook import logbook_bp
from logbook.controllers import get_log_content, get_logs, store_log
from logbook.models import LogItem


@logbook_bp.route("/", defaults={"page_nr": 1})
@logbook_bp.route("/<page_nr>")
@login_required
def index_next_pages(page_nr):
    items = get_logs(page_nr)
    return render_template("index.html", items=items, page_nr=int(page_nr))


@logbook_bp.route("/logs/<log_id>/edit", methods=["GET"])
@login_required
def get_log_entry(log_id):
    content = get_log_content(log_id)
    return render_template("edit_log.html", content=content, log_id=int(log_id))


@logbook_bp.route("/logs/new", methods=["GET"])
@login_required
def create_new_log():
    return render_template("new_log_form.html")
