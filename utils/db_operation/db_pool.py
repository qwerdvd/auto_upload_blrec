import sqlite3

import sqlalchemy.pool as pool  # type: ignore

db_pool = pool.QueuePool(
    lambda: sqlite3.connect('RECORD.db'),
    max_overflow=10,
    pool_size=5,
)
