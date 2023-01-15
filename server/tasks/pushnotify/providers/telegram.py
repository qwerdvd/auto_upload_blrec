from server.config.config import config
from ._requests import _request

from server.model.brec_model import BaseRecordModel
from loggerController import logger


async def telegram_notify(event: BaseRecordModel) -> None:
    event_type = event.EventType
    body = f"分区: {event.EventData.AreaNameParent} {event.EventData.AreaNameChild}\n" \
           f"标题: [{event.EventData.Title}](https://live.bilibili.com/{event.EventData.RoomId})"
    match event_type:
        case "SessionStarted":
            banner = f"*{event.EventData.Name}*的直播录制开始了，快来看看吧！"
            await tg_notice(event, banner, body)
        case "SessionEnded":
            banner = f"*{event.EventData.Name}*的直播录制结束了，欢迎下次再观看！"
            await tg_notice(event, banner, body)
        case "StreamStarted":
            banner = f"*{event.EventData.Name}*的直播开始了，快来看看吧！"
            await tg_notice(event, banner, body)
        case "StreamEnded":
            banner = f"*{event.EventData.Name}*的直播结束了，欢迎下次再观看！"
            await tg_notice(event, banner, body)
        case "FileOpening":
            logger.info(f"EventId: {event.EventId} | EventType: {event_type} | Do nothing.")
            pass
        case "FileClosed":
            logger.info(f"EventId: {event.EventId} | EventType: {event_type} | Do nothing.")
            pass
        case _:
            logger.error(f"EventId: {event.EventId} | EventType: {event_type} | Unknown event type.")
            pass


async def tg_notice(event: BaseRecordModel, banner: str, text: str) -> None:
    bot_token = config.notify.bot_token
    url = "https://api.telegram.org/bot" + bot_token + "/sendMessage"
    callback = await _request(
        url=url,
        method="POST",
        data={
            "chat_id": config.notify.chat_id,
            "text": banner + "\n" + text,
            "parse_mode": "Markdown"
        },
        use_proxy=config.proxy["enable"],
    )
    if callback == 200:
        logger.info(f"EventId: {event.EventId} | EventType: {event.EventType} | Telegram Notice Pushed successfully.")
    else:
        logger.error(
            f"EventId: {event.EventId} | EventType: {event.EventType} | Telegram Notice Pushed failed. | {callback}")
