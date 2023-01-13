import os
import platform

from dotenv import load_dotenv

from handler.utils.upload_to_rclone import upload_to_rclone
from loggerController import logger
from model import BaseRecordModel

load_dotenv(verbose=True)
UPLOAD_TO_RCLONE = os.getenv("UPLOAD_TO_RCLONE")
UPLOAD_TO_BILIBILI = os.getenv("UPLOAD_TO_BILIBILI")
rclone_dir = os.getenv("RCLONE_DIR")
work_dir = os.getenv("BLREC_WORK_DIR")


async def handle_file_path(event: BaseRecordModel) -> tuple:
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
    _filepath, dir_path, file_name, time_data = await handle_file_path(event)
    if UPLOAD_TO_RCLONE:
        rclone_command = f'rclone move {dir_path}/{_filepath}* {rclone_dir}{event.EventData.RoomId}_{event.EventData.Name}/{time_data}'
        logger.info(f"EventId: {event.EventId} | Rclone Command: {rclone_command}")

        result = upload_to_rclone(event, rclone_command, _filepath, file_name)
        if result:
            logger.info(f"EventId: {event.EventId} | Upload To Rclone Success")
        else:
            logger.error(
                f"EventId: {event.EventId} | Upload To Rclone Failed! Please Check! | "
                f"Rclone Command: {rclone_command} | File Path: {_filepath}"
            )
    if UPLOAD_TO_BILIBILI:
        # await upload_to_bilibili(event)
        pass
