import humanize
import markdown2
import uvicorn
from fastapi import FastAPI
from model import Item, LogItem
from starlette.responses import HTMLResponse

app = FastAPI()


@app.post("/logs", status_code=201)
async def store_log(item: Item):
    print(item)
    item = LogItem(content=item.text)
    item.save()
    item.timestamp = f'{item.timestamp.strftime("%m-%d-%Y %H:%M:%S")} ({humanize.naturaldelta(item.timestamp)} ago)'
    item.content = markdown2.markdown(item.content)
    return item


@app.get("/logs")
async def get_logs(page=1,):
    items = list(LogItem.select().order_by(LogItem.id.desc()).paginate(int(page)))
    for item in items:
        item.timestamp = f'{item.timestamp.strftime("%m-%d-%Y %H:%M:%S")} ({humanize.naturaldelta(item.timestamp)} ago)'
        item.content = markdown2.markdown(item.content)
    return items


@app.get("/", response_class=HTMLResponse)
async def read_items():
    with open("view/index.html") as html_index:
        return html_index.read()

if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=8000, log_level="info")
