from flask import Flask, request, jsonify
from datetime import datetime

app = Flask(__name__)

events = []  # In-memory list to store event dictionaries
event_id_counter = 1

# Helper function to validate date format
def is_valid_date(date_str):
    try:
        datetime.strptime(date_str, '%Y-%m-%d')
        return True
    except ValueError:
        return False

@app.route("/events", methods=["POST"])
def add_event():
    global event_id_counter
    data = request.get_json()

    if not all(key in data for key in ("name", "date", "location")):
        return jsonify({"error": "Missing required fields"}), 400

    if not is_valid_date(data["date"]):
        return jsonify({"error": "Date must be in YYYY-MM-DD format"}), 400

    event = {
        "id": event_id_counter,
        "name": data["name"],
        "date": data["date"],
        "location": data["location"]
    }
    events.append(event)
    event_id_counter += 1
    return jsonify({"message": "Event added", "event": event}), 201

@app.route("/events", methods=["GET"])
def get_events():
    return jsonify(events)

@app.route("/events/<int:event_id>", methods=["GET"])
def get_event(event_id):
    for event in events:
        if event["id"] == event_id:
            return jsonify(event)
    return jsonify({"error": "Event not found"}), 404

@app.route("/events/<int:event_id>", methods=["PUT"])
def update_event(event_id):
    data = request.get_json()
    for event in events:
        if event["id"] == event_id:
            event["name"] = data.get("name", event["name"])
            event["date"] = data.get("date", event["date"])
            event["location"] = data.get("location", event["location"])

            if not is_valid_date(event["date"]):
                return jsonify({"error": "Date must be in YYYY-MM-DD format"}), 400

            return jsonify({"message": "Event updated", "event": event})
    return jsonify({"error": "Event not found"}), 404

@app.route("/events/<int:event_id>", methods=["DELETE"])
def delete_event(event_id):
    for event in events:
        if event["id"] == event_id:
            events.remove(event)
            return jsonify({"message": "Event deleted"})
    return jsonify({"error": "Event not found"}), 404

if __name__ == "__main__":
    app.run(debug=True)
