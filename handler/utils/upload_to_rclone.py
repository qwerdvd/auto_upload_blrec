import asyncio
import os
import platform

from .run_cmd import cmd
from loggerController import logger
from model import BaseRecordModel
from dotenv import load_dotenv

load_dotenv(verbose=True)
rclone_dir = os.getenv("RCLONE_DIR")
work_dir = os.getenv("BLREC_WORK_DIR")


async def configer_info(event: BaseRecordModel) -> tuple[str, str]:
    sys_str = platform.system()
    file_data = event.EventData.RelativePath.split('/')[-1].split('-')[2]
    time_data = str(file_data[:4] + '-' + file_data[4:6] + '-' + file_data[6:8])
    file_name = event.EventData.RelativePath.split('.')[-2].split('/')[-1]
    logger.info(f"EventId: {event.EventId} | Time Data: {time_data}")
    if sys_str == "Windows":
        _filepath = str(work_dir + event.EventData.RelativePath.replace('/', '\\'))
        logger.info(f"EventId: {event.EventId} | Platform: {sys_str} | File Path: {_filepath}")
    else:
        _filepath = str(work_dir + event.EventData.RelativePath)
        logger.info(f"EventId: {event.EventId} | Platform: {sys_str} | File Path: {_filepath}")

    return _filepath, time_data


async def rclone_upload(event: BaseRecordModel) -> None:
    _filepath, time_data = await configer_info(event)
    await cmd(
            f'rclone move {_filepath} {rclone_dir}{event.EventData.RoomId}_{event.EventData.Name}/{time_data}'
    )
