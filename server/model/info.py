from datetime import datetime

from pydantic import BaseModel, Field

from server.model.brec_model import BaseRecordModel
from utils import file_operation


class LiveInfo(BaseModel):
    room_id: int = Field(description="直播间长号")
    short_id: int = Field(description="直播间短号")
    anchor: str = Field(description="主播")
    title: str = Field(description="直播间标题")
    start_time: datetime = Field(description="开始时间")
    parent_area: str = Field(description="父区域")
    child_area: str = Field(description="子区域")
    session_id: str = Field(description="会话id")

    def __init__(self, event: BaseRecordModel):
        super().__init__()
        self.room_id = event.EventData.RoomId
        self.short_id = event.EventData.ShortId
        self.title = event.EventData.Title
        self.session_id = event.EventData.SessionId
        self.parent_area = event.EventData.AreaNameParent
        self.child_area = event.EventData.AreaNameChild
        self.anchor = event.EventData.Name

    def read_start_time(self, json_file: str, room_id: int):
        """ read session start time from json file(time cache) """
        data = file_operation.readJson(json_file)
        self.start_time = datetime.fromisoformat(data[str(room_id)])

    def fill_module_string(self, module_string: str) -> str:
        """ set template string """

        return module_string \
            .replace('${anchor}', self.anchor) \
            .replace('${title}', self.title) \
            .replace('${date}', self.start_time.strftime('%Y-%m-%d')) \
            .replace('${time}', self.start_time.strftime('%H:%M:%S')) \
            .replace('${parent_area}', self.parent_area) \
            .replace('${child_area}', self.child_area)
