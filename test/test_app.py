from app import app
import json
import unittest
import uuid


class TestBookMain(unittest.TestCase):
    new_book = {'book_id': uuid.uuid4().hex,
                'title': "Childhood's End",
                'author': "Arthur C. Clarke",
                'read': True
                }

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

class TestBookHelper():
    @staticmethod
    def count_records(test_obj):
        response = test_obj.get('/books', content_type='application/json')
        return len(response.json['books'])

    @staticmethod
    def ret_book(test_obj, search_id):
        response = test_obj.get('/books', content_type='application/json')
        book_list = response.json['books']
        return [x for x in book_list if search_id in x['book_id']]

class TestBookExercise(unittest.TestCase):
    book_id = 0
    def setUp(self):
        self.new_book = {'book_id': '',
                         'title': "Hyperion",
                         'author': "Dan Simmons",
                         'read': True
                         }

    def test_add_book(self):
        tester = app.test_client(self)
        self.assertEqual(5, TestBookHelper.count_records(tester))

        response = tester.post('/books',
                               data=json.dumps(self.new_book),
                               content_type='application/json')
        TestBookExercise.book_id = response.json['book_id']
        self.assertEqual(200, response.status_code)
        self.assertEqual(6, TestBookHelper.count_records(tester))

    def test_change_book(self):
        tester = app.test_client(self)
        self.assertEqual(6, TestBookHelper.count_records(tester))
        self.new_book['book_id'] = TestBookExercise.book_id
        self.new_book['title'] = "foo"
        response = tester.put('/books/%s' % TestBookExercise.book_id,
                               data=json.dumps(self.new_book),
                               content_type='application/json')
        self.assertEqual(200, response.status_code)
        self.assertEqual(6, TestBookHelper.count_records(tester))
        self.assertEqual('foo', TestBookHelper.ret_book(tester, TestBookExercise.book_id)[0]['title'])

    def test_change_book_not_there(self):
        tester = app.test_client(self)
        self.assertEqual(6, TestBookHelper.count_records(tester))

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
        self.assertEqual(6, TestBookHelper.count_records(tester))

        response = tester.delete('/books/%s' % TestBookExercise.book_id,
                                 content_type='application/json')
        self.assertEqual(200, response.status_code)
        self.assertEqual(5, TestBookHelper.count_records(tester))

    def tearDown(self):
        pass
