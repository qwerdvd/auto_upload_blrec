import asyncio

from fastapi import status, Request, FastAPI
from loggerController import logger

from utils.model.record_model import BaseRecordModel
from server.tasks.pushnotify.pushnotify import notify


app = FastAPI()
app.upload_queue = asyncio.Queue()


@app.post("/webhook")
async def get_record(call_back: Request, status_code=status.HTTP_200_OK):
    content_type = call_back.headers["content-type"]
    if content_type != "application/json":
        logger.error(f"Unsupported content-type {content_type}")

        return {"message": "Unsupported Media Type"}, status.HTTP_415_UNSUPPORTED_MEDIA_TYPE
    else:
        data = await call_back.json()

    try:
        event = BaseRecordModel.create_event(**data)
        logger.info(f"EventId: {event.EventId} | EventType: {event.EventType}")
        if event.EventType == "SessionStarted":
            asyncio.create_task(notify(event))
        elif event.EventType == "FileOpening":
            asyncio.create_task(notify(event))
        elif event.EventType == "SessionEnded":
            asyncio.create_task(notify(event))
        return status_code
    except ValueError as e:
        logger.ValueError(e)

        return {"message": str(e)}, status.HTTP_400_BAD_REQUEST
