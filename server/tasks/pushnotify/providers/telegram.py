# from ._requests import _request
#
# from config.Setting import settings
# from utils.config_model.record_model import BaseRecordModel
# from loggerController import logger
#
#
# async def telegram_notify(event: BaseRecordModel):
#     event_type = event.EventType
#     body = f"分区: {event.EventData.AreaNameParent} {event.EventData.AreaNameChild}\n" \
#            f"标题: [{event.EventData.Title}](https://live.bilibili.com/{event.EventData.RoomId})"
#     match event_type:
#         case "SessionStarted":
#             banner = f"*{event.EventData.Name}*的直播录制开始了，快来看看吧！"
#             await tg_notice(event, banner, body)
#         case "SessionEnded":
#             banner = f"*{event.EventData.Name}*的直播录制结束了，欢迎下次再观看！"
#             await tg_notice(event, banner, body)
#         case "StreamStarted":
#             banner = f"*{event.EventData.Name}*的直播开始了，快来看看吧！"
#             await tg_notice(event, banner, body)
#         case "StreamEnded":
#             banner = f"*{event.EventData.Name}*的直播结束了，欢迎下次再观看！"
#             await tg_notice(event, banner, body)
#         case "FileOpening":
#             logger.info(f"EventId: {event.EventId} | EventType: {event_type} | Do nothing.")
#             pass
#         case "FileClosed":
#             logger.info(f"EventId: {event.EventId} | EventType: {event_type} | Do nothing.")
#             pass
#         case _:
#             logger.error(f"EventId: {event.EventId} | EventType: {event_type} | Unknown event type.")
#             pass
#
#
# async def tg_notice(event: BaseRecordModel, banner: str, text: str) -> None:
#     url = "https://api.telegram.org/bot" + settings.TG_BOT_TOKEN + "/sendMessage"
#     callback = await _request(
#         url=url,
#         method="POST",
#         data={
#             "chat_id": settings.TG_CHAT_ID,
#             "text": banner + "\n" + text,
#             "parse_mode": "Markdown"
#         },
#         use_proxy=settings.USE_PROXY,
#     )
#     if callback == 200:
#         logger.info(f"EventId: {event.EventId} | EventType: {event.EventType} | Telegram Notice Pushed successfully.")
#     else:
#         logger.error(
#             f"EventId: {event.EventId} | EventType: {event.EventType} | Telegram Notice Pushed failed. | {callback}")
