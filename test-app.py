from app import app
import json
import unittest


class BasicTestCase(unittest.TestCase):

    def test_books_index(self):
        tester = app.test_client(self)
        response = tester.get('/books', content_type='html/text')
        self.assertEqual(response.status_code, 200)
        bookData = json.loads(response.data)
        self.assertEqual(len(bookData['books']), 5)


if __name__ == '__main__':
    unittest.main()
