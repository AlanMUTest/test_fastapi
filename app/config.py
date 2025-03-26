#from functools import lru_cache
from pydantic_settings import BaseSettings
#import pathlib
#
#ROOT_DIR: pathlib.Path = pathlib.Path(__file__).parent.parent.resolve()
#
class Settings(BaseSettings):
    max_num: int = 10
    max_file_size: int = 5000000
#    class Config:
#        env_file = f"{str(ROOT_DIR)}/.env"
settings = Settings()