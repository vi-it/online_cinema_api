import abc
import json
from typing import Any


class BaseStorage:
    @abc.abstractmethod
    def save_state(self, state: dict) -> None:
        """Сохранить состояние в постоянное хранилище"""
        pass

    @abc.abstractmethod
    def retrieve_state(self) -> dict:
        """Загрузить состояние локально из постоянного хранилища"""
        pass


class JsonFileStorage(BaseStorage):
    def __init__(self, file_path: str | None = None):
        self.file_path = file_path

    def save_state(self, state: dict) -> None:
        prev_state = self.retrieve_state()
        prev_state.update(state)
        with open(self.file_path, 'w', encoding='utf-8') as json_file:
            json.dump(prev_state, json_file, indent=4, sort_keys=True, default=str)

    def retrieve_state(self) -> dict:
        try:
            with open(self.file_path, 'r', encoding='utf-8') as json_file:
                state = json.load(json_file)
        except FileNotFoundError:
            state = {}
        except json.decoder.JSONDecodeError:
            state = {}
        return state


class State:
    """
    Класс для хранения состояния при работе с данными, чтобы постоянно не перечитывать данные с начала.
    Здесь представлена реализация с сохранением состояния в файл.
    В целом ничего не мешает поменять это поведение на работу с БД или распределённым хранилищем.
    """

    def __init__(self, storage: BaseStorage):
        self.storage = storage

    def set_state(self, key: str, value: Any) -> None:
        """Установить состояние для определённого ключа"""
        self.storage.save_state(state={key: value})

    def get_state(self, key: str) -> Any:
        """Получить состояние по определённому ключу"""
        state = self.storage.retrieve_state()
        return state.get(key, None)
