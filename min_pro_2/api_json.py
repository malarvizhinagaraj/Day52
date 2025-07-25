from flask import Flask, request, jsonify
import json

app = Flask(__name__)

@app.route('/echo', methods=['POST'])
def echo():
    data = request.get_json()
    return jsonify(received=data)

@app.route('/multiply', methods=['POST'])
def multiply():
    data = request.get_json()
    if not data or 'a' not in data or 'b' not in data:
        return jsonify(error="Missing numbers"), 400
    if not isinstance(data['a'], int) or not isinstance(data['b'], int):
        return jsonify(error="Both must be integers"), 400
    return jsonify(result=data['a'] * data['b'])

@app.route('/profile', methods=['POST'])
def profile():
    data = request.get_json()
    try:
        bio = data['user']['profile']['bio']
        return jsonify(bio=bio)
    except Exception:
        return jsonify(error="Invalid structure"), 400

if __name__ == '__main__':
    app.run(debug=True)
    