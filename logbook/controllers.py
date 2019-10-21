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


def get_logs(page=1,):
    items = list(LogItem.select().order_by(LogItem.id.desc()).paginate(int(page)))
    response = []
    for item in items:
        row = {}
        row[
            "timestamp"
        ] = f'{item.timestamp.strftime("%m-%d-%Y %H:%M:%S")} ({humanize.naturaldelta(item.timestamp)} ago)'
        row["content"] = markdown2.markdown(item.content).strip()
        response.append(row)
    return response
