import os
import time

from fastapi import FastAPI, Request
from dotenv import load_dotenv

from utils import file_operation
from .router import router
from .config.config import BaseConfig
from loggerController import logger

load_dotenv()
work_dir = os.getenv("WORK_DIR")


def get_app() -> FastAPI:
    app = FastAPI()

    if work_dir is None:
        logger.error("WORK_DIR not set")
        raise ValueError("WORK_DIR not set")

    config = file_operation.readYml(os.path.join(work_dir, 'config', 'config.yml'))
    base_config = BaseConfig(config)
    print(base_config)

    # 添加中间件计算程序运行时间
    @app.middleware("http")
    async def add_process_time_header(request: Request, call_next):
        start_time = time.time()
        response = await call_next(request)
        process_time = time.time() - start_time
        response.headers["X-Process-Time"] = str(process_time)
        return response

    app.include_router(router, prefix="/api")

    return app
