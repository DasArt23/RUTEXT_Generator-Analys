from abc import ABC, abstractmethod
from fake_useragent import UserAgent
from bs4 import BeautifulSoup
from typing import Any, Iterable
import requests


class Source(ABC):
    name = "Demo"

    @abstractmethod
    def __init__(self, **kwargs):
        pass
    
    def get_name(self) -> str:
        return self.name    
    
    @abstractmethod
    def get_text(self) -> Iterable[str]:
        pass


class ParseText(Source):
    name = "Parse text"

    def __init__(self, **kwargs: Any):
        self.urls: list[str] | None = kwargs['urls'] if 'urls' in kwargs else None
        self.ua = UserAgent()

    def get_text(self) -> Iterable[str]:
        if not self.urls:
            return []
        
        return (self.get_text_from_page(url) for url in self.urls)
    
    def get_text_from_page(self, url: str) -> str:
        user_agent = self.ua.random
        headers = {'User-Agent': user_agent}
        res = self.get_page(url, headers)
        return self.page_text(res)

    @staticmethod
    def get_page(url: str, headers: dict[str, Any]) -> requests.Response:
        res = requests.get(url, headers=headers, timeout=10)
        res.raise_for_status()
        return res

    @staticmethod
    def page_text(page: requests.Response) -> str:
        soup = BeautifulSoup(page.text, 'html.parser')
        for el in soup(['script', 'style', 'meta', 'link']):
            el.decompose()

        text = soup.get_text(separator='\n', strip=True)
        lines = [line.strip() for line in text.splitlines() if line.strip()]
        cor_text = '\n'.join(lines)
        return cor_text

