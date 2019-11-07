from flask import Flask,  jsonify, request
from flask_cors import CORS
import uuid
import os

BOOKS = [
    {
        'book_id': uuid.uuid4().hex,
        'title': 'The Fifth Season',
        'author': 'N.K. Jemesin',
        'read': True
    },
    {
        'book_id': uuid.uuid4().hex,
        'title': 'The Warrior who carried Life',
        'author': 'Geoff Ryman',
        'read': True
    },
    {
        'book_id': uuid.uuid4().hex,
        'title': 'Words of Radiance',
        'author': 'Brandon Sanderson',
        'read': True
    },
    {
        'book_id': uuid.uuid4().hex,
        'title': 'Roadside Picnic',
        'author': 'Arkady Strugatsky',
        'read': True
    },
    {
        'book_id': uuid.uuid4().hex,
        'title': 'Perdido Street Station',
        'author': 'China Mieville',
        'read': True
    },
]

#configuration
DEBUG = True

#instantiate the app
app = Flask(__name__)
app.config.from_object(__name__)

# enable CORS
CORS(app, resources={r'/*': {'origins': '*'}})


# sanity check route
@app.route('/ping', methods=['GET'])


def ping_pong():
    return jsonify('poof!')

@app.route('/books', methods=['GET', 'POST'])
def all_books():
    response_object = {'status': 'success'}
    if request.method == 'POST':
        post_data = request.get_json()
        BOOKS.append({
            'book_id': post_data.get('book_id'),
            'title': post_data.get('title'),
            'author': post_data.get('author'),
            'read': post_data.get('read')
        })
        response_object['message'] = 'Book added!'
    else:
        response_object['books'] = BOOKS

    return jsonify(response_object)

@app.route('/books/<book_id>', methods=['PUT', 'DELETE'])
def single_book(book_id):
    response_object = {'status': 'success'}
    if request.method == 'PUT':
        get_data = request.get_json()
        remove_book(book_id)
        BOOKS.append({
            'book_id': book_id,
            'title': get_data.get('title'),
            'author': get_data.get('author'),
            'read': get_data.get('read')
        })
        response_object['message'] = 'Book Updated!'
    if request.method == 'DELETE':
        # todo: need to test remove_book
        remove_book(book_id)
        response_object['message'] = 'Book removed!'
    return jsonify(response_object)

def remove_book(book_id):
    for book in BOOKS:
        if book['book_id'] == book_id:
            BOOKS.remove(book)
            return True
    return False



if __name__ == '__main__':
    port = int(os.getenv("PORT", 5000))
    app.run(host='0.0.0.0', port=port)
