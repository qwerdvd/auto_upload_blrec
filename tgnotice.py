import json
import os
from typing import Dict, Literal, Optional, Any
from aiohttp import ClientSession
from dotenv import load_dotenv

load_dotenv(verbose=True)

TG_CHAT_ID = os.getenv('TG_CHAT_ID')
TG_BOT_TOKEN = os.getenv('TG_BOT_TOKEN')
USE_PROXY = os.getenv('USE_PROXY')
PROXY_URL = os.getenv('PROXY_URL')


async def _request(
        url: str,
        method: Literal['GET', 'POST'] = 'POST',
        # header: Dict[str, Any] = _HEADER,
        params: Optional[Dict[str, Any]] = None,
        data: Optional[Dict[str, Any]] = None,
        sess: Optional[ClientSession] = None,
        use_proxy: Optional[bool] = False,
) -> dict:
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
        )
        text_data = await req.text()
        if text_data.startswith('('):
            text_data = json.loads(text_data.replace("(", "").replace(")", ""))
            return text_data
        raw_data = await req.json()
        return raw_data
    except Exception:
        return {'retcode': -1}
    finally:
        if is_temp_sess:
            await sess.close()


async def tg_notice(banner, text):
    url = 'https://api.telegram.org/bot' + TG_BOT_TOKEN + '/sendMessage'
    raw_data = await _request(
        url=url,
        method='POST',
        data={
            'chat_id': TG_CHAT_ID,
            'text': banner + "\n" + text,
            'parse_mode': 'Markdown'
        },
        use_proxy=USE_PROXY,
    )
    if raw_data['ok']:
        print(" Telegram notice 发送成功.")
    elif raw_data['retcode'] == -1:
        print(" Telegram notice 发送失败.")
        print(raw_data)
