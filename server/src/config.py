import os
from dataclasses import dataclass, field


@dataclass
class ServerConfig:
    host: str = os.environ.get("SERVER_HOST", "0.0.0.0")
    port: str | int = os.environ.get("SERVER_PORT", 8000)


@dataclass
class LoggingConfig:
    level: str = os.environ.get("LOGGING_LEVEL", "INFO")

    def __post_init__(self) -> None:
        if self.level not in ["DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"]:
            raise ValueError(
                "Logging level should be DEBUG, INFO, WARNING, ERROR or CRITICAL"
            )


@dataclass
class Settings:
    server: ServerConfig = field(default_factory=ServerConfig)
    logging: LoggingConfig = field(default_factory=LoggingConfig)


settings = Settings()
