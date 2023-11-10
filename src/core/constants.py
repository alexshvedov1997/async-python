from enum import Enum

ENDPOINT: str = "https://storage.yandexcloud.net"


class TokenType(Enum):
    bearer = "bearer"
