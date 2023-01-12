from pydantic import BaseModel, Field


class ConfigModel(BaseModel):
    RCLONE_DIR: str = Field(default=None, description="rclone挂载的目录")
    BLREC_WORK_DIR: str = Field(description="录播姬工作目录")
    TG_CHAT_ID: str = Field(description="Telegram群组ID")
    TG_BOT_TOKEN: str = Field(description="Telegram Bot Token")
