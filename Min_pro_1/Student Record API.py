from flask import Flask, request, jsonify

app = Flask(__name__)

students = {}
next_id = 1
VALID_GRADES = {'A', 'B', 'C', 'D'}

# Helper: Validate student data
def validate_student(data):
    if 'name' not in data or 'roll' not in data or 'grade' not in data:
        return "Missing fields: name, roll, or grade", False
    if data['grade'] not in VALID_GRADES:
        return "Grade must be one of A, B, C, or D", False
    return "", True

# ➕ Add Student
@app.route("/students", methods=["POST"])
def add_student():
    global next_id
    data = request.get_json()
    msg, valid = validate_student(data)
    if not valid:
        return jsonify({"error": msg}), 400
    student = {
        "id": next_id,
        "name": data["name"],
        "roll": data["roll"],
        "grade": data["grade"]
    }
    students[next_id] = student
    next_id += 1
    return jsonify({"message": "Student added", "student": student}), 201

# 📋 View All Students
@app.route("/students", methods=["GET"])
def get_all_students():
    return jsonify(list(students.values()))

# 🔄 Update Student
@app.route("/students/<int:student_id>", methods=["PUT"])
def update_student(student_id):
    if student_id not in students:
        return jsonify({"error": "Student not found"}), 404
    data = request.get_json()
    msg, valid = validate_student(data)
    if not valid:
        return jsonify({"error": msg}), 400
    students[student_id].update({
        "name": data["name"],
        "roll": data["roll"],
        "grade": data["grade"]
    })
    return jsonify({"message": "Student updated", "student": students[student_id]})

# ❌ Delete Student
@app.route("/students/<int:student_id>", methods=["DELETE"])
def delete_student(student_id):
    if student_id not in students:
        return jsonify({"error": "Student not found"}), 404
    deleted = students.pop(student_id)
    return jsonify({"message": "Student deleted", "student": deleted})

# 🔍 Get Single Student (Optional)
@app.route("/students/<int:student_id>", methods=["GET"])
def get_student(student_id):
    if student_id not in students:
        return jsonify({"error": "Student not found"}), 404
    return jsonify(students[student_id])

if __name__ == "__main__":
    app.run(debug=True)
