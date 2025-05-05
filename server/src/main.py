import logging.config

from src.logging_config import LOGGING_CONFIG
from src.server import server


def main() -> None:
    server()


if __name__ == "__main__":
    logging.config.dictConfig(LOGGING_CONFIG)

    main()
