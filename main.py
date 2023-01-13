import subprocess
from loggerController import logger
from app import app

logger.add("log/server.log")

if __name__ == "__main__":
    subprocess.Popen("celery -A celery_app worker -l info", shell=True)
    logger.info("Start Celery Worker Server Successfully")

    logger.info("Start FastAPI Server")
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
