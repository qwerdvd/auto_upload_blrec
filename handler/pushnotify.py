from typing import Literal, Optional, Dict, Any

import os
import json
from aiohttp import ClientSession
from dotenv import load_dotenv

from model import BaseRecordModel
from loggerController import logger

load_dotenv(verbose=True)

TG_BOT_TOKEN = os.getenv("TG_BOT_TOKEN")
TG_CHAT_ID = os.getenv("TG_CHAT_ID")
USE_PROXY = os.getenv("USE_PROXY")
PROXY_URL = os.getenv("PROXY_URL")


async def notify(event: BaseRecordModel):
    await telegram_notify(event)


async def telegram_notify(event: BaseRecordModel):
    event_type = event.EventType
    body = f"分区: {event.EventData.AreaNameParent} {event.EventData.AreaNameChild}\n" \
           f"标题: [{event.EventData.Title}](https://live.bilibili.com/{event.EventData.RoomId})"
    match event_type:
        case "SessionStarted":
            banner = f"*{event.EventData.Name}*的直播录制开始了，快来看看吧！"
            await tg_notice(banner, body)
        case "SessionEnded":
            banner = f"*{event.EventData.Name}*的直播录制结束了，欢迎下次再观看！"
            await tg_notice(banner, body)
        case "StreamStarted":
            banner = f"*{event.EventData.Name}*的直播开始了，快来看看吧！"
            await tg_notice(banner, body)
        case "StreamEnded":
            banner = f"*{event.EventData.Name}*的直播结束了，欢迎下次再观看！"
            await tg_notice(banner, body)
        case "FileOpening":
            logger.info(f"EventType: {event_type} Do nothing.")
            pass
        case "FileClosed":
            logger.info(f"EventType: {event_type} Do nothing.")
            pass
        case _:
            logger.error(f"Unsupported EventType: {event_type}")
            pass


async def tg_notice(banner: str, text: str) -> None:
    url = 'https://api.telegram.org/bot' + TG_BOT_TOKEN + '/sendMessage'
    callback = await _request(
        url=url,
        method='POST',
        data={
            'chat_id': TG_CHAT_ID,
            'text': banner + "\n" + text,
            'parse_mode': 'Markdown'
        },
        use_proxy=USE_PROXY,
    )
    if callback == 200:
        logger.info("Telegram notice 发送成功.")
    else:
        logger.error("Telegram notice 发送失败. {}".format(callback))


async def _request(
        url: str,
        method: Literal['GET', 'POST'] = 'POST',
        # header: Dict[str, Any] = _HEADER,
        params: Optional[Dict[str, Any]] = None,
        data: Optional[Dict[str, Any]] = None,
        sess: Optional[ClientSession] = None,
        use_proxy: Optional[bool] = False,
) -> int | dict:
    is_temp_sess = False
    if sess is None:
        sess = ClientSession()
        is_temp_sess = True
    try:
        req = await sess.request(
            method,
            url=url,
            # headers=header,
            params=params,
            json=data,
            proxy=PROXY_URL if use_proxy else None,
            timeout=300,
            ssl = False
        )
        status_code = req.status
        if status_code != 200:
            text_data = await req.text()
            if text_data.startswith('('):
                text_data = json.loads(text_data.replace("(", "").replace(")", ""))
                return text_data
            raw_data = await req.json()
            return raw_data
        return status_code
    except Exception as e:
        return {'error': str(e)}
    finally:
        if is_temp_sess:
            await sess.close()
