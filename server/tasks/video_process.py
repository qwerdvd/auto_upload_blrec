import os

from pydantic import BaseModel, Field

from loggerController import logger
from server.config.config import config, RoomConfig, Config
from server.model.info import LiveInfo
from server.tasks.pushnotify.pushnotify import notify
from utils import file_operation, video_operation

from server.model.brec_model import BaseRecordModel


class BrecVideoProcess(BaseModel):
    """ process brec videos
    Attributes:
        folder: 录播文件所属文件夹
        origins: 原始文件名（不带后缀）
        process_dir: 处理后文件所在文件夹
        processes: 处理文件名（不带后缀）
        extensions: 后缀名
        event: 直播信息
    """
    folder: str = Field(..., description="录播文件所属文件夹")
    origins: list[str] = Field(..., description="原始文件名（不带后缀）")
    process_dir: str = Field(..., description="处理后文件所在文件夹")
    processes: list[str] = Field(..., description="处理文件名（不带后缀）")
    extensions: list[str] = Field(..., description="后缀名")
    event: BaseRecordModel = Field(..., description="直播信息")
    live_info: LiveInfo = Field(..., description="直播信息")
    base_config: Config = Field(..., description="配置文件")
    room_config: RoomConfig = Field(..., description="房间配置文件")

    def __init__(self, event: BaseRecordModel, room_config: RoomConfig):
        super().__init__()
        self.event = event
        self.base_config = config
        self.room_config = room_config
        self.live_info.read_start_time(config.server['time_cache_path'], self.live_info.room_id)

    @staticmethod
    async def session_start(event: BaseRecordModel):
        rooms = file_operation.readJson(str(config.server['time_cache_path']))
        rooms[str(event.EventData.RoomId)] = event.EventTimestamp.timestamp()
        file_operation.writeDict(config.server['time_cache_path'], rooms)
        await notify(event)

    @staticmethod
    async def file_opening(event: BaseRecordModel):
        relative_folder, name = os.path.split(event.EventData.RelativePath)
        folder = os.path.join(config.rec_dir, relative_folder)  # relative -> absolute
        name = os.path.splitext(name)[0]
        extensions = ['.flv', '.xml'] if config.process['danmaku'] else ['.flv']
        for extension in extensions:  # check if file exists
            if not os.path.exists(os.path.join(folder, name + extension)):
                logger.warning(f"EventId: {event.EventId} | EventType: {event.EventType} | "
                               f"File not found: {name + extension} | Should exist in {folder} but not found")

        rooms = file_operation.readJson(config.server['video_cache_path'])
        if str(event.EventData.RoomId) not in rooms:
            rooms[str(event.EventData.RoomId)] = {
                'folder': folder,
                'filenames': [],
                'extensions': extensions
            }
        rooms[str(event.EventData.RoomId)]['filenames'].append(name)
        file_operation.writeDict(config.server['video_cache_path'], rooms)
        await notify(event)

    async def live_end(self):
        rooms = file_operation.readJson(config.server['video_cache_path'])
        if str(self.event.EventData.RoomId) not in rooms:
            logger.error(f"EventId: {self.event.EventId} | EventType: {self.event.EventType} | "
                         f"RoomId: {self.event.EventData.RoomId} | This room is not in video cache")
            # raise UnknownError(f'Room {self.live_info.room_id} not found in video_cache.json')
        room = rooms.pop(str(self.event.EventData.RoomId))
        file_operation.writeDict(config.server['video_cache_path'], rooms)
        self.folder, self.origins, self.extensions = room['folder'], room['filenames'], room['extensions']
        self.generate_process_dir()

    def generate_process_dir(self):
        room_id = self.event.EventData.RoomId
        start_time = self.live_info.start_time
        self.process_dir = os.path.join(config.work_dir, f'{room_id}_{start_time.strftime("%Y%m%d-%H%M%S")}')

    @property
    def need_process(self) -> bool:
        # whether this room is in config
        if self.room_config is None:
            logger.debug('Room not found in config.', extra={'room_id': self.live_info.room_id})
            return False
        # whether videos exist
        if len(self.origins) == 0:
            logger.warning('No video found.', extra={'room_id': self.live_info.room_id})
            return False
        # whether this room is filtered by extra config
        for condition in self.room_config.list_conditions(self.live_info):
            if not condition.process:
                logger.debug('Room filtered by extra conditions, '
                             'details: item -- %s | regexp -- %s',
                             condition.item, condition.regexp, extra={'room_id': self.live_info.room_id})
                return False
        # whether total time is enough
        videos = [os.path.join(self.folder, origin + '.flv') for origin in self.origins]
        total_time = video_operation.getTotalTime(videos)
        if total_time < config.bilibili_upload['min_time']:
            logger.debug('Total time is not enough, details: total time -- %s | min time -- %s',
                         total_time, config.bilibili_upload['min_time'], extra={'room_id': self.live_info.room_id})
            return False
        return True


async def session_end(event: BaseRecordModel):
    await notify(event)


async def file_closed(event: BaseRecordModel):
    await notify(event)


async def stream_started(event: BaseRecordModel):
    await notify(event)


async def stream_ended(event: BaseRecordModel):
    await notify(event)
