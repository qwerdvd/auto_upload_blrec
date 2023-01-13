from celery import Celery
from loggerController import logger
from model import BaseRecordModel
from config import settings

celery_app = Celery('tasks', broker='redis://localhost:6379/0')


@celery_app.task
def tgnotice(event_data):
    # Do something with event_data and send message to telegram
    pass


@celery_app.task
def rclone_upload(event_data):
    # Do something with event_data and upload to rclone
    pass


@celery_app.task
def upload_to_bilibili(event_data):
    # Do something with event_data and upload to bilibili
    pass


@celery_app.task
def handle_event(event: BaseRecordModel):
    # check if the event_data needs to be uploaded to bilibili
    if settings.UPLOAD_TO_BILIBILI:
        upload_to_bilibili.apply_async(args=[event])
    settings.USE_TG_NOTIFICATION.apply_async(args=[event])
    settings.UPLOAD_TO_RCLONE.apply_async(args=[event])
