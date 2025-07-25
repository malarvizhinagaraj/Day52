from flask import Flask, request, jsonify

app = Flask(__name__)

books = []
next_id = 1

# GET all or filter
@app.route('/books', methods=['GET'])
def get_books():
    author = request.args.get('author')
    if author:
        filtered = [book for book in books if book['author'].lower() == author.lower()]
        return jsonify(filtered)
    return jsonify(books)

# POST a new book
@app.route('/books', methods=['POST'])
def add_book():
    global next_id
    data = request.get_json()
    if not data.get('title') or not data.get('author') or not data.get('year'):
        return jsonify({'error': 'Missing title, author, or year'}), 400
    book = {
        'id': next_id,
        'title': data['title'],
        'author': data['author'],
        'year': data['year']
    }
    books.append(book)
    next_id += 1
    return jsonify(book), 201

# GET single book
@app.route('/books/<int:book_id>', methods=['GET'])
def get_book(book_id):
    for book in books:
        if book['id'] == book_id:
            return jsonify(book)
    return jsonify({'error': 'Book not found'}), 404

# PUT update
@app.route('/books/<int:book_id>', methods=['PUT'])
def update_book(book_id):
    data = request.get_json()
    for book in books:
        if book['id'] == book_id:
            if 'title' in data:
                book['title'] = data['title']
            if 'author' in data:
                book['author'] = data['author']
            if 'year' in data:
                book['year'] = data['year']
            return jsonify(book)
    return jsonify({'error': 'Book not found'}), 404

# DELETE book
@app.route('/books/<int:book_id>', methods=['DELETE'])
def delete_book(book_id):
    for book in books:
        if book['id'] == book_id:
            books.remove(book)
            return jsonify({'message': f'Book {book_id} deleted'})
    return jsonify({'error': 'Book not found'}), 404

if __name__ == '__main__':
    app.run(debug=True)
