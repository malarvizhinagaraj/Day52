from flask import Flask, jsonify, request

app = Flask(__name__)

# In-memory storage
tasks = []
next_id = 1

# GET all tasks
@app.route('/tasks', methods=['GET'])
def get_tasks():
    return jsonify(tasks)

# POST a new task
@app.route('/tasks', methods=['POST'])
def create_task():
    global next_id
    data = request.get_json()

    if not data or 'title' not in data:
        return jsonify({'error': 'Task title is required'}), 400

    new_task = {
        'id': next_id,
        'title': data['title'],
        'status': 'pending'
    }
    tasks.append(new_task)
    next_id += 1
    return jsonify(new_task), 201

# PUT to update a task (toggle or update)
@app.route('/tasks/<int:task_id>', methods=['PUT'])
def update_task(task_id):
    data = request.get_json()
    for task in tasks:
        if task['id'] == task_id:
            if 'title' in data:
                task['title'] = data['title']
            if 'status' in data:
                if data['status'] in ['pending', 'done']:
                    task['status'] = data['status']
            else:
                # Toggle status
                task['status'] = 'done' if task['status'] == 'pending' else 'pending'
            return jsonify(task)
    return jsonify({'error': 'Task not found'}), 404

# DELETE a task
@app.route('/tasks/<int:task_id>', methods=['DELETE'])
def delete_task(task_id):
    for task in tasks:
        if task['id'] == task_id:
            tasks.remove(task)
            return jsonify({'message': f'Task {task_id} deleted'})
    return jsonify({'error': 'Task not found'}), 404

if __name__ == '__main__':
    app.run(debug=True)
