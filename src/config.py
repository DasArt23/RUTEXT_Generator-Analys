import logging
import pandas as pd
from text_source.source import ParseSource, FileSource
from typing import Iterable
from work_with_file import WorkWithFile


class TextsGetter:
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

        self.files_dir = "Texts"
        self.file_mang: WorkWithFile = WorkWithFile(files_path=self.files_dir)
        self.data_path = self.file_mang.project_path + "/" + source_file
        self.text_gen = 0
        self.urls: list[dict[str, str]] = []
        self.files: list[dict[str, str]] = []
        logging.info("Создан экзэмпляр AppConfig")

        self._initialized = True
    
    def check_data_file(self):
        first = ""
        try:
            with open(self.data_path, mode='r', encoding="utf-8") as file:
                first = file.readline()
            if first.startswith(self.SYM):
                logging.info("Файл с данными для получения текста найдены")
            else:
                raise FileNotFoundError
        except FileNotFoundError:
            with open(self.data_path, mode='w', encoding="utf-8") as file:
                file.write(self.SYM + ",url,file\n")
                logging.info("Файл с данными создан")

    def run(self) -> Iterable[str]:
        self.check_data_file()
        data: list[dict[str, str]] = self.get_data()
        logging.info(f"Получены данные из {self.data_path}")
        
        self.get_lists(data)
        parse_source = ParseSource(urls=[data['url'] for data in self.urls])
        file_source = FileSource(files=[data['file'] for data in self.files], 
                                 dir_name=self.files_dir)
        
        parse_text = parse_source.get_text()
        file_text = file_source.get_text()
        
        def get_texts():
            if parse_text is not None:
                for text, data in zip(parse_text, self.urls):
                    self.file_mang.write_file(text, data.get('file', 'file.txt'))
                    yield text
            if file_text is not None:
                yield from file_text
        return get_texts()
        
    def get_lists(self, data: dict[str, str]) -> None:
        self.urls, self.files = [], []
        for row in data:
            if row['file']:
                if self.file_mang.exist_file(row['file']):
                    self.files.append({'file': row['file']})
                    logging.info(f"FILE: {row['file']}")
                elif row['url']:
                    self.urls.append({'url': row['url'], 'file': row['file']})
                    logging.info(f"PARSE: {row['url']}")
            logging.info("Данных нет")

    def get_data(self) -> list[dict[str, str]]:
        """Словарь: url, file"""
        data = pd.read_csv(self.data_path, dtype_backend="numpy_nullable")
        js_data = data.drop(columns=[self.SYM]).to_dict(orient="records")
        return js_data
