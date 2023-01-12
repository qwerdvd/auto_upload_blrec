import os

from dotenv import load_dotenv

from handler.utils.upload_to_rclone import rclone_upload
from model import BaseRecordModel

load_dotenv(verbose=True)
UPLOAD_TO_RCLONE = os.getenv("UPLOAD_TO_RCLONE")
UPLOAD_TO_BILIBILI = os.getenv("UPLOAD_TO_BILIBILI")


async def handle_upload(event: BaseRecordModel) -> None:
    if UPLOAD_TO_RCLONE:
        await rclone_upload(event)
    if UPLOAD_TO_BILIBILI:
        await upload_to_bilibili(event)
