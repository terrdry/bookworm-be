from . import app
from flask import jsonify, request
from .helper import load_booktable, add_book, modify_book, delete_book


@app.route('/books', methods=['GET', 'POST'])
def all_books():
    response_object = {'status': 'success'}
    if request.method == 'POST':
        post_data = request.get_json()
        new_book = dict(id=0,
                        title=post_data.get('title'),
                        author=post_data.get('author'),
                        read=post_data.get('read'))
        new_book_id = add_book(new_book)
        response_object['message'] = 'Book added!'
        response_object['book_id'] = new_book_id
    else:
        response_object['books'] = load_booktable()

    return jsonify(response_object)


@app.route('/books/<book_id>', methods=['PUT', 'DELETE'])
def single_book(book_id):
    ret_code = 200
    response_object = {'status': 'success'}
    if request.method == 'PUT':
        if not update_book(book_id):
            response_object = dict(status="failure")
            response_object['message'] = 'Book Not Found!'
            ret_code = 404
    if request.method == 'DELETE':
        if remove_book(book_id):
            response_object['message'] = 'Book removed!'
        else:
            response_object = dict(status='failure')
            response_object['message'] = 'Book Not Removed!'
            ret_code = 404
    return jsonify(response_object), ret_code


def remove_book(book_id):
    return delete_book(book_id)


def update_book(book_id):
    # Get the stuff that got sent to us
    post_data = request.get_json()
    ret_val = modify_book(dict(id=book_id,
                               title=post_data.get('title'),
                               author=post_data.get('author'),
                               read=post_data.get('read')
                               )
                          )
    return ret_val
