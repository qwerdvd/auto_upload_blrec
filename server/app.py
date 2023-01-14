import asyncio

from fastapi import status, Request, FastAPI
from loggerController import logger

from utils.model.record_model import BaseRecordModel
from server.EventHandler import handle_event
from server.tasks.pushnotify.pushnotify import notify

# from celery_app import handle_event as celery_handle_event, celery_app

app = FastAPI()
app.upload_queue = asyncio.Queue()


@app.post("/webhook")
async def get_record(call_back: Request, status_code=status.HTTP_200_OK):
    content_type = call_back.headers["content-type"]
    if content_type != "application/json":
        logger.error(f"Unsupported content-type {content_type}")

        return {"message": "Unsupported Media Type"}, status.HTTP_415_UNSUPPORTED_MEDIA_TYPE
    else:
        data = await call_back.json()

    try:
        event = BaseRecordModel.create_event(**data)
        logger.info(f"EventId: {event.EventId} | EventType: {event.EventType}")
        # celery_handle_event.apply_async(args=[event])
        # await handle_event(event)
        if event.EventType == "SessionStarted":
            asyncio.create_task(notify(event))
        elif event.EventType == "FileOpening":
            asyncio.create_task(notify(event))
        elif event.EventType == "SessionEnded":
            await handle_event(event)
        return status_code
    except ValueError as e:
        logger.ValueError(e)

        return {"message": str(e)}, status.HTTP_400_BAD_REQUEST

# @app.post("/handle_event")
# async def hello():
#     return {"message": "Hello World"}


# @app.get("/active_tasks")
# def active_tasks():
#     inspector = celery_app.control.inspect()
#     active_tasks = inspector.active()
#     if active_tasks:
#         task_id_list = [task['id'] for task in active_tasks[list(active_tasks.keys())[0]]]
#         return {"active_tasks": task_id_list}
#     else:
#         return {"message": "No active tasks"}
#
#
# @app.get("/all_tasks")
# def all_tasks():
#     inspector = celery_app.control.inspect()
#     all_tasks = inspector.scheduled()
#     if all_tasks:
#         task_id_list = [task['id'] for task in all_tasks[list(all_tasks.keys())[0]]]
#         return {"all_tasks": task_id_list}
#     else:
#         return {"message": "No tasks"}
#
#
# @app.get("/purge")
# def purge():
#     celery_app.control.purge()
#     return {"message": "All tasks have been purged"}
