import asyncio
import os

from dotenv import load_dotenv
from fastapi import APIRouter, Request, status, HTTPException
from loggerController import logger
from server.config.config import config
from server.model.blrec_model import BaseBlrecWebhookEvent

from server.model.brec_model import BaseRecordModel
from server.tasks.video_process import BrecVideoProcess
from utils import file_operation

router = APIRouter()
load_dotenv()
work_dir = os.getenv("WORK_DIR")


@router.post("/webhook")
async def get_record(call_back: Request, status_code=status.HTTP_200_OK):
    content_type = call_back.headers["content-type"]
    user_agent = call_back.headers["user-agent"].split("/")[0]
    if content_type != "application/json":
        logger.error(f"Unsupported content-type {content_type}")
        # return {"message": "Unsupported Media Type"}, status.HTTP_415_UNSUPPORTED_MEDIA_TYPE
        raise HTTPException(status_code=status.HTTP_415_UNSUPPORTED_MEDIA_TYPE)

    data = await call_back.json()
    # config = file_operation.readYml(os.path.join(work_dir, 'config', 'config.yml'))
    # base_config = BaseConfig(config)

    if user_agent == "BililiveRecorder":
        logger.info("BililiveRecorder callback")

        event = BaseRecordModel.create_event(**data)
        logger.info(f"EventId: {event.EventId} | EventType: {event.EventType}")

        if event.EventType == "SessionStarted":
            asyncio.create_task(BrecVideoProcess.session_start(event))
        elif event.EventType == "FileOpening":
            # asyncio.create_task(notify(event))
            pass
        elif event.EventType == "SessionEnded":
            # asyncio.create_task(notify(event))
            pass

    elif user_agent == "blrec":
        logger.info("blrec callback")

        event = BaseBlrecWebhookEvent.create_event(**data)
        logger.info(f"EventId: {event.id} | EventType: {event.type}")

        # TODO: 增加对blrec的webhook的处理
    else:
        logger.error(f"Unsupported user-agent {user_agent}")
        # return {"message": "Unsupported Media Type"}, status.HTTP_415_UNSUPPORTED_MEDIA_TYPE
        raise HTTPException(status_code=status.HTTP_415_UNSUPPORTED_MEDIA_TYPE)

    return status_code
