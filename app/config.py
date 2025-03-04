#from functools import lru_cache
#from pydantic_settings import BaseSettings
#import pathlib
#
#ROOT_DIR: pathlib.Path = pathlib.Path(__file__).parent.parent.resolve()
#
#class Settings(BaseSettings):
#    or_url: str
#    or_api: str
#    
#    gcp_credential: str
#    gcp_project: str
#    gcp_genai_location: str
#    class Config:
#        env_file = f"{str(ROOT_DIR)}/.env"
