from flask import Flask, jsonify, request
from werkzeug.exceptions import HTTPException

app = Flask(__name__)
users = []
next_id = 1

@app.route('/api/users', methods=['GET'])
def get_users():
    return jsonify(users)

@app.route('/api/users', methods=['POST'])
def add_user():
    global next_id
    data = request.get_json()
    if not data or 'name' not in data or 'email' not in data:
        return jsonify(error="Name and email are required"), 400
    if any(u['email'] == data['email'] for u in users):
        return jsonify(error="Email already exists"), 400
    data['id'] = next_id
    next_id += 1
    users.append(data)
    return jsonify(success=True, user=data), 201

@app.route('/api/users/<int:user_id>', methods=['GET'])
def get_user(user_id):
    user = next((u for u in users if u['id'] == user_id), None)
    if user:
        return jsonify(user)
    return jsonify(error="User not found"), 404

@app.route('/api/users/<int:user_id>', methods=['PUT'])
def update_user(user_id):
    data = request.get_json()
    user = next((u for u in users if u['id'] == user_id), None)
    if not user:
        return jsonify(error="User not found"), 404
    if 'email' in data and any(u['email'] == data['email'] and u['id'] != user_id for u in users):
        return jsonify(error="Email already exists"), 400
    user.update(data)
    return jsonify(success=True, user=user)

@app.route('/api/users/<int:user_id>', methods=['DELETE'])
def delete_user(user_id):
    global users
    new_users = [u for u in users if u['id'] != user_id]
    if len(new_users) == len(users):
        return jsonify(error="User not found"), 404
    users = new_users
    return jsonify(success=True)

@app.route('/api/users/clear', methods=['DELETE'])
def clear_users():
    global users
    users = []
    return jsonify(message="All users cleared")

if __name__ == '__main__':
    app.run(debug=True)
