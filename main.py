from sqlalchemy import create_engine
import json
import urllib.request
from random_word import RandomWords
from dataclasses import dataclass
from pprint import pprint
from User import User
from Author import Author
from Book import Book
import pickle


rando = RandomWords()
engine = create_engine("sqlite:////home/gronek/Documents/wdi_baza/db.db",
                       echo=True)

with open("conf.cfg", "r") as conf:
    key=conf.readline()[:-1]
api_url = "https://www.googleapis.com/books/v1/volumes?key="+key+"&maxResults=1&q="


def generateBook(keyword: str, url: str, identifier: int) -> Book:
    final_url = (url+keyword).replace(" ", "+")
    resp = json.loads(urllib.request.urlopen(final_url).read().decode('utf-8'))
    book = resp['items'][0]['volumeInfo']
    return Book(identifier,
                book['title'],
                book['authors'] if 'authors' in book.keys() \
                                else tuple([]),
                None,
                book['publisher'] if 'publisher' in book.keys() \
                                else None,
                book['pageCount'] if 'pageCount' in book.keys() \
                                else None,
                book['averageRating'] if 'averageRating' in book.keys() \
                                else None,
                book['maturityRating'] if 'maturity_rating' in book.keys() \
                                else None,
                tuple(book['categories']) if 'categories' in book.keys() \
                                else tuple([]),
                'available',
                book['publishedDate'] if 'publishedDate' in book.keys() \
                                else None,
                None,
                book['language'] if 'language' in book.keys() \
                                else None)


try:
    with open('books.bin', 'rb') as books_file:
         books = pickle.load(books_file)
except (EOFError, FileNotFoundError):
    books = [generateBook(keyword, api_url, i)
             for i, keyword in enumerate(rando.get_random_words(limit=127))]
    with open('books.bin', 'wb+') as books_file:
        pickle.dump(books, books_file)

# generating authors list
authors_names = [name for name in (book.authors for book in books)
                 if name is not None]
authors_names_tmp = []
for name in authors_names:
    authors_names_tmp += name
authors_names = authors_names_tmp

# removing duplicates from authors
authors_names = list(dict.fromkeys(authors_names))

try:
    with open('authors.bin', 'rb') as authors_file:
        authors = pickle.load(authors_file)
except (EOFError, FileNotFoundError):
    authors = [Author(i,
                  name,
                  tuple(book.title for book in books if name in book.authors))
           for i, name in enumerate(authors_names)]
    with open('authors.bin', 'wb+') as authors_file:
        pickle.dump(authors, authors_file)

try:
    with open('users.bin', 'rb') as users_file:
        users = pickle.load(users_file)
except (EOFError, FileNotFoundError):
    users = [User(i, nick) for i, nick in enumerate(rando.get_random_words(limit=20))]
    with open('users.bin', 'wb+') as users_file:
        pickle.dump(users, users_file)

