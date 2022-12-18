# # from flask import request
# # from tgnotice import tg_notice as tgnotice
# # from runbash import run_bash as runbash
# # from main import app
# # import json
# #
# #
# # @app.route("/webhook", methods=['POST'])
# # async def handle_post_request():
# #     # 获取event事件
# #     event = json.loads(request.get_data().decode("utf-8"))
# #     app.logger.info("event:"+event["EventType"])
# #     app.logger.info(event)
# #
# #     # 处理 JSON 数据
# #     event_type = event['EventType']
# #     room_id = event['EventData']['RoomId'] if 'EventData' in event else 0
# #     text = f"分区: {event['EventData']['AreaNameParent']} {event['EventData']['AreaNameChild']}\n" \
# #            f"标题: [{event['EventData']['Title']}](https://live.bilibili.com/{event['EventData']['RoomId']})"
# #     match event_type:
# #         case 'FileClosed':
# #             # 上传文件
# #             runbash(event['EventData']['RelativePath'], event['EventData']['RoomId'], event['EventData']['Name'])
# #         case 'StreamStarted':
# #             # 开始直播
# #             banner = f"*{event['EventData']['Name']}*的直播开始了，快来看看吧！"
# #             tgnotice(banner, text)
# #         case 'SessionStarted':
# #             # 开始录制
# #             banner = f"*{event['EventData']['Name']}*的直播录制开始了，快来看看吧！"
# #             tgnotice(banner, text)
# #         case 'StreamEnded':
# #             # 结束直播
# #             banner = f"*{event['EventData']['Name']}*的直播结束了，欢迎下次再观看！"
# #             tgnotice(banner, text)
# #         case _:
# #             # 未知事件
# #             pass
# #
# #     # 返回状态码 200
# #     return 200
#
# from flask import Flask, request
#
# app = Flask(__name__)
#
#
# @app.route('/', methods=['POST'])
# def register():
#     print(request.headers)
#     print(request.stream.read())
#     return 200
#
#
# if __name__ == '__main__':
#     app.run(port=5000, debug=True)
