from loggerController import logger
from server.app import app

logger.add("log/server.log")

if __name__ == "__main__":
    logger.info("Start FastAPI Server")
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=5000)
