import logging
from typing import Iterable


class AppConfig:
    _instance = None
    _initialized = False

    def __new__(cls, *args, **kwargs):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance
    
    def __init__(self, urls: Iterable[str], filenames: Iterable[str]) -> None:
        if self._initialized:
            return
        self.urls = urls
        self.filenames = filenames
        if len(urls) != len(filenames):
            logging.error(f"Неверные данные: кол-во ссылок - {len(urls)} | кол-во названий файлов - {len(filenames)}")
            return
        logging.info("Создан экзэмплярAppConfig")
        self._initialized = True

    def run(self):
        print("Hello world!")
