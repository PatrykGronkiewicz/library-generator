from dataclasses import dataclass

@dataclass
class Book:
    identifier: int
    title: str
    authors: tuple
    isbn: str
    publisher: str
    page_count: int
    rating: float
    maturity_rating: str
    category: tuple
    status: str
    publish_date: str
    series: str
    lang: str

