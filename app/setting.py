

from starlette.config import Config
from starlette.datastructures import Secret


try:
    config = Config(".env")

except FileNotFoundError:
    config = Config()

DATABASE_TODO_NEW = config("DATABASE_TODO_NEW", cast=Secret)

