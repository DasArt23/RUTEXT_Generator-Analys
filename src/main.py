import logging
from config import TextsGetter

logging.basicConfig(
    filename='app.log',
    filemode='w',
    level=logging.DEBUG,
    format='%(asctime)s [%(levelname)s] %(message)s',
    encoding='utf-8'
)


def main():
    texts = TextsGetter()
    data = texts.run()
    for text in data:
        print(text)


if __name__ == "__main__":
    main()
