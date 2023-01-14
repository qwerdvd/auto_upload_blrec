import os

from dotenv import load_dotenv

from loggerController import logger
from utils import file_operation
from server import get_app
from server.config.config import BaseConfig

logger.add("log/server.log")
load_dotenv()
work_dir = os.getenv("WORK_DIR")

app = get_app()


if __name__ == "__main__":
    if work_dir is None:
        logger.error("WORK_DIR not set")
        raise ValueError("WORK_DIR not set")

    config = file_operation.readYml(os.path.join(work_dir, 'config', 'config.yml'))
    config = BaseConfig(config)
    import uvicorn

    uvicorn.run('main:app', host='127.0.0.1', port=5000, reload=True)
