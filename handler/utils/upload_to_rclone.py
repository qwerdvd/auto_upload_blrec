import datetime
import subprocess

from loggerController import logger
from model import BaseRecordModel


# def upload_to_rclone(
#         event: BaseRecordModel,
#         rclone_command: str,
#         _filepath: str,
# ) -> bool:
#     log_file_name = f"log/rclone_log/rclone-{event.EventData.RoomId}-{datetime.datetime.now().strftime('%Y-%m-%d')}.log"
#     logger.add(log_file_name)
#
#     proc = subprocess.run(rclone_command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
#     stdout = proc.stdout.decode()
#     stderr = proc.stderr.decode()
#     if proc.returncode != 0:
#         logger.error(f"EventId: {event.EventId} | Rclone Upload Failed")
#         logger.error(f"EventId: {event.EventId} | Rclone Upload Failed | Stdout: {stdout}")
#         logger.error(f"EventId: {event.EventId} | Rclone Upload Failed | Stderr: {stderr}")
#         return False
#     else:
#         logger.info(f"EventId: {event.EventId} | Rclone Upload Success")
#         logger.info(f"EventId: {event.EventId} | Rclone Upload Success | Stdout: {stdout}")
#         logger.info(f"EventId: {event.EventId} | Rclone Upload Success | Stderr: {stderr}")
#         return True
