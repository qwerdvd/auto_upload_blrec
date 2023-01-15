from pydantic import BaseModel, Field

from server.config.config import config, RoomConfig, Config
from server.tasks.pushnotify.pushnotify import notify
from utils import file_operation

from server.model.brec_model import BaseRecordModel


class BrecVideoProcess(BaseModel):
    """ process videos
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
    base_config: Config = Field(..., description="配置文件")
    room_config: RoomConfig = Field(..., description="房间配置文件")

    def __init__(self, event: BaseRecordModel, room_config: RoomConfig):
        super().__init__()
        self.event = event
        self.base_config = config
        self.room_config = room_config

    @staticmethod
    async def session_start(event: BaseRecordModel):
        print(config)
        rooms = file_operation.readJson(str(config.server['time_cache_path']))
        rooms[str(event.EventData.RoomId)] = event.EventTimestamp.timestamp()
        file_operation.writeDict(config.server['time_cache_path'], rooms)
        await notify(event)
