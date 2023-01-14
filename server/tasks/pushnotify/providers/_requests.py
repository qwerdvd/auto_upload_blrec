# import json
# from typing import Literal, Optional, Dict, Any
#
# from aiohttp import ClientSession
#
# # from config.Setting import settings
#
#
# async def _request(
#         url: str,
#         method: Literal['GET', 'POST'] = 'POST',
#         # header: Dict[str, Any] = _HEADER,
#         params: Optional[Dict[str, Any]] = None,
#         data: Optional[Dict[str, Any]] = None,
#         sess: Optional[ClientSession] = None,
#         use_proxy: Optional[bool] = False,
# ) -> int | dict:
#     is_temp_sess = False
#     if sess is None:
#         sess = ClientSession()
#         is_temp_sess = True
#     try:
#         req = await sess.request(
#             method,
#             url=url,
#             # headers=header,
#             params=params,
#             json=data,
#             proxy=settings.PROXY_URL if use_proxy else None,
#             timeout=300,
#         )
#         status_code = req.status
#         if status_code != 200:
#             text_data = await req.text()
#             if text_data.startswith('('):
#                 text_data = json.loads(text_data.replace("(", "").replace(")", ""))
#                 return text_data
#             raw_data = await req.json()
#             return raw_data
#         return status_code
#     except Exception as e:
#         return {'error': str(e)}
#     finally:
#         if is_temp_sess:
#             await sess.close()
