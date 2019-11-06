import humanize
from logbook.models import LogItem
from logbook import app
import markdown2
from flask import jsonify, request, redirect


@app.route("/logs", methods=["POST"])
def store_log():
    item = LogItem(content=request.form["text"])
    item.save()
    return redirect("/")


def get_logs(page=1):
    items = list(LogItem.select().order_by(LogItem.id.desc()).paginate(int(page)))
    response = []
    for item in items:
        row = {}
        row["id"] = item.id
        row[
            "timestamp"
        ] = f'{item.timestamp.strftime("%m-%d-%Y %H:%M:%S")} ({humanize.naturaldelta(item.timestamp)} ago)'
        row["content"] = (
            markdown2.markdown(item.content, extras=["fenced-code-blocks"])
            .strip()
            .replace("<img", '<img class="ui image"')
        )
        response.append(row)
    return response


def get_log_content(log_id):
    log = LogItem.get(LogItem.id == log_id)
    return log.content


@app.route("/logs/<log_id>/edit", methods=["POST"])
def update_log_content(log_id):
    new_content = request.form["text"]
    log = LogItem.get(LogItem.id == log_id)
    log.content = new_content
    log.save()
    return redirect("/")


# deleting with a post as forms do not support DELETE and I
# am trying to stay javascript-free
@app.route("/logs/<log_id>/delete", methods=["POST"])
def delete_log_entry(log_id):
    log = LogItem.get(LogItem.id == log_id)
    log.delete_instance()
    return redirect("/")
