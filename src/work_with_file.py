import os
import logging
from typing import Any, Callable, TextIO


class WorkWithFile:
    def __init__(self, files_path="exFiles"):
        self.project_path = os.path.dirname(os.path.abspath(__file__))
        self.files_path = self.project_path + '/' + files_path
        self.create_dir(self.files_path)

    def write_file(self, text: str, filename: str = "file.txt") -> None:
        logging.info(f"Запись в файл {filename}")

        def write_text(file: TextIO):
            file.write(text)
        
        return self.__do_action(mode='w', filename=filename, func=write_text)

    def read_file(self, filename: str = "file.txt") -> str:
        logging.info(f"Чтение файла {filename}")
        
        def read_file(file: TextIO):
            text = file.read()
            return text
        
        return self.__do_action(mode='r', filename=filename, func=read_file)

    def exist_file(self, filename: str) -> bool:
        path = self.files_path + '/' + filename
        if os.path.exists(path): 
            return True
        return False

    def create_dir(self, path: str) -> None:
        os.makedirs(path, exist_ok=True)

    def __do_action(self, mode: str, filename: str, func: Callable[[TextIO], [Any]]) -> Any:
        if not self.exist_file(filename) and mode != 'w':
            logging.error(f"Файла {filename} в {self.files_path} не сущесвует")
            return
        path = self.files_path + '/' + filename
        res = None
        with open(path, mode=mode, encoding="utf-8") as file:
            res = func(file)
        return res

