from typing import Optional

from pydantic import BaseSettings


class Settings(BaseSettings):
    class Config(BaseSettings.Config):
        env_file = '../.env'
        env_prefix = 'TEST_'


class SettingsIntegration(Settings):
    host: str
    port: int


class TestApiSettings(SettingsIntegration):
    token: str

    class Config(Settings.Config):
        env_prefix = 'TEST_API_'


class TestElasticSettings(SettingsIntegration):
    class Config(Settings.Config):
        env_prefix = 'TEST_ELASTIC_'


class TestRedisSettings(SettingsIntegration):
    password: Optional[str] = '123qwe'
    pool_minsize: Optional[int] = 10
    pool_maxsize: Optional[int] = 20

    class Config(Settings.Config):
        env_prefix = 'TEST_REDIS_'


class TestSettings(Settings):
    elastic: TestElasticSettings = TestElasticSettings()
    redis: TestRedisSettings = TestRedisSettings()
    api: TestApiSettings = TestApiSettings()


test_settings = TestSettings()
