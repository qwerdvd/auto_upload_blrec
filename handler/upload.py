import os
import platform

from celery.result import AsyncResult
from dotenv import load_dotenv

# from handler.utils.upload_to_rclone import upload_to_rclone
from loggerController import logger
from model import BaseRecordModel
from celery_app import rclone_upload

load_dotenv(verbose=True)
UPLOAD_TO_RCLONE = os.getenv("UPLOAD_TO_RCLONE")
UPLOAD_TO_BILIBILI = os.getenv("UPLOAD_TO_BILIBILI")
rclone_dir = os.getenv("RCLONE_DIR")
work_dir = os.getenv("BLREC_WORK_DIR")


def handle_file_path(event: BaseRecordModel) -> tuple[str, str, str, str]:
    file_data = event.EventData.RelativePath.split('/')[-1].split('-')[2]
    time_data = str(file_data[:4] + '-' + file_data[4:6] + '-' + file_data[6:8])
    file_name = event.EventData.RelativePath.split('.')[-2].split('/')[-1]
    logger.info(f"EventId: {event.EventId} | Time Data: {time_data}")

    sys_str = platform.system()
    if sys_str == "Windows":
        _filepath = str(work_dir + event.EventData.RelativePath.replace('/', '\\'))
    else:
        _filepath = str(work_dir + event.EventData.RelativePath)
    logger.info(f"EventId: {event.EventId} | Platform: {sys_str} | File Path: {_filepath}")

    dir_path = os.path.dirname(_filepath)

    return _filepath, dir_path, file_name, time_data


async def handle_upload(event: BaseRecordModel) -> None:
    _filepath, dir_path, file_name, time_data = handle_file_path(event)
    if UPLOAD_TO_RCLONE:
        remote_path = f'{rclone_dir}{event.EventData.RoomId}_{event.EventData.Name}/{time_data}'
        rclone_command = f'rclone move {dir_path}\\{file_name}.flv {rclone_dir}{event.EventData.RoomId}_{event.EventData.Name}/{time_data}'
        logger.info(f"EventId: {event.EventId} | Rclone Command: {rclone_command}")

        rclone_upload.apply_async(args=[_filepath, file_name, remote_path])
        # result = AsyncResult(task.id)
        # task_result = await result
        # logger.info(f"EventId: {event.EventId} | Task Result: {task_result}")
    if UPLOAD_TO_BILIBILI:
        # await upload_to_bilibili(event)
        pass
