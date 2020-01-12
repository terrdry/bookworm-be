from bookworm import db
from bookworm.models import Books
from bookworm.helper import provision_database
import unittest


class TestDatabase(unittest.TestCase):
    def setUp(self):
        self.title_name = "Wonderous Music"
        self.author_name = "moi"
        provision_database()

    def test_books_addDB(self):
        x = Books(title=self.title_name, author=self.author_name)
        self.assertEqual(x.title, self.title_name)
        self.assertEqual(x.author, self.author_name)

        self.assertEqual(len(Books.query.all()), 5)
        db.session.add(x)
        db.session.commit()
        self.assertEqual(len(Books.query.all()), 6)

    def test_books_delDB(self):
        x = db.session.query(Books).filter(Books.author == self.author_name)
        x.delete()
        what = Books.query.all()
        self.assertEqual(len(Books.query.all()), 5)

    def test_books_chgDB(self):
        # add the new record
        new = Books(title=self.title_name, author=self.author_name)
        db.session.add(new)
        db.session.commit()
        BookRecord = db.session.query(Books).filter(Books.author == self.author_name).first()
        BookRecord.title = "What"
        db.session.commit()
        BookRecord = db.session.query(Books).filter(Books.author == self.author_name).first()

        self.assertEqual(BookRecord.title, 'What')

    def tearDown(self):
        Books.query.delete()
        db.session.commit()
