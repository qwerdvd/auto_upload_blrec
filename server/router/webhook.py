import asyncio
import os

from dotenv import load_dotenv
from fastapi import APIRouter, Request, status, HTTPException
from loggerController import logger
from server.config.config import RoomConfig
from server.model.blrec_model import BaseBlrecWebhookEvent

from server.model.brec_model import BaseRecordModel
from server.tasks.video_process import BrecVideoProcess, session_end, file_closed, stream_started, stream_ended

router = APIRouter()
load_dotenv()
work_dir = os.getenv("WORK_DIR")


@router.post("/webhook")
async def get_record(call_back: Request, status_code=status.HTTP_200_OK):
    content_type = call_back.headers["content-type"]
    user_agent = call_back.headers["user-agent"].split("/")[0]
    if content_type != "application/json":
        logger.error(f"Unsupported content-type {content_type}")
        raise HTTPException(status_code=status.HTTP_415_UNSUPPORTED_MEDIA_TYPE)

    data = await call_back.json()

    if user_agent == "BililiveRecorder":
        logger.info("BililiveRecorder callback")

        event = BaseRecordModel.create_event(**data)
        logger.info(f"EventId: {event.EventId} | EventType: {event.EventType}")

        if event.EventType == "SessionStarted":  # 开始录制
            asyncio.create_task(BrecVideoProcess.session_start(event))
        elif event.EventType == "SessionEnded":  # 结束录制
            room_config = RoomConfig.init(work_dir, event)
            asyncio.create_task(session_end(event))
        elif event.EventType == "FileOpening":  # 开始写入文件
            asyncio.create_task(BrecVideoProcess.file_opening(event))
        elif event.EventType == "FileClosed":  # 文件关闭
            asyncio.create_task(file_closed(event))
        elif event.EventType == "StreamStarted":  # 直播开始
            asyncio.create_task(stream_started(event))
        elif event.EventType == "StreamEnded":  # 直播结束
            asyncio.create_task(stream_ended(event))
        else:
            logger.error(f"Unknown event type: {event.EventType}")

    elif user_agent == "blrec":
        logger.info("blrec callback")

        event = BaseBlrecWebhookEvent.create_event(**data)
        logger.info(f"EventId: {event.id} | EventType: {event.type}")

        # TODO: 增加对blrec的webhook的处理
    else:
        logger.error(f"Unsupported user-agent {user_agent}")
        raise HTTPException(status_code=status.HTTP_415_UNSUPPORTED_MEDIA_TYPE)

    return status_code
