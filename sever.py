# import json
# from runbash import run_bash as runbash
# from tgnotice import tg_notice as tgnotice
# from http.server import BaseHTTPRequestHandler, HTTPServer
# from urllib.parse import unquote
#
# default_event_type = {'FileClosed', 'StreamStarted', 'SessionStarted', 'StreamEnded'}
#
#
# class RequestHandler(BaseHTTPRequestHandler):
#     def do_POST(self):
#         # 返回状态码
#         self.send_response(200)
#         data = self.rfile.read(int(self.headers['content-length']))
#         data = unquote(str(data, encoding='utf-8'))
#         data = json.loads(data)
#         event_type = data['EventType']
#         print(data)
#         text = f"分区: {data['EventData']['AreaNameParent']} {data['EventData']['AreaNameChild']}\n" \
#                f"标题: [{data['EventData']['Title']}](https://live.bilibili.com/{data['EventData']['RoomId']})"
#         match event_type:
#             case 'FileClosed':
#                 # 上传文件
#                 runbash(data['EventData']['RelativePath'], data['EventData']['RoomId'], data['EventData']['Name'])
#             case 'StreamStarted':
#                 # 开始直播
#                 banner = f"*{data['EventData']['Name']}*的直播开始了，快来看看吧！"
#                 tgnotice(banner, text)
#             case 'SessionStarted':
#                 # 开始录制
#                 banner = f"*{data['EventData']['Name']}*的直播录制开始了，快来看看吧！"
#                 tgnotice(banner, text)
#             case 'StreamEnded':
#                 # 结束直播
#                 banner = f"*{data['EventData']['Name']}*的直播结束了，欢迎下次再观看！"
#                 tgnotice(banner, text)
#             case _:
#                 # 未知事件
#                 pass
