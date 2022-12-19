import os
import config
from biliup.plugins.bili_webup import BiliBili, Data
from dotenv import load_dotenv

load_dotenv(verbose=True)

COVER_PATH = os.getenv('COVER_PATH') if os.getenv('COVER_PATH') else './cover.png'


async def upload_to_bilibili(
        _filepath: str,
        room_id: int,
        title: str,
        time_data: str,
        file_list: list,
) -> None:
    config_data = config.Config().load('config.toml')
    video = Data()
    video.title = config_data['title'].format(title=title, time=time_data)
    video.desc = config_data['description']
    video.cover = config_data['cover_path'] if config_data['cover_path'] else None
    video.copyright = config_data['copyright']
    if video.copyright == 2:
        video.source = f'https://live.bilibili.com/{room_id}'
    else:
        video.source = None
    video.dynamic = config_data['dynamic']

    video.tid = config_data['tid']
    video.set_tag(config_data['tag'])
    with BiliBili(video) as bili:
        bili.login_by_cookies(config_data['user_cookie'])
        for file in file_list:
            video_part = bili.upload_file(file)  # 上传视频
            video.append(video_part)  # 添加视频分P
        video.cover = bili.cover_up('/cover_path').replace('http:', '')  # 上传封面
        bili.submit()  # 提交视频
