from model import LogItem, Item
from fastapi import FastAPI
import uvicorn

app = FastAPI()


@app.post("/logs")
async def store_log(item: Item):
    print(item.text)
    item = LogItem(content=item.text)
    item.save()


@app.get("/logs")
async def get_logs():
    items = list(LogItem.select())
    return items

if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=8000, log_level="info", reload=True)