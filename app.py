from dotenv import load_dotenv

from fastapi import status, Request, FastAPI
from loggerController import logger

from model import BaseRecordModel
from handler.EventHandler import handle_event
from celery_app import handle_event as celery_handle_event

app = FastAPI()
background_tasks = set()
load_dotenv(verbose=True)


@app.post("/webhook")
async def get_record(call_back: Request, status_code=status.HTTP_200_OK):
    content_type = call_back.headers["content-type"]
    if content_type != "application/json":
        logger.error("Unsupported content-type application/json")

        return {"message": "Unsupported Media Type"}, status.HTTP_415_UNSUPPORTED_MEDIA_TYPE
    else:
        logger.info("Receive Webhook")

        data = await call_back.json()

    try:
        event = BaseRecordModel.create_event(**data)
        logger.info(f"GOT EVENT: {event.EventType}")
        celery_handle_event.apply_async(args=[event])

        await handle_event(event)

        return status_code
    except ValueError as e:
        logger.ValueError(e)

        return {"message": str(e)}, status.HTTP_400_BAD_REQUEST


@app.post("/handle_event")
async def hello():
    return {"message": "Hello World"}
