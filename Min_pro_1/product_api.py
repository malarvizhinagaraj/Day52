from flask import Flask, request, jsonify

app = Flask(__name__)
products = []
product_id_counter = 1

@app.route('/products', methods=['POST'])
def add_product():
    global product_id_counter
    data = request.get_json()
    name = data.get('name')
    price = data.get('price')
    in_stock = data.get('in_stock', True)

    if not name or price is None:
        return jsonify({'error': 'Name and price are required'}), 400
    if not isinstance(price, (int, float)) or price <= 0:
        return jsonify({'error': 'Price must be a number > 0'}), 400

    product = {'id': product_id_counter, 'name': name, 'price': price, 'in_stock': in_stock}
    products.append(product)
    product_id_counter += 1
    return jsonify({'message': 'Product added', 'product': product}), 201

@app.route('/products', methods=['GET'])
def get_products():
    return jsonify(products), 200

@app.route('/products/<int:pid>', methods=['PUT'])
def update_product(pid):
    data = request.get_json()
    for p in products:
        if p['id'] == pid:
            p['name'] = data.get('name', p['name'])
            if 'price' in data:
                if data['price'] <= 0:
                    return jsonify({'error': 'Price must be > 0'}), 400
                p['price'] = data['price']
            p['in_stock'] = data.get('in_stock', p['in_stock'])
            return jsonify({'message': 'Product updated', 'product': p}), 200
    return jsonify({'error': 'Product not found'}), 404

@app.route('/products/<int:pid>', methods=['DELETE'])
def delete_product(pid):
    for p in products:
        if p['id'] == pid:
            products.remove(p)
            return jsonify({'message': 'Product deleted'}), 200
    return jsonify({'error': 'Product not found'}), 404

if __name__ == '__main__':
    app.run(debug=True)
