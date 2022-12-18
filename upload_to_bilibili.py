import os
import stream_gears
from dotenv import load_dotenv

load_dotenv(verbose=True)

COVER_PATH = os.getenv('COVER_PATH') if os.getenv('COVER_PATH') else './cover.png'


async def upload_to_bilibili(
        _filepath: str, room_id: int, title: str, time_data: str
) -> None:
    _title = f'【狼宝滴录播】 {time_data} {title}'
    await stream_gears.upload(
        _filepath,
        "./cookies.json",  # cookies
        _title,  # title
        27,  # 投稿分区
        "直播回放,血狼破军",  # tags，写在一个引号内，逗号分隔
        2,  # 1：原创；2：转载
        f"https://live.bilibili.com/{room_id}",  # 转载来源
        f"XXXX直播间：https://live.bilibili.com/XXXX",  # introduction
        "",  # dynamic
        COVER_PATH,  # cover
        None,  # 延迟发布
        None,  # 自动选择上传线路
        3,
    )
