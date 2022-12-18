from typing import Optional

from sqlalchemy.future import select
from sqlalchemy import update
from sqlalchemy.ext.asyncio import AsyncSession

from .models import CK
from ..database.models import BiliBiliCookies


class CookiesDAL:
    def __init__(self, db_session: AsyncSession):
        self.db_session = db_session

    async def get_user_data(self, uid: int) -> Optional[BiliBiliCookies]:
        sql = select(BiliBiliCookies).where(BiliBiliCookies.UID == uid)
        result = await self.db_session.execute(sql)
        data = result.scalars().all()
        if data:
            return data[0]
        else:
            return None

    async def get_ck(self, uid: int) -> CK | bool:
        """
        :说明:
          获取Cookies
        :参数:
          * uid (int): UID。
        :返回:
          * cookies (str): Cookies。
        """
        data = await self.get_user_data(uid)
        if data:
            return CK(CK=data.Cookies, UID=data.UID)
        else:
            return False

    async def user_exists(self, uid: int) -> bool:
        data = await self.get_user_data(uid)
        if data:
            return True
        else:
            return False

    async def add_cookie_db(self, uid: int, cookies: str) -> bool:
        """
        :说明:
          绑定Cookies
        :参数:
          * uid (int): UID。
          * cookies (str): Cookies。
        :返回:
          * bool (bool): 是否成功。
        """
        if await self.user_exists(uid):
            sql = (
                update(BiliBiliCookies)
                .where(BiliBiliCookies.UID == uid)
                .values(Cookies=cookies, Extra=None)
            )
            await self.db_session.execute(sql)
        else:
            new_data = BiliBiliCookies(
                UID=int(uid),
                Cookies=cookies,
            )
            self.db_session.add(new_data)
        await self.db_session.flush()
        return True
