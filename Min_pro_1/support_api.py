from flask import Flask, request, jsonify

app = Flask(__name__)

tickets = []
ticket_id_counter = 1

@app.route('/tickets', methods=['GET'])
def get_tickets():
    return jsonify({'tickets': tickets}), 200

@app.route('/tickets', methods=['POST'])
def submit_ticket():
    global ticket_id_counter
    data = request.get_json()
    email = data.get('email')
    issue = data.get('issue')
    priority = data.get('priority')

    if not all([email, issue, priority]):
        return jsonify({'error': 'All fields are required: email, issue, priority'}), 400

    ticket = {
        'id': ticket_id_counter,
        'email': email,
        'issue': issue,
        'priority': priority,
        'status': 'open'
    }
    tickets.append(ticket)
    ticket_id_counter += 1

    return jsonify({'message': 'Ticket submitted.', 'ticket': ticket}), 201

@app.route('/tickets/<int:ticket_id>', methods=['PUT'])
def resolve_ticket(ticket_id):
    for ticket in tickets:
        if ticket['id'] == ticket_id:
            ticket['status'] = 'closed'
            return jsonify({'message': 'Ticket closed', 'ticket': ticket}), 200

    return jsonify({'error': 'Ticket not found'}), 404

@app.route('/tickets/<int:ticket_id>', methods=['DELETE'])
def delete_ticket(ticket_id):
    for ticket in tickets:
        if ticket['id'] == ticket_id:
            tickets.remove(ticket)
            return jsonify({'message': 'Ticket deleted'}), 200

    return jsonify({'error': 'Ticket not found'}), 404

if __name__ == '__main__':
    app.run(debug=True)
