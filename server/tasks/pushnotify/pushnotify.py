from server.config.config import Config
from server.model.brec_model import BaseRecordModel
from server.tasks.pushnotify.providers.telegram import telegram_notify


async def notify(event: BaseRecordModel):
    await telegram_notify(event)
