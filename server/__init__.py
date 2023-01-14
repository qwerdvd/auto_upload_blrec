import time

from fastapi import FastAPI, Request

from .router import router


def get_app() -> FastAPI:
    app = FastAPI()

    # 添加中间件计算程序运行时间
    @app.middleware("http")
    async def add_process_time_header(request: Request, call_next):
        start_time = time.time()
        response = await call_next(request)
        process_time = time.time() - start_time
        response.headers["X-Process-Time"] = str(process_time)
        return response

    app.include_router(router, prefix="/api")

    @app.on_event("startup")
    async def startup():
        app.config = {
            "TIME_CACHE_PATH": "cache/time.json",
            "VIDEO_CACHE_PATH": "cache/video.json",
            "VIDEO_PROCESS_DIR": "video",
            "VIDEO_PROCESS_EXT": ["mp4", "flv", "mkv"],
            "VIDEO_PROCESS_DANMAKU": True,
        }

    return app
