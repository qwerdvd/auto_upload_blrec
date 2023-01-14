import os
import platform

# from celery.result import AsyncResult

from server.tasks.upload.upload_to_rclone import upload_to_rclone
from loggerController import logger
from utils.model.record_model import BaseRecordModel
from config import settings

# from celery_app import rclone_upload


def handle_file_path(event: BaseRecordModel) -> tuple[str, str, str]:
    file_data = event.EventData.RelativePath.split('/')[-1].split('-')[2]
    file_name = event.EventData.RelativePath.split('.')[-2].split('/')[-1]
    logger.info(f"EventId: {event.EventId} | Time Data: {event.EventData.TimeData}")

    sys_str = platform.system()
    if sys_str == "Windows":
        _filepath = str(settings.BLREC_WORK_DIR + event.EventData.RelativePath.replace('/', '\\'))
    else:
        _filepath = str(settings.BLREC_WORK_DIR + event.EventData.RelativePath)
    logger.info(f"EventId: {event.EventId} | Platform: {sys_str} | File Path: {_filepath}")

    dir_path = os.path.dirname(_filepath)

    return _filepath, dir_path, file_name


async def handle_upload(event: BaseRecordModel) -> None:
    _filepath, dir_path, file_name = handle_file_path(event)
    if settings.UPLOAD_TO_RCLONE:
        local_path = f'{dir_path}/{file_name}.flv'
        remote_path = f'{event.EventData.RoomId}_{event.EventData.Name}/{event.EventData.TimeData}'
        rclone_command = f'rclone move "{local_path}" {settings.RCLONE_DIR}"{remote_path}"'
        logger.info(f"EventId: {event.EventId} | Rclone Command: {rclone_command}")

        upload_to_rclone(event, rclone_command, _filepath)
        # result = rclone_upload.apply_async(args=[_filepath, file_name, remote_path])
        # logger.info(f"EventId: {event.EventId} | Rclone Result: {result.ready()}")
        # result = AsyncResult(task.id)
        # task_result = await result
        # logger.info(f"EventId: {event.EventId} | Task Result: {task_result}")
    if settings.UPLOAD_TO_BILIBILI:
        # await upload_to_bilibili(event)
        pass
