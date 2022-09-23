from abc import abstractmethod
from typing import Any


class Connectable:
    @abstractmethod
    def ping(self) -> bool:
        """
        Проверка возможности подключения к источнику данных

        :return: результат возможности подключения в булевом варианте
        """

    @abstractmethod
    def connection(self) -> Any:
        """Установка соединения с источником данных"""
        pass


class Cache:
    pass
