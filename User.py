from dataclasses import dataclass


@dataclass
class User:
    identifier: int
    username: str
    limit: int = 5
