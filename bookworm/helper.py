from .models import Books
from . import db

BOOKS = [
    {
        'title': 'The Fifth Season',
        'author': 'N.K. Jemesin',
        'read': True
    },
    {
        'title': 'The Warrior who carried Life',
        'author': 'Geoff Ryman',
        'read': True
    },
    {
        'title': 'Words of Radiance',
        'author': 'Brandon Sanderson',
        'read': True
    },
    {
        'title': 'Roadside Picnic',
        'author': 'Arkady Strugatsky',
        'read': False
    },
    {
        'title': 'Perdido Street Station',
        'author': 'China Mieville',
        'read': True
    },
]


def load_booktable():
    ''' This will create a list of dictionary items '''
    selection = [dict(book_id=book.id,
                      title=book.title,
                      author=book.author,
                      read=book.read
                      )
                 for book in Books.query.all()]
    return selection


def provision_database():
    for elem in BOOKS:
        new_book = Books(title=elem['title'],
                         author=elem['author'],
                         read=elem['read']
                         )
        db.session.add(new_book)
    db.session.commit()
    return True


if __name__ == "__main__":
    provision_database()
