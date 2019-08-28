from model import LogItem, Item
from fastapi import FastAPI
import uvicorn
from starlette.responses import HTMLResponse

app = FastAPI()


@app.post("/logs", status_code=201)
async def store_log(item: Item):
    print(item)
    item = LogItem(content=item.text)
    item.save()
    return item


@app.get("/logs")
async def get_logs():
    items = list(LogItem.select().order_by(LogItem.id.desc()))
    return items


@app.get("/", response_class=HTMLResponse)
async def read_items():
    with open("view/index.html") as html_index:
        return html_index.read()

if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=8000, log_level="info")
