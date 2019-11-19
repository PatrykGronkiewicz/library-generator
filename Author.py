from dataclasses import dataclass

@dataclass
class Author:
    identifier: int
    name: str
    books: tuple

