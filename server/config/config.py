import functools
import os
import re
from typing import Optional, Any, Tuple, Union

from dotenv import load_dotenv
from pydantic import BaseModel, Field, BaseSettings

from server.model.info import LiveInfo
from utils import file_operation
from loggerController import logger
from server.model.brec_model import BaseRecordModel
from server.config.utils import _getValue, _setChannel

load_dotenv()
work_dir = os.getenv("WORK_DIR")


class TelegramNotify(BaseSettings):
    enable: bool = True
    bot_token: str = ''
    chat_id: int = None

    def update(self, data: dict):
        self.enable = data['enable']
        self.bot_token = data['bot-token']
        self.chat_id = data['chat-id']


class Proxy(BaseSettings):
    enable: bool = False
    proxy_url: str = ''

    def update(self, data: dict):
        self.enable = data['enable']
        self.proxy_url = data['proxy-url']


class RcloneUpload(BaseSettings):
    enable: bool = True
    delete_after_upload: bool = True
    remote: str = ''

    def update(self, data: dict):
        self.enable = data['enable']
        self.delete_after_upload = data['delete-after-upload']
        self.remote = data['remote']


class BilibiliUpload(BaseSettings):
    enable: bool = False
    multipart: int = 2
    delete_after_upload: bool = True
    auto_upload: bool = True
    min_time: int = 1

    def update(self, data: dict):
        self.enable = data['enable']
        self.multipart = data['multipart']
        self.delete_after_upload = data['delete-after-upload']
        self.auto_upload = data['auto-upload']
        self.min_time = data['min-time']


class Process(BaseSettings):
    danmaku: bool = False
    video_process_dir: str = ''
    video_process_ext: list = []
    video_process_danmaku: bool = True

    def update(self, data: dict):
        self.danmaku = data['danmaku']
        self.video_process_dir = data['video-process-dir']
        self.video_process_ext = data['video-process-ext']
        self.video_process_danmaku = data['video-process-danmaku']


class Server(BaseSettings):
    port: int = 5000
    webhooks: str = 'webhook'
    time_cache_path: str = 'cache/time.json'
    video_cache_path: str = 'cache/video.json'

    def update(self, data: dict):
        self.port = data['port']
        self.webhooks = data['webhooks']
        self.time_cache_path = data['time-cache-path']
        self.video_cache_path = data['video-cache-path']


class Config(BaseModel):
    rec_dir: str = Field(None, description='?????????????????????')
    work_dir: str = Field(None, description='?????????????????????')
    workers: int = Field(1, description='?????????')
    server: Server = Field(Server(), description='server??????')
    process: Process = Field(Process(), description='process??????')
    bilibili_upload: BilibiliUpload = Field(BilibiliUpload(), description='bilibili_upload??????')
    rclone_upload: RcloneUpload = Field(RcloneUpload(), description='rclone_upload??????')
    proxy: Proxy = Field(Proxy(), description='proxy??????')
    notify: TelegramNotify = Field(TelegramNotify(), description='telegram_notify??????')

    config_dir: str = Field(None, description='??????????????????')

    def __init__(self):
        super().__init__()

        load_config = file_operation.readYml(os.path.join(work_dir, 'config', 'config.yml'))
        print(work_dir)
        self.rec_dir = load_config['base']['rec-dir']
        self.__dict__.update(load_config['base'])
        self.work_dir = work_dir
        self.server.update(load_config['base']['server'])
        self.process.update(load_config['base']['process'])
        self.bilibili_upload.update(load_config['base']['bilibili-upload'])
        self.rclone_upload.update(load_config['base']['rclone-upload'])
        self.proxy.update(load_config['base']['proxy'])
        self.notify.update(load_config['notify']['telegram'])
        self.config_dir = self._config_dir()

    def _config_dir(self):
        return os.path.join(self.work_dir, 'config')


class Condition(BaseModel):
    item: str = Field(..., description='????????????')
    regexp: str = Field(..., description='???????????????')
    tags: list[str] = Field([], description='???????????????????????????')
    # channel: property(lambda self: self._channel, _setChannel) = Field(..., description='???????????????????????????')
    process: bool = Field(..., description='???????????????????????????')

    _channel: (str, str) = None

    def __init__(self, room_config: dict, **kwargs):
        super().__init__(**kwargs)
        get_value = functools.partial(_getValue, data=room_config)
        self.item = get_value('item')
        self.regexp = str(get_value('regexp'))
        self.process = get_value('process', True)
        self.tags = get_value('tags', '').split(',')
        self.channel = room_config.get('channel', '')


class RoomConfig(BaseModel):
    id: int = Field(..., description='??????id')
    title: str = Field(..., description='????????????(???????????????)')
    description: str = Field(..., description='????????????(???????????????)')
    dynamic: str = Field(..., description='????????????(???????????????)')
    channel: Union[Tuple[str], str, list[str]] = Field(..., description='????????????')
    tags: list[str] = Field([], description='????????????')
    conditions: list[Condition] = Field([], description='??????????????????')

    _channel: Union[Tuple[str], str, list[str]] = None

    def __init__(self, room_config: dict):
        super().__init__()
        get_value = functools.partial(_getValue, data=room_config)

        self.id = get_value('id')
        self.title = get_value('title', '{title}')
        self.description = get_value('description', '')
        self.dynamic = get_value('dynamic', '')
        self.tags = get_value('tags', '').split(',')
        self.conditions = [Condition(c) for c in get_value('conditions', [])]
        self.channel = get_value('channel', '')
        _setChannel(self, self.channel)

    def __post_init__(self):
        if not self.description:
            self.description = '????????????@qwerdvd???????????????????????????'

    @classmethod
    def init(cls, event: BaseRecordModel) -> Optional['RoomConfig']:
        path = os.path.join(work_dir, 'config', 'room-config.yml')
        configs = file_operation.readYml(path)
        for room in configs['rooms']:
            if int(room['id']) in (event.EventData.RoomId, event.EventData.ShortId):
                return cls(room)
        logger.warning(f"EventId: {event.EventId} | EventType: {event.EventType} | "
                       f"Unknown room: [Room_id: {event.EventData.RoomId}] [Short_id: {event.EventData.ShortId}]")

    def list_conditions(self, live_info: LiveInfo) -> list[Condition]:
        """ list proper conditions
        :param live_info
        :return:
        """
        result = []
        for condition in self.conditions:
            try:
                if re.search(pattern=condition.regexp, string=getattr(live_info, condition.item)):
                    result.append(condition)
            except AttributeError as _:
                logger.warning('Invalid condition: %s', condition.item)
        return result


config = Config()
