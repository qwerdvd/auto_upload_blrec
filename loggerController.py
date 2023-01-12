from functools import wraps
import os
import datetime
import loguru


def singleton_class_decorator(cls):
    _instance = {}

    @wraps(cls)
    def wrapper_class(*args, **kwargs):
        if cls not in _instance:
            _instance[cls] = cls(*args, **kwargs)
        return _instance[cls]

    return wrapper_class


@singleton_class_decorator
class Logger:
    def __init__(self):
        self.logger_add()

    def get_project_path(self, project_path=None):
        if project_path is None:
            project_path = os.path.realpath('..')
        return project_path

    def get_log_path(self):
        project_path = self.get_project_path()
        log_dir = os.path.join(project_path, 'log')
        log_filename = 'runtime_{}.log'.format(datetime.date.today())
        log_path = os.path.join(log_dir, log_filename)
        return log_path

    def logger_add(self):
        loguru.logger.add(
            sink=self.get_log_path(),
            rotation="1 day",
            retention="7 days",
            compression='zip',
            encoding="utf-8",
            enqueue=True
        )

    @property
    def get_logger(self):
        return loguru.logger


logger = Logger().get_logger
