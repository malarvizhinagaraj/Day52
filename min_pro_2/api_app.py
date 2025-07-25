from flask import Flask, jsonify, request
from datetime import datetime

app = Flask(__name__)

# 3. Simple GET /hello
@app.route('/hello')
def hello():
    return jsonify(message="Welcome to the Flask REST API!")

# 5. /info route
@app.route('/info')
def info():
    return jsonify(app_name="Flask API Demo", version="1.0.0")

# 6. /status route for health check
@app.route('/status')
def status():
    uptime = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    return jsonify(status="Running", uptime=uptime)

# 8. Structured JSON via jsonify()
@app.route('/structured')
def structured():
    return jsonify(success=True, data={"feature": "JSON structure example"})

if __name__ == '__main__':
    app.run(debug=True)
