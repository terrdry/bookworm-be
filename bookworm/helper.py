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


def add_book(book):
    new_book = Books(id=book['id'],
                     title=book['title'],
                     author=book['author'],
                     read=book['read']
                     )
    db.session.add(new_book)
    db.session.commit()
    return new_book.id


def modify_book(book):
    book_record = db.session.query(Books).get(book['id'])
    if book_record:
        book_record.title = book['title']
        book_record.author = book['author']
        book_record.read = book['read']
        db.session.commit()
        return True
    else:
        return False


def return_book(book_id):
    book_record = db.session.query(Books).get(book_id)
    return [dict(id=book_record.id,
                 title=book_record.title,
                 author=book_record.author,
                 read=book_record.read
                 )]


def delete_book(book_id):
    book_record = db.session.query(Books).get(book_id)
    if book_record:
        db.session.delete(book_record)
        db.session.commit()
        return True
    else:
        return False




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
