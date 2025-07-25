from flask import Flask, request, jsonify
import re

app = Flask(__name__)

subscribers = set()

# Simple email regex
def is_valid_email(email):
    pattern = r'^[\w\.-]+@[\w\.-]+\.\w+$'
    return re.match(pattern, email)

@app.route('/subscribe', methods=['POST'])
def subscribe():
    data = request.get_json()
    email = data.get('email')

    if not email or not is_valid_email(email):
        return jsonify({'error': 'Invalid email format'}), 400

    if email in subscribers:
        return jsonify({'message': 'Email already subscribed'}), 200

    subscribers.add(email)
    return jsonify({'message': f'{email} subscribed successfully'}), 201

@app.route('/subscribe/<email>', methods=['DELETE'])
def unsubscribe(email):
    if not is_valid_email(email):
        return jsonify({'error': 'Invalid email format'}), 400

    if email in subscribers:
        subscribers.remove(email)
        return jsonify({'message': f'{email} unsubscribed successfully'}), 200
    else:
        return jsonify({'message': 'Email not found in subscription list'}), 404

if __name__ == '__main__':
    app.run(debug=True)
