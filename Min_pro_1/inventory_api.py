from flask import Flask, request, jsonify

app = Flask(__name__)

inventory = []
next_id = 1

@app.route('/items', methods=['GET'])
def get_items():
    return jsonify(inventory)

@app.route('/items', methods=['POST'])
def add_item():
    global next_id
    data = request.get_json()

    if not data.get('item_name') or not isinstance(data.get('quantity'), int) or not data.get('category'):
        return jsonify({'error': 'item_name, quantity (int), and category are required'}), 400

    item = {
        'id': next_id,
        'item_name': data['item_name'],
        'quantity': data['quantity'],
        'category': data['category']
    }
    inventory.append(item)
    next_id += 1
    return jsonify(item), 201

@app.route('/items/<int:item_id>', methods=['PUT'])
def update_item(item_id):
    data = request.get_json()
    for item in inventory:
        if item['id'] == item_id:
            if 'quantity' in data:
                try:
                    qty = int(data['quantity'])
                    item['quantity'] = qty
                except ValueError:
                    return jsonify({'error': 'Quantity must be an integer'}), 400
            if 'item_name' in data:
                item['item_name'] = data['item_name']
            if 'category' in data:
                item['category'] = data['category']

            response = {'message': 'Item updated', 'item': item}
            if item['quantity'] < 5:
                response['warning'] = 'Low stock warning: quantity is below threshold'
            return jsonify(response)
    return jsonify({'error': 'Item not found'}), 404

@app.route('/items/<int:item_id>', methods=['DELETE'])
def delete_item(item_id):
    for item in inventory:
        if item['id'] == item_id:
            inventory.remove(item)
            return jsonify({'message': f'Item {item_id} deleted'})
    return jsonify({'error': 'Item not found'}), 404

if __name__ == '__main__':
    app.run(debug=True)
