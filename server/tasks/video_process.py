from fastapi import FastAPI
from pydantic import BaseModel, Field

from utils import file_operation
from server.config.record_model import BaseRecordModel


class VideoProcess(BaseModel):
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

    def __init__(self):
        super().__init__()

    @staticmethod
    def session_start(event: BaseRecordModel):
        rooms = file_operation.readJson(app.config.TIME_CACHE_PATH)
        rooms[str(event.EventData.RoomId)] = event.EventTimestamp
        file_operation.writeDict(app.config.TIME_CACHE_PATH, rooms)
