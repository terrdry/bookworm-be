from . import app
from .models import Books
from . import db
from flask import jsonify, request
from .helper import load_booktable


@app.route('/books', methods=['GET', 'POST'])
def all_books():
    response_object = {'status': 'success'}
    if request.method == 'POST':
        post_data = request.get_json()
        new_book = Books(title=post_data.get('title'),
                         author=post_data.get('author'),
                         read=post_data.get('read'))
        db.session.add(new_book)
        db.session.commit()
        response_object['message'] = 'Book added!'
        response_object['book_id'] = new_book.id
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
    book_record = db.session.query(Books).get(book_id)
    if book_record:
        db.session.delete(book_record)
        db.session.commit()
        return True
    else:
        return False


def update_book(book_id):
    # Get the stuff that got sent to us
    post_data = request.get_json()
    book_record = db.session.query(Books).get(book_id)
    if book_record:
        book_record.title = post_data['title']
        book_record.author = post_data['author']
        book_record.read = post_data['read']
        db.session.commit()
        return True
    else:
        return False
