from typing import Optional

from pydantic import BaseSettings, SecretStr, Field


class Settings(BaseSettings):
    class Config:
        env_file = '.env'
        json_encoders = {
            SecretStr: lambda v: v.get_secret_value() if v else None,
        }


class Project(Settings):
    name: str = 'Movies'

    class Config(Settings.Config):
        env_prefix = 'PROJECT_'


class Redis(Settings):
    host: str = '127.0.0.1'
    port: int = 6379
    pool_minsize: int = 10
    pool_maxsize: int = 20
    password: Optional[str] = None

    class Config(Settings.Config):
        env_prefix = 'REDIS_'


class Elastic(Settings):
    host: str = '127.0.0.1'
    port: int = 9200

    class Config(Settings.Config):
        env_prefix = 'ELASTIC_'


class Logger(Settings):
    log_level: str = 'DEBUG'
    force: bool = True
    enable_additional_debug: bool = True

    class Config(Settings.Config):
        env_prefix = 'LOG_'


class ExternalService(Settings):
    auth: str

    class Config(Settings.Config):
        env_prefix = 'EXTERNAL_'


class Test(Settings):
    token: Optional[str] = None

    class Config(Settings.Config):
        env_prefix = 'TEST_'


class Envs(Settings):
    project: Project = Project()
    redis: Redis = Redis()
    elastic: Elastic = Elastic()
    logger: Logger = Logger()
    external: ExternalService = ExternalService()
    test: Test = Test()


envs = Envs()
