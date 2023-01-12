import uvicorn
from loggerController import logger
from app import app

logger.add("log/server.log")

if __name__ == "__main__":
    logger.info("Start Server")
    uvicorn.run("main:app", host="127.0.0.1", port=5000, workers=2, reload=True)
