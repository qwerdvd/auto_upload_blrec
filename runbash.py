import os
import platform

from dotenv import load_dotenv
from upload_to_bilibili import upload_to_bilibili
from upload_to_rclone import rclone_upload

load_dotenv(verbose=True)

work_dir = os.getenv('BLREC_WORK_DIR')
rclone_dir = os.getenv('RCLONE_DIR')
delete_local = bool(os.getenv('DELETE_LOCAL'))
upload_to_bili = os.getenv('UPLOAD_TO_BILI')


async def run_bash(filepath, room_id, name, title):
    sys_str = platform.system()
    file_data = filepath.split('/')[-1].split('-')[2]
    time_data = file_data[:4] + '-' + file_data[4:6] + '-' + file_data[6:8]
    file_name = filepath.split('.')[-2].split('/')[-1]
    print(file_name)
    if sys_str == "Windows":
        _filepath = work_dir + filepath.replace('/', '\\')
        print(_filepath)
    else:
        _filepath = work_dir + filepath
    if os.path.exists(_filepath):
        if upload_to_bili:
            await upload_to_bilibili(_filepath, room_id, title, time_data)
        await rclone_upload(_filepath, room_id, name, rclone_dir, time_data, delete_local)
    else:
        print('文件不存在')


async def add_file_list(file_list, file, work_dir):
    for file_name in os.listdir(work_dir):
        if file in file_name and os.path.isfile(file_name):
            file_list.append(file_name)
    file_list = sorted(file_list)
    return file_list
