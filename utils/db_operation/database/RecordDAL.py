from typing import List, Optional, Callable

from sqlalchemy import update
from sqlalchemy.orm import Session
from sqlalchemy.future import select

from .models import RecordTable


class RecordDAL:
    def __init__(self, db_session: Session):
        self.db_session = db_session

    async def get_record_data(self, room_id: int) -> Optional[RecordTable]:
        sql = select(RecordTable).where(RecordTable.RoomId == room_id)
        result = await self.db_session.execute(sql)
        data = result.scalars().all()
        if data:
            return data[0]
        else:
            return None

    async def record_room_exists(self, room_id: int) -> bool:
        data = await self.get_record_data(room_id)
        if data:
            return True
        else:
            return False

    async def add_record_room(self, room_id: int) -> bool:
        """
        :说明:
          添加直播间
        :参数:
          * room_id (int): 直播间号。
        :返回:
          * bool (bool): 是否成功。
        """
        if await self.record_room_exists(room_id):
            return True
        else:
            new_data = RecordTable(RoomId=room_id)
            self.db_session.add(new_data)
        await self.db_session.flush()  # type: ignore
        return True

    async def update_record_status(
        self,
        room_id: int,
        data: Optional[dict],
    ) -> bool:
        """
        :说明:
          更新数据库中的直播状态数据。
        :参数:
          * room_id (int): 直播间号。
          * data (dict): InRecording,InStreaming,IsPushed,IsUpload 至少填写一项。
            data = {'InRecording': False, 'InStreaming': False, 'IsPushed': True, 'IsUpload': False}
        :返回:
          * bool (bool): 是否成功。
        """
        if not await self.record_room_exists(room_id):
            await self.add_record_room(room_id)
        sql = (
            update(RecordTable)
            .where(RecordTable.RoomId == room_id)
            .values(**data)
        )
        await self.db_session.execute(sql)
        await self.db_session.flush()
        return True
