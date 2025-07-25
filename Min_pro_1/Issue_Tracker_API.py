from flask import Flask, request, jsonify

app = Flask(__name__)
issues = []
issue_id = 1

@app.route('/issues', methods=['POST'])
def create_issue():
    global issue_id
    data = request.get_json()
    title = data.get('title')
    desc = data.get('description')
    status = data.get('status', 'open')
    if not title or not desc or status not in ['open', 'closed']:
        return jsonify({'error': 'Missing or invalid fields'}), 400
    issues.append({'id': issue_id, 'title': title, 'description': desc, 'status': status})
    issue_id += 1
    return jsonify({'message': 'Issue created'}), 201

@app.route('/issues', methods=['GET'])
def get_issues():
    return jsonify(issues)

@app.route('/issues/<int:id>', methods=['PUT'])
def update_issue(id):
    data = request.get_json()
    for issue in issues:
        if issue['id'] == id:
            new_status = data.get('status')
            if new_status not in ['open', 'closed']:
                return jsonify({'error': 'Invalid status'}), 400
            issue['status'] = new_status
            return jsonify({'message': 'Status updated'})
    return jsonify({'error': 'Issue not found'}), 404

@app.route('/issues/<int:id>', methods=['DELETE'])
def delete_issue(id):
    global issues
    if any(issue['id'] == id for issue in issues):
        issues = [i for i in issues if i['id'] != id]
        return jsonify({'message': 'Issue deleted'})
    return jsonify({'error': 'Issue not found'}), 404
