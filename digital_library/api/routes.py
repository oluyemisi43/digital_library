from flask import Blueprint, request, jsonify
from digital_library.helpers import token_required
from digital_library.models import db,User,Book,book_schema,books_schema

api = Blueprint('api', __name__, url_prefix = '/api')

# CREATE book ENDPOINT
@api.route('/books', methods = ['POST'])
@token_required
def create_book(current_user_token):
    isbn = request.json['isbn']
    author = request.json['author']
    title = request.json['title']
    length = request.json['length']
    publish_year = request.json['publish_year']
    publisher = request.json['publisher']
    genre = request.json['genre']
    hardcover_paperback = request.json['hardcover_paperback']
    country = request.json['country']
    user_token = current_user_token.token

    print(f'BIG TESTER: {current_user_token.token}')

    book = Book(isbn, author, title, length, publish_year, publisher, genre, hardcover_paperback, country, user_token = user_token )

    db.session.add(book)
    db.session.commit()

    response = book_schema.dump(book)
    return jsonify(response)

    # RETRIEVE ALL books ENDPOINT
@api.route('/books', methods = ['GET'])
@token_required
def get_books(current_user_token):
    owner = current_user_token.token
    books = Book.query.filter_by(user_token = owner).all()
    response = books_schema.dump(books)
    return jsonify(response)

    # RETRIEVE ONE book ENDPOINT
@api.route('/books/<id>', methods = ['GET'])
@token_required
def get_book(current_user_token, id):
    owner = current_user_token.token
    if owner == current_user_token.token:
        book = Book.query.get(id)
        response = book_schema.dump(book)
        return jsonify(response)
    else:
        return jsonify({"message": "Valid Token Required"}),401

     # UPDATE book ENDPOINT
@api.route('/books/<id>', methods = ['POST','PUT'])
@token_required
def update_book(current_user_token,id):
    book = Book.query.get(id) # GET book INSTANCE

    book.isbn = request.json['isbn']
    book.author = request.json['author']
    book.title = request.json['title']
    book.length = request.json['length']
    book.publish_year = request.json['publish_year']
    book.publisher = request.json['publisher']
    book.genre = request.json['genre']
    book.hardcover_paperback = request.json['hardcover_paperback']
    book.country = request.json['country']
    book.user_token = current_user_token.token

    db.session.commit()
    response = book_schema.dump(book)
    return jsonify(response)

    # DELETE book ENDPOINT
@api.route('/books/<id>', methods = ['DELETE'])
@token_required
def delete_book(current_user_token, id):
    book = Book.query.get(id)
    db.session.delete(book)
    db.session.commit()
    response = Book_schema.dump(book)
    return jsonify(response)   