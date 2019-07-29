from flask import Flask,  jsonify
from flask_cors import CORS

BOOKS = [
    {
        'title': 'The Fifth Season',
        'author': 'N.K. Jemesin',
        'reae': True
    },
    {
        'title': 'The Warrior who carried Life',
        'author': 'Geoff Ryman',
        'reae': True
    },    {
        'title': 'Words of Radiance',
        'author': 'Brandon Sanderson',
        'reae': True
    },    {
        'title': 'Roadside Picnic',
        'author': 'Arkady Strugatsky',
        'reae': True
    },    {
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

@app.route('/books', methods=['GET'])
def all_books():
    return jsonify({
        'status': 'success',
        'books': BOOKS
    })



if __name__ == '__main__':
    app.run()
