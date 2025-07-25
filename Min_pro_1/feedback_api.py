from flask import Flask, request, jsonify
import re

app = Flask(__name__)
feedback_list = []

def is_valid_email(email):
    return re.match(r'^[\w\.-]+@[\w\.-]+\.\w+$', email)

@app.route('/feedback', methods=['POST'])
def collect_feedback():
    data = request.get_json()
    name = data.get('name')
    email = data.get('email')
    message = data.get('message')

    if not all([name, email, message]):
        return jsonify({'error': 'All fields are required.'}), 400
    if not is_valid_email(email):
        return jsonify({'error': 'Invalid email format.'}), 400

    feedback = {'name': name, 'email': email, 'message': message}
    feedback_list.append(feedback)

    return jsonify({'message': f'Thank you for your feedback, {name}!'}), 200

if __name__ == '__main__':
    app.run(debug=True)
