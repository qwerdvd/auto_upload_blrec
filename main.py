# import os
# from http.server import HTTPServer
# from dotenv import load_dotenv
# from sever import RequestHandler
#
# load_dotenv(verbose=True)
#
# webhook_addr = os.getenv('WEBHOOK_ADDR')
# webhook_port = int(os.getenv('WEBHOOK_PORT'))
#
# addr = (webhook_addr, webhook_port)
# server = HTTPServer(addr, RequestHandler)
# server.serve_forever()
import json
import os
from time import sleep

from aioflask import Flask, request
from dotenv import load_dotenv
from tgnotice import tg_notice as tgnotice
from runbash import run_bash as runbash

app = Flask(__name__)
load_dotenv(verbose=True)

webhook_addr = os.getenv('WEBHOOK_ADDR')
webhook_port = int(os.getenv('WEBHOOK_PORT'))
UPLOAD_TO_BILI_ROOM_ID = os.getenv('UPLOAD_TO_BILI_ROOM_ID')
delay = int(os.getenv('DELAY'))


@app.route("/", methods=['POST'])
async def handle_post_request():
    # 获取event事件
    event = json.loads(request.get_data().decode("utf-8"))
    app.logger.info("event:"+event["EventType"])
    app.logger.info(event)

    # 处理 JSON 数据
    event_type = event['EventType']
    room_id = event['EventData']['RoomId'] if 'EventData' in event else 0
    text = f"分区: {event['EventData']['AreaNameParent']} {event['EventData']['AreaNameChild']}\n" \
           f"标题: [{event['EventData']['Title']}](https://live.bilibili.com/{event['EventData']['RoomId']})"
    match event_type:
        case 'FileClosed':
            # 进行延迟处理
            if room_id in UPLOAD_TO_BILI_ROOM_ID:
                pass
            else:
                # 上传文件
                await runbash(
                    event['EventData']['RelativePath'], event['EventData']['RoomId'],
                    event['EventData']['Name'], event['EventData']['Title']
                )
        case 'StreamStarted':
            # 开始直播
            banner = f"*{event['EventData']['Name']}*的直播开始了，快来看看吧！"
            await tgnotice(banner, text)
        case 'SessionStarted':
            # 开始录制
            banner = f"*{event['EventData']['Name']}*的直播录制开始了，快来看看吧！"
            await tgnotice(banner, text)
        case 'StreamEnded':
            # 结束直播
            banner = f"*{event['EventData']['Name']}*的直播结束了，欢迎下次再观看！"
            await tgnotice(banner, text)
        case _:
            # 未知事件
            pass

    # 返回状态码 200
    return 'OK', 200

if __name__ == '__main__':
    app.run(host=webhook_addr, port=webhook_port)
