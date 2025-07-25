from flask import Flask, request, jsonify

app = Flask(__name__)
cart = []

@app.route('/cart', methods=['GET'])
def get_cart():
    return jsonify(cart)

@app.route('/cart', methods=['POST'])
def add_item():
    data = request.get_json()
    name = data.get('product_name')
    qty = data.get('quantity')
    price = data.get('price')
    if not name or type(qty) is not int or type(price) not in [int, float]:
        return jsonify({'error': 'Invalid input'}), 400
    cart.append({'product_name': name, 'quantity': qty, 'price': price})
    return jsonify({'message': 'Item added'}), 201

@app.route('/cart/<string:name>', methods=['PUT'])
def update_item(name):
    data = request.get_json()
    for item in cart:
        if item['product_name'] == name:
            item['quantity'] = data.get('quantity', item['quantity'])
            item['price'] = data.get('price', item['price'])
            return jsonify({'message': 'Item updated'})
    return jsonify({'error': 'Item not found'}), 404

@app.route('/cart/<string:name>', methods=['DELETE'])
def delete_item(name):
    global cart
    cart = [item for item in cart if item['product_name'] != name]
    return jsonify({'message': 'Item removed'})

@app.route('/cart/total', methods=['GET'])
def get_total():
    total = sum(item['quantity'] * item['price'] for item in cart)
    return jsonify({'total_price': total})
