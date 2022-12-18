from .database.CookiesDAL import CookiesDAL
from .database.RecordDAL import RecordDAL
from .database.db_config import async_session


async def add_record_room(room_id: int) -> bool:
    async with async_session() as session:
        async with session.begin():
            RecordData = RecordDAL(session)
            if await RecordData.add_record_room(room_id):
                return True
            else:
                return False


async def update_record_status(
        room_id: int,
        in_recording: bool,
        in_streaming: bool,
        is_pushed: bool,
        is_upload: bool
) -> bool:
    async with async_session() as session:
        async with session.begin():
            RecordStatus = RecordDAL(session)
            return await RecordStatus.update_record_status(
                room_id,
                {'InRecording': in_recording, 'InStreaming': in_streaming, 'IsPushed': is_pushed, 'IsUpload': is_upload}
            )


async def add_cookie(uid: int, cookies: str) -> bool:
    async with async_session() as session:
        async with session.begin():
            CookieData = CookiesDAL(session)
            return await CookieData.add_cookie_db(uid, cookies)


async def get_ck(room_id: int) -> str:
    async with async_session() as session:
        async with session.begin():
            CookieData = CookiesDAL(session)
            cookie = await CookieData.get_ck(room_id)
            if cookie:
                return cookie.CK
            else:
                return ''
