from pydantic import BaseSettings, SecretStr


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
    password: str | None = None

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


class Envs(Settings):
    project: Project
    redis: Redis
    elastic: Elastic
    logger: Logger


envs = Envs()
