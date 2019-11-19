from sqlalchemy import create_engine
import json
import urllib.request
from random_word import RandomWords
from dataclasses import dataclass
from pprint import pprint


engine = create_engine("sqlite:////home/gronek/Documents/wdi_baza/db.db",
                       echo=True)
rando = RandomWords()
@dataclass
class Book:
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


@dataclass(init=True, repr=False, eq=False)
class User:
    username: str
    penalties: float
    borrowed_books: tuple
    first_name: str
    last_name: str
    address: str

with open("conf.cfg", "r") as conf:
    key=conf.readline
api_url = "https://www.googleapis.com/books/v1/volumes?key="+key+"&maxResults=1&q="


def generateBook(keyword: str, url: str) -> Book:
    print(keyword)
    final_url = (url+keyword).replace(" ", "+")
    resp = json.loads(urllib.request.urlopen(final_url).read().decode('utf-8'))
    book = resp['items'][0]['volumeInfo']
    # print(book.keys())
    return Book(book['title'],
                book['authors'] if 'authors' in book.keys() else None,
                None,
                book['publisher'] if 'publisher' in book.keys() else None,
                book['pageCount'] if 'pageCount' in book.keys() else None,
                book['averageRating'] if 'averageRating' in book.keys() else None,
                book['maturityRating'] if 'maturity_rating' in book.keys() else None,
                tuple(book['categories']) if 'categories' in book.keys() else None,
                'available',
                book['publishedDate'] if 'publishedDate' in book.keys() else None,
                None,
                book['language'] if 'language' in book.keys() else None)

books = [generateBook(keyword, api_url)
         for keyword in rando.get_random_words(limit=100)]


