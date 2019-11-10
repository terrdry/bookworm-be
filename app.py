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

def get_book(search_id, book_list):
    return [x for x in book_list if search_id in x['book_id']]




@app.route('/books', methods=['GET', 'POST'])
def all_books():
    response_object = {'status': 'success'}
    if request.method == 'POST':
        post_data = request.get_json()
        bookID = uuid.uuid4().hex

        BOOKS.append({
            'book_id': bookID,
            'title': post_data.get('title'),
            'author': post_data.get('author'),
            'read': post_data.get('read')
        })
        response_object['message'] = 'Book added!'
        response_object['book_id'] = bookID
    else:
        response_object['books'] = BOOKS

    return jsonify(response_object)

@app.route('/books/<book_id>', methods=['PUT', 'DELETE'])
def single_book(book_id):
    ret_code = 200
    response_object = {'status': 'success'}
    if request.method == 'PUT':
        get_data = request.get_json()
        if not update_book(book_id):
            response_object = {'status': 'failure'}
            response_object['message'] = 'Book Not Found!'
            ret_code = 404
    if request.method == 'DELETE':
        # todo: need to test remove_book
        if remove_book(book_id):
            response_object['message'] = 'Book removed!'
        else:
            response_object = {'status': 'failure'}
            response_object['message'] = 'Book Not Removed!'
            ret_code = 404
    return jsonify(response_object), ret_code

def remove_book(book_id):
    for book in BOOKS:
        if book['book_id'] == book_id:
            BOOKS.remove(book)
            return True
    return False


def update_book(book_id):
    # Get the stuff that got sent to us
    post_data = request.get_json()
    try:
        # find the book in the list
        ans = [indx for indx, book in enumerate(BOOKS) if book['book_id'] == book_id][0]
        BOOKS[ans]['book_id'] = post_data['book_id']
        BOOKS[ans]['title'] = post_data['title']
        BOOKS[ans]['author'] = post_data['author']
        BOOKS[ans]['read'] = post_data['read']
    except IndexError:
        return False
    return True


if __name__ == '__main__':
    port = int(os.getenv("PORT", 5000))
    app.run(host='0.0.0.0', port=port)
