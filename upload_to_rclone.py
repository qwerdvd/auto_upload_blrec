import asyncio


async def rclone_upload(
        _filepath: str,
        room_id: int,
        name: str,
        rclone_dir: str,
        time_data: str,
        delete_local: bool
):
    if delete_local:
        rclone_cmd = f'rclone move {_filepath} {rclone_dir}{room_id}_{name}/{time_data}'
    else:
        rclone_cmd = f'rclone copy {_filepath} {rclone_dir}{room_id}_{name}/{time_data}'
    proc = await asyncio.create_subprocess_shell(
        rclone_cmd,
        stdout=asyncio.subprocess.PIPE,
        stderr=asyncio.subprocess.PIPE
    )
    stdout, stderr = await proc.communicate()
    if stdout:
        print(f'[stdout]\n{stdout.decode()}')
    if stderr:
        print(f'[stderr]\n{stderr.decode()}')
