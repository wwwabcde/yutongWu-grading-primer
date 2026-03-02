from flask import Flask, jsonify, request
from flask_cors import CORS

import db

app = Flask(__name__)
CORS(app)

# ======================================================
# Students APIs
# ======================================================

@app.route("/students")
def get_students():
    """
    Route to fetch all students from the database
    return: Array of student objects
    """
    students = db.get_all_students()
    return jsonify(students), 200


@app.route("/students", methods=["POST"])
def create_student():
    """
    Route to create a new student
    """
    data = request.get_json(silent=True) or {}

    name = data.get("name")
    course = data.get("course")
    mark = data.get("mark")

    if not isinstance(name, str) or name.strip() == "":
        return jsonify({"error": "name must be a non-empty string"}), 400

    if not isinstance(course, str) or course.strip() == "":
        return jsonify({"error": "course must be a non-empty string"}), 400

    try:
        mark_int = int(mark)
    except (TypeError, ValueError):
        return jsonify({"error": "mark must be an integer"}), 400

    if mark_int < 0 or mark_int > 100:
        return jsonify({"error": "mark must be between 0 and 100"}), 400

    created = db.insert_student(name.strip(), course.strip(), mark_int)
    return jsonify(created), 201


@app.route("/students/<int:student_id>", methods=["PUT"])
def update_student(student_id):
    """
    Route to update student details by id
    """
    data = request.get_json(silent=True) or {}

    name = data.get("name")
    course = data.get("course")
    mark = data.get("mark")

    if name is not None:
        if not isinstance(name, str) or name.strip() == "":
            return jsonify({"error": "name must be a non-empty string if provided"}), 400
        name = name.strip()

    if course is not None:
        if not isinstance(course, str) or course.strip() == "":
            return jsonify({"error": "course must be a non-empty string if provided"}), 400
        course = course.strip()

    mark_int = None
    if mark is not None:
        try:
            mark_int = int(mark)
        except (TypeError, ValueError):
            return jsonify({"error": "mark must be an integer if provided"}), 400
        if mark_int < 0 or mark_int > 100:
            return jsonify({"error": "mark must be between 0 and 100"}), 400

    updated = db.update_student(student_id, name=name, course=course, mark=mark_int)
    if updated is None:
        return jsonify({"error": "student not found"}), 404

    return jsonify(updated), 200


@app.route("/students/<int:student_id>", methods=["DELETE"])
def delete_student(student_id):
    """
    Route to delete student by id
    """
    deleted = db.delete_student(student_id)
    if deleted is None:
        return jsonify({"error": "student not found"}), 404
    return jsonify(deleted), 200


# ======================================================
# Stats API
# ======================================================

@app.route("/stats")
def get_stats():
    """
    Route to show the stats of all student marks
    """
    students = db.get_all_students()
    marks = [int(s["mark"]) for s in students]

    # Edge case: no students in DB
    if len(marks) == 0:
        return jsonify({"count": 0, "average": None, "min": None, "max": None}), 200

    return jsonify({
        "count": len(marks),
        "average": sum(marks) / len(marks),
        "min": min(marks),
        "max": max(marks),
    }), 200


@app.route("/")
def health():
    return {"status": "ok"}


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
