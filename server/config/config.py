import functools
import os
import re
from typing import Optional, Any

from pydantic import BaseModel, Field, BaseSettings

from utils import file_operation
from loggerController import logger
from server.model.brec_model import BaseRecordModel
from server.config.utils import _getValue


class TelegramNotify(BaseSettings):
    enable: bool = False
    bot_token: str = ''
    chat_id: str = ''

    @classmethod
    def update(cls, data: dict):
        cls.enable = data['enable']
        cls.bot_token = data['bot-token']


class Proxy(BaseSettings):
    enable: bool = False
    proxy_url: str = ''

    @classmethod
    def update(cls, data: dict):
        cls.enable = data['enable']
        cls.proxy_url = data['proxy-url']


class RcloneUpload(BaseSettings):
    enable: bool = True
    delete_after_upload: bool = True
    remote: str = ''

    @classmethod
    def update(cls, data: dict):
        cls.enable = data['enable']
        cls.delete_after_upload = data['delete-after-upload']
        cls.remote = data['remote']


class BilibiliUpload(BaseSettings):
    enable: bool = False
    multipart: int = 2
    delete_after_upload: bool = True
    auto_upload: bool = True
    min_time: int = 1

    @classmethod
    def update(cls, data: dict):
        cls.enable = data['enable']
        cls.multipart = data['multipart']
        cls.delete_after_upload = data['delete-after-upload']
        cls.auto_upload = data['auto-upload']
        cls.min_time = data['min-time']


class Process(BaseSettings):
    danmaku: bool = False
    video_process_dir: str = ''
    video_process_ext: list = []
    video_process_danmaku: bool = True

    @classmethod
    def update(cls, data: dict):
        cls.danmaku = data['danmaku']
        cls.video_process_dir = data['video-process-dir']
        cls.video_process_ext = data['video-process-ext']
        cls.video_process_danmaku = data['video-process-danmaku']


class Server(BaseSettings):
    port: int = 5000
    webhooks: str = 'webhook'
    time_cache_path: str = 'cache/time.json'
    video_cache_path: str = 'cache/video.json'

    @classmethod
    def update(cls, data: dict):
        cls.port = data['port']
        cls.webhooks = data['webhooks']
        cls.time_cache_path = data['time-cache-path']
        cls.video_cache_path = data['video-cache-path']


class BaseConfig(BaseSettings):
    rec_dir: str = Field(None, description='录播姬工作目录')
    work_dir: str = Field(None, description='录播姬工作目录')
    workers: int = Field(1, description='线程数')
    server: Server = Field(Server(), description='server配置')
    process: Process = Field(Process(), description='process配置')
    bilibili_upload: BilibiliUpload = Field(BilibiliUpload(), description='bilibili_upload配置')
    rclone_upload: RcloneUpload = Field(RcloneUpload(), description='rclone_upload配置')
    proxy: Proxy = Field(Proxy(), description='proxy配置')
    notify: TelegramNotify = Field(TelegramNotify(), description='notify配置')

    config_dir: str = Field(None, description='配置文件目录')

    def __init__(self, config: dict):
        super().__init__()
        self.__dict__.update(config['base'])
        self.server.update(config['base']['server'])
        self.process.update(config['base']['process'])
        self.bilibili_upload.update(config['base']['bilibili-upload'])
        self.rclone_upload.update(config['base']['rclone-upload'])
        self.proxy.update(config['base']['proxy'])
        self.notify.update(config['notify']['telegram'])
        self.config_dir = self._config_dir()

    def _config_dir(self):
        return os.path.join(self.work_dir, 'config')


class Condition(BaseModel):
    item: str = Field(..., description='条件名称')
    regexp: str = Field(..., description='正则表达式')
    tags: list[str] = Field([], description='此条件下的上传标签')
    # channel: property(lambda self: self._channel, _setChannel) = Field(..., description='此条件下的上传频道')
    process: bool = Field(..., description='此条件是否需要处理')

    _channel: (str, str) = None

    def __init__(self, config: dict, **kwargs):
        super().__init__(**kwargs)
        get_value = functools.partial(_getValue, data=config)
        self.item = get_value('item')
        self.regexp = str(get_value('regexp'))
        self.process = get_value('process', True)
        self.tags = get_value('tags', '').split(',')
        self.channel = config.get('channel', '')


class RoomConfig(BaseModel):
    id: int = Field(..., description='房间id')
    title: str = Field(..., description='视频标题(模板字符串)')
    description: str = Field(..., description='视频描述(模板字符串)')
    dynamic: str = Field(..., description='视频动态(模板字符串)')
    # channel: property(lambda self: self._channel, _setChannel) = Field(..., description='上传频道')
    tags: list[str] = Field([], description='上传标签')
    conditions: list[Condition] = Field([], description='房间额外条件')

    _channel: (str, str) = None

    def __init__(self, config: dict, **data: Any):
        super().__init__(**data)
        get_value = functools.partial(_getValue, data=config)

        self.id = get_value('id')
        self.title = get_value('title', '{title}')
        self.description = get_value('description', '')
        self.dynamic = get_value('dynamic', '')
        self.tags = get_value('tags', '').split(',')
        self.conditions = [Condition(c) for c in get_value('conditions', [])]
        self.channel = get_value('channel', '')

    @classmethod
    def init(cls, work_dir: str, room_id: int, short_id: int = 0) -> Optional['RoomConfig']:
        path = os.path.join(work_dir, 'config', 'room-config.yml')
        configs = file_operation.readYml(path)
        for room in configs['rooms']:
            if int(room['id']) in (room_id, short_id):
                return cls(room)
        logger.warning('Unknown room: [id: %d] [short id: %d]', room_id, short_id)

    def list_conditions(self, event: BaseRecordModel) -> list[Condition]:
        """ list proper conditions
        :param event
        :return:
        """
        result = []
        for condition in self.conditions:
            try:
                if re.search(pattern=condition.regexp, string=getattr(event, condition.item)):
                    result.append(condition)
            except AttributeError as _:
                logger.warning('Invalid condition: %s', condition.item)
        return result
