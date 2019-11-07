from app import app
import json
import unittest
import uuid
from app import get_book


class TestBookMain(unittest.TestCase):
    new_book = {'book_id': uuid.uuid4().hex,
                'title': "Childhood's End",
                'author': "Arthur C. Clarke",
                'read': True
                }

    def test_books_index(self):
        tester = app.test_client(self)
        response = tester.get('/books', content_type='html/text')
        self.assertEqual(response.status_code, 200)

    def test_books_json(self):
        tester = app.test_client(self)
        response = tester.get('/books', content_type='html/text')
        self.assertIsInstance(response.json, dict)

    def test_books_list_length(self):
        tester = app.test_client(self)
        response = tester.get('/books', content_type='html/text')
        self.assertEqual(len(response.json['books']), 5)

    def test_books_first_entry(self):
        tester = app.test_client(self)
        response = tester.get('/books', content_type='html/text')
        book_data = response.json
        self.assertEqual(book_data['books'][0]['author'], 'N.K. Jemesin')


class TestBookExercise(unittest.TestCase):
    new_book = {'book_id': uuid.uuid4().hex,
                'title': "Hyperion",
                'author': "Dan Simmons",
                'read': True
                }

    def setUp(self):
        # add a record
        tester = app.test_client(self)
        self.book_id = self.new_book['book_id']
        response = tester.post('/books', data=json.dumps(self.new_book), content_type='application/json')
        self.assertEqual(response.status_code, 200)

    @staticmethod
    def count_records(test_obj):
        response = test_obj.get('/books', content_type='application/json')
        return len(response.json['books'])

    def test_change_book(self):
        tester = app.test_client(self)
        self.assertEqual(6, TestBookExercise.count_records(tester))

        self.new_book['title'] = "foo"
        response = tester.put('/books/%s' % self.book_id,
                              data=json.dumps(self.new_book),
                              content_type='application/json')

        book_stuff = tester.get('/books', content_type='application/json').json['books']

        x = get_book(self.book_id, book_stuff)

        self.assertEqual('foo', get_book(self.book_id, book_stuff)[0]['title'])


    def tearDown(self):
        tester = app.test_client(self)
        # what is there
        res = tester.get('/books', content_type='applicaiton/html')
        myLeng = len(res.json['books'])
        response = tester.delete('/books/%s' % self.book_id, content_type='application/html')
        res = tester.get('/books', content_type='applicaiton/html')
        myLeng = len(res.json['books'])
        self.assertEqual(response.status_code, 200)



