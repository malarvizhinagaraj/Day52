from flask import Flask, request, jsonify

app = Flask(__name__)

students = []
next_id = 1

def calculate_grade(avg):
    if avg >= 90:
        return 'A'
    elif avg >= 75:
        return 'B'
    elif avg >= 60:
        return 'C'
    else:
        return 'D'

@app.route('/students', methods=['GET'])
def get_students():
    return jsonify(students)

@app.route('/students', methods=['POST'])
def add_student():
    global next_id
    data = request.get_json()
    required = ['name', 'maths', 'science', 'english']

    if not all(k in data for k in required):
        return jsonify({'error': 'Missing fields'}), 400
    
    try:
        maths = float(data['maths'])
        science = float(data['science'])
        english = float(data['english'])

        if not all(0 <= m <= 100 for m in [maths, science, english]):
            raise ValueError
    except ValueError:
        return jsonify({'error': 'Marks must be numbers between 0 and 100'}), 400

    avg = round((maths + science + english) / 3, 2)
    grade = calculate_grade(avg)

    student = {
        'id': next_id,
        'name': data['name'],
        'maths': maths,
        'science': science,
        'english': english,
        'average': avg,
        'grade': grade
    }
    students.append(student)
    next_id += 1
    return jsonify(student), 201

@app.route('/students/<int:student_id>', methods=['PUT'])
def update_student(student_id):
    data = request.get_json()
    for student in students:
        if student['id'] == student_id:
            for subject in ['maths', 'science', 'english']:
                if subject in data:
                    try:
                        mark = float(data[subject])
                        if 0 <= mark <= 100:
                            student[subject] = mark
                        else:
                            return jsonify({'error': f'{subject} must be between 0 and 100'}), 400
                    except ValueError:
                        return jsonify({'error': f'{subject} must be a number'}), 400

            # Recalculate average & grade
            avg = round((student['maths'] + student['science'] + student['english']) / 3, 2)
            student['average'] = avg
            student['grade'] = calculate_grade(avg)
            return jsonify(student)
    return jsonify({'error': 'Student not found'}), 404

if __name__ == '__main__':
    app.run(debug=True)
