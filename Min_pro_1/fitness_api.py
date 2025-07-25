from flask import Flask, request, jsonify

app = Flask(__name__)

workouts = []
workout_id_counter = 1

# ✅ GET all workouts
@app.route('/workouts', methods=['GET'])
def get_workouts():
    return jsonify({'workouts': workouts}), 200

# ✅ POST new workout
@app.route('/workouts', methods=['POST'])
def add_workout():
    global workout_id_counter
    data = request.get_json()
    user = data.get('user')
    wtype = data.get('type')
    duration = data.get('duration')

    if not all([user, wtype, duration]):
        return jsonify({'error': 'All fields (user, type, duration) are required.'}), 400
    if not isinstance(duration, (int, float)) or duration <= 0:
        return jsonify({'error': 'Duration must be a number greater than 0.'}), 400

    workout = {
        'id': workout_id_counter,
        'user': user,
        'type': wtype,
        'duration': duration
    }
    workouts.append(workout)
    workout_id_counter += 1

    return jsonify({'message': 'Workout added.', 'workout': workout}), 201

# ✅ PUT update workout
@app.route('/workouts/<int:wid>', methods=['PUT'])
def update_workout(wid):
    data = request.get_json()
    for workout in workouts:
        if workout['id'] == wid:
            workout['user'] = data.get('user', workout['user'])
            workout['type'] = data.get('type', workout['type'])
            new_duration = data.get('duration', workout['duration'])

            if new_duration <= 0:
                return jsonify({'error': 'Duration must be > 0'}), 400
            workout['duration'] = new_duration

            return jsonify({'message': 'Workout updated', 'workout': workout}), 200
    return jsonify({'error': 'Workout not found'}), 404

# ✅ DELETE workout
@app.route('/workouts/<int:wid>', methods=['DELETE'])
def delete_workout(wid):
    for workout in workouts:
        if workout['id'] == wid:
            workouts.remove(workout)
            return jsonify({'message': 'Workout deleted'}), 200
    return jsonify({'error': 'Workout not found'}), 404

# ✅ Summary route
@app.route('/summary', methods=['GET'])
def workout_summary():
    total = sum(w['duration'] for w in workouts)
    return jsonify({'total_duration': total, 'count': len(workouts)}), 200

if __name__ == '__main__':
    app.run(debug=True)
