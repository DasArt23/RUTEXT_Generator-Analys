import logging
from config import AppConfig

logging.basicConfig(
    filename='app.log',
    level=logging.DEBUG,
    format='%(asctime)s [%(levelname)s] %(message)s',
    encoding='utf-8'
)


def main():
    app = AppConfig(
        urls=[""],
        filenames=[],
    )
    app.run()


if __name__ == "__main__":
    main()
