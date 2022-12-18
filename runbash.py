import asyncio
import os
import platform
from dotenv import load_dotenv

load_dotenv(verbose=True)

work_dir = os.getenv('BLREC_WORK_DIR')
rclone_dir = os.getenv('RCLONE_DIR')
delete_local = os.getenv('DELETE_LOCAL')


async def run_bash(filepath, room_id, name):
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
        if delete_local:
            proc = await asyncio.create_subprocess_shell(
                f'rclone move {_filepath} {rclone_dir}{room_id}_{name}/{time_data}',
                stdout=asyncio.subprocess.PIPE,
                stderr=asyncio.subprocess.PIPE
            )
            stdout, stderr = await proc.communicate()
            if stdout:
                print(f'[stdout]\n{stdout.decode()}')
            if stderr:
                print(f'[stderr]\n{stderr.decode()}')
        else:
            proc = await asyncio.create_subprocess_shell(
                f'rclone copy {_filepath} {rclone_dir}{room_id}_{name}/{time_data}',
                stdout=asyncio.subprocess.PIPE,
                stderr=asyncio.subprocess.PIPE
            )
            stdout, stderr = await proc.communicate()
            if stdout:
                print(f'[stdout]\n{stdout.decode()}')
            if stderr:
                print(f'[stderr]\n{stderr.decode()}')
    else:
        print('文件不存在')
