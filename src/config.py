import logging
from typing import Iterable
from text_source.source import Source, ParseSource, FileSource
from work_with_file import WorkWithFile


class AppConfig:
    _instance = None
    _initialized = False
    SYM = "#GEN"

    def __new__(cls, *args, **kwargs):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance
    
    def __init__(self, source_file: str = "data.csv") -> None:
        if self._initialized:
            return

        self.files = "Texts"
        self.data_file = source_file
        self.file_mang: WorkWithFile = WorkWithFile(files_path=self.files)
        logging.info("Создан экзэмпляр AppConfig")

        self._initialized = True
    
    def check_data_file(self):
        path = self.file_mang.project_path + "/" + self.data_file
        first = ""
        try:
            with open(path, mode='r', encoding="utf-8") as file:
                first = file.readline()
            if first.startswith(self.SYM):
                logging.info("Файл с данными для получения текста найдены")
            else:
                raise FileNotFoundError
        except FileNotFoundError:
            with open(path, mode='w', encoding="utf-8") as file:
                file.write(self.SYM + "\n")
                file.write("type;url;filename;\n")
                logging.info("Файл с данными создан")

    def run(self):
        self.check_data_file()
        data = self.get_data()

    def get_data(self):
        data = {
            "types": [],
            "urls": [],
            "files": [],
        }
        return data
