from src.config import settings

LOGGING_CONFIG = {
    "version": 1,
    "disable_existing_loggers": False,
    "formatters": {
        "default": {
            "datefmt": "%Y-%m-%d %H:%M:%S",
            "format": "\033[90m[%(asctime)s.%(msecs)03d]\033[0m  %(name)-15s  \033[96m%(levelname)-5s\033[0m  %(message)s",
        },
    },
    "handlers": {
        "console": {
            "class": "logging.StreamHandler",
            "formatter": "default",
        },
    },
    "loggers": {
        "server": {
            "handlers": ["console"],
            "level": settings.logging.level,
            "propagate": False,
        },
    },
    "root": {
        "handlers": ["console"],
        "level": "WARNING",
    },
}
