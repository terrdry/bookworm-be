from bookworm import app
import json
import unittest
import uuid
from bookworm.helper import provision_database
from bookworm import db
from bookworm.models import Books


class TestBookMain(unittest.TestCase):
    new_book = {'book_id': uuid.uuid4().hex,
                'title': "Childhood's End",
                'author': "Arthur C. Clarke",
                'read': True
                }

    def setUp(self):
        provision_database()

    def test_books_index(self):
        tester = app.test_client(self)
        response = tester.get('/books', content_type='html/text')
        self.assertEqual(200, response.status_code)

    def test_books_json(self):
        tester = app.test_client(self)
        response = tester.get('/books', content_type='html/text')
        self.assertIsInstance(response.json['books'], list)

    def test_books_list_length(self):
        tester = app.test_client(self)
        response = tester.get('/books', content_type='html/text')
        self.assertEqual(5, len(response.json['books']))

    def test_books_first_entry(self):
        tester = app.test_client(self)
        response = tester.get('/books', content_type='html/text')
        self.assertEqual('N.K. Jemesin', response.json['books'][0]['author'])

    def tearDown(self):
        Books.query.delete()
        db.session.commit()


class TestBookHelper:
    @staticmethod
    def count_records():
        return len(Books.query.all())

    @staticmethod
    def ret_book(search_id):
        book_record = db.session.query(Books).filter(Books.id == search_id).first()
        return [dict(id=book_record.id,
                     title=book_record.title,
                     author=book_record.author,
                     read=book_record.read
                     )]


class TestBookExercise(unittest.TestCase):
    book_idnum = 2
    new_book = {'book_id': '',
                'title': "Hyperion",
                'author': "Dan Simmons",
                'read': True
                }

    def setUp(self):
        provision_database()

    def test_add_book(self):
        tester = app.test_client(self)
        self.assertEqual(5, TestBookHelper.count_records())

        response = tester.post('/books',
                               data=json.dumps(self.new_book),
                               content_type='application/json')
        self.assertEqual(200, response.status_code)
        self.assertEqual(6, TestBookHelper.count_records())

    def test_change_book(self):
        tester = app.test_client(self)
        self.assertEqual(5, TestBookHelper.count_records())
        self.new_book['book_id'] = self.book_idnum
        self.new_book['title'] = "foo"
        self.new_book['author'] = "not"
        response = tester.put('/books/%s' % self.book_idnum,
                              data=json.dumps(self.new_book),
                              content_type='application/json')
        self.assertEqual(200, response.status_code)
        self.assertEqual(5, TestBookHelper.count_records())
        self.assertEqual('foo', TestBookHelper.ret_book(TestBookExercise.book_idnum)[0]['title'])

    def test_change_book_not_there(self):
        tester = app.test_client(self)
        self.assertEqual(5, TestBookHelper.count_records())

        response = tester.put('/books/%s' % 'NOT THERE',
                              data=json.dumps(self.new_book),
                              content_type='application/json')
        self.assertEqual(404, response.status_code)

    def test_delete_book_not_there(self):
        tester = app.test_client(self)
        response = tester.delete('/books/%s' % 'NOT THERE',
                                 content_type='application/json')
        self.assertEqual(404, response.status_code)

    def test_delete_book(self):
        tester = app.test_client(self)
        self.assertEqual(5, TestBookHelper.count_records())

        response = tester.delete('/books/%s' % TestBookExercise.book_idnum,
                                 content_type='application/json')
        self.assertEqual(200, response.status_code)
        self.assertEqual(4, TestBookHelper.count_records())

    def tearDown(self):
        Books.query.delete()
        db.session.commit()
