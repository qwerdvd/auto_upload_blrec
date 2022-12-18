import asyncio
import threading
from typing import Optional

from pydantic import BaseModel

from .db_config import Field, SQLModel, engine


class CK(BaseModel):
    __table_args__ = {'keep_existing': True}
    UID: int
    CK: str


class RecordTable(SQLModel, table=True):
    __table_args__ = {'keep_existing': True}
    RoomId: int = Field(default=5279, primary_key=True, title='RoomId')
    EventId: str = Field(title='EventId')
    data: str = Field(title='data')
    InRecording: bool = Field(default=False, title='InRecording')
    InStreaming: bool = Field(default=False, title='InStreaming')
    IsPushed: bool = Field(default=True, title='IsPushed')
    IsUpload: bool = Field(default=False, title='IsUpload')


class BiliBiliCookies(SQLModel, table=True):
    __table_args__ = {'keep_existing': True}
    UID: Optional[int] = Field(default='100000000', primary_key=True)
    Cookies: str = Field(title='Cookies')


async def create_all():
    async with engine.begin() as conn:
        await conn.run_sync(SQLModel.metadata.create_all)


threading.Thread(target=lambda: asyncio.run(create_all()), daemon=True).start()
