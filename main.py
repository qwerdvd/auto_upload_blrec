# import subprocess
from loggerController import logger
from server.app import app

logger.add("log/server.log")

if __name__ == "__main__":
    # subprocess.Popen("celery -A celery_app worker -l info", shell=True)
    # logger.info("Start Celery Worker Server Successfully")

    logger.info("Start FastAPI Server")
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=5000)
