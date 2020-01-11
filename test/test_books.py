from bookworm import db
from bookworm.models import Books
import unittest


class TestDatabase(unittest.TestCase):
    def test_books_addDB(self):
        title_name = "Wonderous Music"
        author_name = "moi"
        x = Books(title=title_name, author=author_name)
        y = x
        self.assertEqual(x.title, title_name)
        self.assertEqual(x.author, author_name)

        db.session.add(x)
        db.session.commit()

        x = 0
