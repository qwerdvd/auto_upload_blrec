import datetime
import glob
import subprocess

from celery import Celery
from loggerController import logger
from model import BaseRecordModel
from config import settings

celery_app = Celery('tasks', broker='redis://localhost:6379/0', backend='redis://localhost:6379/0')

file_types = ['*.flv', '*.xml', '*.jpg']


# def after_return_callback(status, retval, task_id, args, kwargs, einfo):
#     logger.info(f"Task {task_id} completed with result {retval}")


@celery_app.task
def tgnotice(event: BaseRecordModel):
    # Do something with event_data and send message to telegram
    pass


@celery_app.task(bind=True)
def rclone_upload(self, _filepath: str, file_name: str, remote_path: str):
    for file_type in file_types:
        files = glob.glob(_filepath + file_name + file_type)
        for file in files:
            rclone_command = f"rclone move {file} {remote_path}"
            print(rclone_command)
            logger.info(f"TaskId: {self.request.id} | Rclone Command: {rclone_command}")
            subprocess.run(rclone_command)

    return {"Upload Successful"}


@celery_app.task
def upload_to_bilibili(event: BaseRecordModel):
    # Do something with event_data and upload to bilibili
    pass


@celery_app.task
def handle_event(event: BaseRecordModel):
    if settings.USE_TG_NOTIFICATION:
        tgnotice.apply_async(args=[event])
    settings.USE_TG_NOTIFICATION.apply_async(args=[event])
    if event.EventType == "StreamEnded":
        if settings.UPLOAD_TO_BILIBILI and settings.UPLOAD_TO_RCLONE:
            upload_to_bilibili.apply_async(args=[event])
            rclone_upload.apply_async(args=[event])
        elif settings.UPLOAD_TO_RCLONE:
            rclone_upload.apply_async(args=[event])
