import asyncio
from fastapi import BackgroundTasks


async def cmd(cmd: str, background_task=BackgroundTasks) -> None:
    # background_task.add_task(write_notification, email, message="test_message")
    proc = await asyncio.create_subprocess_exec(
        cmd,
        stdout=asyncio.subprocess.PIPE,
        stderr=asyncio.subprocess.PIPE
    )

    stdout, stderr = await proc.communicate()

    print(f'[{cmd!r} exited with {proc.returncode}]')
    if stdout:
        print(f'[stdout]\n{stdout.decode()}')
    if stderr:
        print(f'[stderr]\n{stderr.decode()}')
