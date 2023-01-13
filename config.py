from pydantic import BaseSettings
from dotenv import load_dotenv


class Config(BaseSettings):
    WEBHOOK_ADDR: str
    WEBHOOK_PORT: int

    RCLONE_DIR: str
    BLREC_WORK_DIR: str

    USE_PROXY: bool
    PROXY_URL: str

    TG_CHAT_ID: str
    TG_BOT_TOKEN: str

    USE_TG_NOTIFICATION: bool
    UPLOAD_TO_RCLONE: bool
    UPLOAD_TO_BILIBILI: bool

    DELETE_LOCAL: bool

    class Config:
        env_file = '.env'

    _instance = None

    def __new__(cls):
        if not cls._instance:
            load_dotenv('.env')
            cls._instance = super().__new__(cls)
        return cls._instance


settings = Config()
