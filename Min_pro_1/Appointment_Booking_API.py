from flask import Flask, request, jsonify
from datetime import datetime

app = Flask(__name__)

appointments = []
appointment_id_counter = 1

# ✅ Validate date format helper
def is_valid_date(date_str):
    try:
        datetime.strptime(date_str, '%Y-%m-%d')
        return True
    except ValueError:
        return False

# 📌 GET all appointments
@app.route('/appointments', methods=['GET'])
def get_appointments():
    return jsonify({'appointments': appointments}), 200

# ✅ POST - Book new appointment
@app.route('/appointments', methods=['POST'])
def book_appointment():
    global appointment_id_counter
    data = request.get_json()

    name = data.get('name')
    date = data.get('date')
    service = data.get('service')

    # Validation
    if not all([name, date, service]):
        return jsonify({'error': 'Name, date, and service are required.'}), 400

    if not is_valid_date(date):
        return jsonify({'error': 'Date must be in YYYY-MM-DD format.'}), 400

    appointment = {
        'id': appointment_id_counter,
        'name': name,
        'date': date,
        'service': service
    }
    appointments.append(appointment)
    appointment_id_counter += 1

    return jsonify({'message': 'Appointment booked successfully!', 'appointment': appointment}), 201

# ✏️ PUT - Update appointment
@app.route('/appointments/<int:appointment_id>', methods=['PUT'])
def update_appointment(appointment_id):
    data = request.get_json()
    for appt in appointments:
        if appt['id'] == appointment_id:
            appt['name'] = data.get('name', appt['name'])
            appt['date'] = data.get('date', appt['date'])
            appt['service'] = data.get('service', appt['service'])

            if not is_valid_date(appt['date']):
                return jsonify({'error': 'Date must be in YYYY-MM-DD format.'}), 400

            return jsonify({'message': 'Appointment updated successfully.', 'appointment': appt}), 200

    return jsonify({'error': 'Appointment not found.'}), 404

# ❌ DELETE - Cancel appointment
@app.route('/appointments/<int:appointment_id>', methods=['DELETE'])
def delete_appointment(appointment_id):
    for appt in appointments:
        if appt['id'] == appointment_id:
            appointments.remove(appt)
            return jsonify({'message': f'Appointment with ID {appointment_id} canceled successfully.'}), 200

    return jsonify({'error': 'Appointment not found.'}), 404

# 🚀 Run app
if __name__ == '__main__':
    app.run(debug=True)
