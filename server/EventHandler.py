from server.tasks.pushnotify.pushnotify import notify
from utils.model.record_model import BaseRecordModel
from server.tasks.upload.upload import handle_upload

# background_tasks = set()


# async def _handle_event(event: BaseRecordModel) -> None:
#     task = asyncio.create_task(_handle_event(event))
#     background_tasks.add(task)
#     task.add_done_callback(background_tasks.discard)
#
#     logger.info(f"Create Asyncio Task | Background_Tasks: {task} | {background_tasks}")


async def handle_event(event: BaseRecordModel) -> None:
    await notify(event)
    if event.EventType == "SessionEnded":
        await handle_upload(event)

    # logger.info(f"Create Asyncio Task | {background_tasks}")
