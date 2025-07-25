from flask import Flask, request, jsonify
import random

app = Flask(__name__)

quotes = []
quote_id_counter = 1

# 📋 GET all quotes
@app.route('/quotes', methods=['GET'])
def get_quotes():
    return jsonify({'quotes': quotes}), 200

# ✅ POST - Add a new quote
@app.route('/quotes', methods=['POST'])
def add_quote():
    global quote_id_counter
    data = request.get_json()
    text = data.get('text')
    author = data.get('author', 'Unknown')

    if not text:
        return jsonify({'error': 'Quote text is required.'}), 400

    quote = {
        'id': quote_id_counter,
        'text': text,
        'author': author
    }
    quotes.append(quote)
    quote_id_counter += 1

    return jsonify({'message': 'Quote added successfully!', 'quote': quote}), 201

# ✏️ PUT - Update quote
@app.route('/quotes/<int:quote_id>', methods=['PUT'])
def update_quote(quote_id):
    data = request.get_json()
    for quote in quotes:
        if quote['id'] == quote_id:
            quote['text'] = data.get('text', quote['text'])
            quote['author'] = data.get('author', quote['author'])
            return jsonify({'message': 'Quote updated.', 'quote': quote}), 200

    return jsonify({'error': 'Quote not found.'}), 404

# ❌ DELETE - Remove quote
@app.route('/quotes/<int:quote_id>', methods=['DELETE'])
def delete_quote(quote_id):
    for quote in quotes:
        if quote['id'] == quote_id:
            quotes.remove(quote)
            return jsonify({'message': f'Quote with ID {quote_id} deleted.'}), 200

    return jsonify({'error': 'Quote not found.'}), 404

# 🎲 GET random quote
@app.route('/quote/random', methods=['GET'])
def random_quote():
    if not quotes:
        return jsonify({'error': 'No quotes available.'}), 404
    return jsonify(random.choice(quotes)), 200

# 🚀 Run the app
if __name__ == '__main__':
    app.run(debug=True)
