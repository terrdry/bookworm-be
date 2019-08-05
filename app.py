from flask import Flask,  jsonify, request
from flask_cors import CORS
import uuid

BOOKS = [
    {
        'id': uuid.uuid4().hex,
        'title': 'The Fifth Season',
        'author': 'N.K. Jemesin',
        'reae': True
    },
    {
        'id': uuid.uuid4().hex,
        'title': 'The Warrior who carried Life',
        'author': 'Geoff Ryman',
        'reae': True
    },
    {
        'id': uuid.uuid4().hex,
        'title': 'Words of Radiance',
        'author': 'Brandon Sanderson',
        'reae': True
    },
    {
        'id': uuid.uuid4().hex,
        'title': 'Roadside Picnic',
        'author': 'Arkady Strugatsky',
        'reae': True
    },
    {
        'id': uuid.uuid4().hex,
        'title': 'Perdido Street Station',
        'author': 'China Mieville',
        'reae': True
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
            'id': uuid.uuid4().hex,
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
        post_data = request.get_json()
        remove_book(book_id)
        BOOKS.append({
            'id': uuid.uuid4().hex,
            'title': post_data.get('title'),
            'author': post_data.get('author'),
            'read': post_data.get('read')
        })
        response_object['message'] = 'Book Updated!'
    if request.method == 'DELETE':
        remove_book(book_id)
        response_object['message'] = 'Book removed!'
    return jsonify(response_object)

def remove_book(book_id):
    for book in BOOKS:
        if book['id'] == book_id:
            BOOKS.remove(book)
            return True
    return False



if __name__ == '__main__':
    app.run()
