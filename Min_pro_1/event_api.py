from flask import Flask, request, jsonify
from datetime import datetime

app = Flask(__name__)

events = []
next_id = 1

# Helper: validate date
def validate_date(date_str):
    try:
        datetime.strptime(date_str, '%Y-%m-%d')
        return True
    except ValueError:
        return False

# GET all events
@app.route('/events', methods=['GET'])
def get_events():
    return jsonify(events)

# POST a new event
@app.route('/events', methods=['POST'])
def add_event():
    global next_id
    data = request.get_json()
    if not data.get('name') or not data.get('date') or not data.get('location'):
        return jsonify({'error': 'Missing name, date or location'}), 400
    if not validate_date(data['date']):
        return jsonify({'error': 'Invalid date format. Use YYYY-MM-DD'}), 400
    event = {
        'id': next_id,
        'name': data['name'],
        'date': data['date'],
        'location': data['location']
    }
    events.append(event)
    next_id += 1
    return jsonify(event), 201

# PUT update event
@app.route('/events/<int:event_id>', methods=['PUT'])
def update_event(event_id):
    data = request.get_json()
    for event in events:
        if event['id'] == event_id:
            if 'name' in data:
                event['name'] = data['name']
            if 'date' in data:
                if not validate_date(data['date']):
                    return jsonify({'error': 'Invalid date format'}), 400
                event['date'] = data['date']
            if 'location' in data:
                event['location'] = data['location']
            return jsonify(event)
    return jsonify({'error': 'Event not found'}), 404

# DELETE an event
@app.route('/events/<int:event_id>', methods=['DELETE'])
def delete_event(event_id):
    for event in events:
        if event['id'] == event_id:
            events.remove(event)
            return jsonify({'message': f'Event {event_id} deleted'})
    return jsonify({'error': 'Event not found'}), 404

if __name__ == '__main__':
    app.run(debug=True)
