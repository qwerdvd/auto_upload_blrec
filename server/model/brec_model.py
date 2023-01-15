from typing import Literal
from datetime import datetime

from pydantic import BaseModel, Field
from utils.time_operation import fromIso


class BaseEventData(BaseModel):
    RoomId: int = Field(description="房间号")
    ShortId: int = Field(description="短号，如果没有则为0")
    Name: str = Field(description="主播名字")
    Title: str = Field(description="直播间标题")
    AreaNameParent: str = Field(description="直播间父分区")
    AreaNameChild: str = Field(description="直播间子分区")
    Recording: bool = Field(description="当前是否正在录制")
    Streaming: bool = Field(description="当前直播间状态是否为直播中")
    DanmakuConnected: bool = Field(description="当前是否连接了弹幕服务器")


class SessionStartedEventData(BaseEventData):
    SessionId: str = Field(description="录制会话ID")


class FileOpeningEventData(BaseEventData):
    RelativePath: str = Field(description="文件相对路径")
    FileOpenTime: str = Field(description="文件打开时间")
    SessionId: str = Field(description="录制会话ID")


class FileClosedEventData(BaseEventData):
    RelativePath: str = Field(description="文件相对路径")
    FileSize: int = Field(description="文件大小")
    Duration: int = Field(description="录制时长")
    FileOpenTime: str = Field(description="文件打开时间")
    FileCloseTime: str = Field(description="文件关闭时间")
    SessionId: str = Field(description="录制会话ID")


class SessionEndedEventData(BaseEventData):
    SessionId: str = Field(description="录制会话ID")


class StreamStartedEventData(BaseEventData):
    ...


class StreamEndedEventData(BaseEventData):
    ...


class BaseRecordModel(BaseModel):
    EventType: Literal[
        "SessionStarted", "SessionEnded", "StreamStarted", "StreamEnded", "FileOpening", "FileClosed"] = Field(
        description="事件类型")
    EventTimestamp: datetime = Field(description="事件发生时间", convert_loader=lambda value: fromIso(value))
    EventId: str = Field(description="事件ID")
    EventData: BaseEventData = Field(description="事件数据")
    _subclasses = {}

    @classmethod
    def register_subclass(cls, event_type):
        def decorator(subclass):
            cls._subclasses[event_type] = subclass
            return subclass
        return decorator

    @classmethod
    def create_event(cls, **kwargs):
        event_type = kwargs["EventType"]
        if event_type in cls._subclasses:
            return cls._subclasses[event_type](**kwargs)
        else:
            raise ValueError(f"Invalid EventType: {event_type}")


@BaseRecordModel.register_subclass("SessionStarted")
class SessionStarted(BaseRecordModel):
    EventData: SessionStartedEventData = Field(description="事件数据")


@BaseRecordModel.register_subclass("SessionEnded")
class SessionEnded(BaseRecordModel):
    EventData: SessionEndedEventData = Field(description="事件数据")


@BaseRecordModel.register_subclass("StreamStarted")
class StreamStarted(BaseRecordModel):
    EventData: StreamStartedEventData = Field(description="事件数据")


@BaseRecordModel.register_subclass("StreamEnded")
class StreamEnded(BaseRecordModel):
    EventData: StreamEndedEventData = Field(description="事件数据")


@BaseRecordModel.register_subclass("FileOpening")
class FileOpening(BaseRecordModel):
    EventData: FileOpeningEventData = Field(description="事件数据")


@BaseRecordModel.register_subclass("FileClosed")
class FileClosed(BaseRecordModel):
    EventData: FileClosedEventData = Field(description="事件数据")
