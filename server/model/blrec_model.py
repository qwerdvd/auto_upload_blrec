from typing import Union

from pydantic import BaseModel, Field


class UserInfo(BaseModel):
    name: str = Field(description="用户名")
    gender: str = Field(description="性别")
    face: str = Field(description="头像url")
    uid: int = Field(description="用户uid")
    level: int = Field(description="用户等级")
    sign: str = Field(description="个性签名")


class RoomInfo(BaseModel):
    uid: int = Field(description="用户uid")
    room_id: int = Field(description="房间号")
    short_room_id: int = Field(description="短房间号")
    area_id: int = Field(description="分区id")
    area_name: str = Field(description="分区名称")
    parent_area_id: int = Field(description="父分区id")
    parent_area_name: str = Field(description="父分区名称")
    live_status: int = Field(description="直播状态")
    live_start_time: int = Field(description="直播开始时间")
    online: int = Field(description="在线人数")
    title: str = Field(description="直播标题")
    cover: str = Field(description="直播封面url")
    tags: str = Field(description="直播标签")
    description: str = Field(description="直播简介")


class FileData(BaseModel):
    room_id: int = Field(description="房间号")
    path: str = Field(description="文件路径")


class Usage(BaseModel):
    total: int = Field(description="总容量")
    used: int = Field(description="已用容量")
    free: int = Field(description="剩余容量")


class SpaceNoEnoughData(BaseModel):
    path: str = Field(description="文件路径")
    threshold: int = Field(description="阈值")
    usage: Usage = Field(description="磁盘使用情况")


class ErrorData(BaseModel):
    name: str = Field(description="错误名称")
    detail: str = Field(description="错误详情")


class BaseBlrecWebhookEvent(BaseModel):
    id: str = Field(description="事件id")
    date: str = Field(description="事件发生时间")
    type: str = Field(description="事件类型")
    data: dict = Field(description="事件数据")

    @staticmethod
    def create_event(data: dict):
        event_type = data.get('type')
        event_class = globals().get(event_type)
        if not event_class or not issubclass(event_class, BaseBlrecWebhookEvent):
            raise ValueError(f'Invalid event type: {event_type}')
        return event_class(**data)


class LiveBeganEvent(BaseBlrecWebhookEvent):
    data: dict[str, Union[UserInfo, RoomInfo]] = Field(description="事件数据")


class LiveEndedEvent(BaseBlrecWebhookEvent):
    data: dict[str, Union[UserInfo, RoomInfo]] = Field(description="事件数据")


class RoomChangeEvent(BaseBlrecWebhookEvent):
    data: dict[str, RoomInfo] = Field(description="事件数据")


class RecordingStartedEvent(BaseBlrecWebhookEvent):
    data: dict[str, RoomInfo] = Field(description="事件数据")


class RecordingFinishedEvent(BaseBlrecWebhookEvent):
    data: dict[str, RoomInfo] = Field(description="事件数据")


class RecordingCancelledEvent(BaseBlrecWebhookEvent):
    data: dict[str, RoomInfo] = Field(description="事件数据")


class VideoFileCreatedEvent(BaseBlrecWebhookEvent):
    data: dict[str, FileData] = Field(description="事件数据")


class VideoFileCompletedEvent(BaseBlrecWebhookEvent):
    data: dict[str, FileData] = Field(description="事件数据")


class RawDanmakuFileCreatedEvent(BaseBlrecWebhookEvent):
    data: dict[str, FileData] = Field(description="事件数据")


class RawDanmakuFileCompletedEvent(BaseBlrecWebhookEvent):
    data: dict[str, FileData] = Field(description="事件数据")


class VideoPostprocessingCompletedEvent(BaseBlrecWebhookEvent):
    data: dict[str, FileData] = Field(description="事件数据")


class SpaceNoEnoughEvent(BaseBlrecWebhookEvent):
    data: SpaceNoEnoughData = Field(description="事件数据")


class ErrorEvent(BaseBlrecWebhookEvent):
    data: ErrorData = Field(description="事件数据")
