import uvicorn
from loggerController import logger, Logger
from concurrent.futures import ThreadPoolExecutor
from asyncio.windows_events import ProactorEventLoop
from app import app

if __name__ == "__main__":
    logger.info("Start Server")
    Logger().logger_add()
    uvicorn.run("main:app", host="127.0.0.1", port=5000, workers=2, reload=True)
