from flask import Flask, request, jsonify
from flask_cors import CORS
from database import students, admissions, courses, exams, grades, staff, departments
from pymongo.errors import DuplicateKeyError, PyMongoError
import logging

app = Flask(__name__)
CORS(app)
logging.basicConfig(level=logging.DEBUG)

# Generic CRUD functions
def create_crud_routes(entity, collection, id_field):
    """Generate CRUD endpoints dynamically for each entity."""

    @app.route(f'/{entity}', methods=['GET'], endpoint=f'get_{entity}')
    def get_entities():
        """Retrieve all records from a collection."""
        try:
            data = list(collection.find({}, {"_id": 0}))  # Exclude MongoDB _id field
            return jsonify(data), 200
        except PyMongoError as e:
            return jsonify({"error": str(e)}), 500

    @app.route(f'/{entity}/<string:id_value>', methods=['GET'], endpoint=f'get_single_{entity}')
    def get_entity(id_value):
        """Retrieve a specific record by ID."""
        try:
            record = collection.find_one({id_field: id_value}, {"_id": 0})
            if record:
                return jsonify(record), 200
            return jsonify({"error": f"{entity.capitalize()} not found!"}), 404
        except PyMongoError as e:
            return jsonify({"error": str(e)}), 500

    @app.route(f'/{entity}', methods=['POST'], endpoint=f'add_{entity}')
    def add_entity():
        """Insert a new record into a collection."""
        try:
            data = request.json
            if id_field not in data:
                return jsonify({"error": f"{id_field.replace('_', ' ').title()} is required!"}), 400
            collection.insert_one(data)
            return jsonify({"message": f"{entity.capitalize()} added successfully!"}), 201
        except DuplicateKeyError:
            return jsonify({"error": f"{id_field.replace('_', ' ').title()} already exists!"}), 400
        except PyMongoError as e:
            return jsonify({"error": str(e)}), 500

    @app.route(f'/{entity}/<string:id_value>', methods=['PUT'], endpoint=f'update_{entity}')
    def update_entity(id_value):
        """Update a record based on its ID."""
        try:
            data = request.json
            result = collection.update_one({id_field: id_value}, {"$set": data})
            if result.matched_count == 0:
                return jsonify({"error": f"{entity.capitalize()} not found!"}), 404
            return jsonify({"message": f"{entity.capitalize()} updated successfully!"}), 200
        except PyMongoError as e:
            return jsonify({"error": str(e)}), 500

    @app.route(f'/{entity}/<string:id_value>', methods=['DELETE'], endpoint=f'delete_{entity}')
    def delete_entity(id_value):
        """Delete a record from a collection."""
        try:
            result = collection.delete_one({id_field: id_value})
            if result.deleted_count == 0:
                return jsonify({"error": f"{entity.capitalize()} not found!"}), 404
            return jsonify({"message": f"{entity.capitalize()} deleted successfully!"}), 200
        except PyMongoError as e:
            return jsonify({"error": str(e)}), 500

# Generate API routes for each entity
entities_config = {
    "students": (students, "student_id"),
    "admissions": (admissions, "admission_id"),
    "courses": (courses, "course_id"),
    "departments": (departments, "department_id"),
    "staff": (staff, "staff_id"),
    "exams": (exams, "exam_id"),
    "grades": (grades, "grade_id")
    
}

for entity, (collection, id_field) in entities_config.items():
    create_crud_routes(entity, collection, id_field)

# Special Routes
@app.route('/students/search', methods=['GET'])
def search_students():
    """Search students by name or ID."""
    try:
        query = request.args.get("query", "").strip()
        if not query:
            return jsonify({"error": "Query parameter is required!"}), 400

        students_list = list(students.find(
            {"$or": [
                {"student_id": query},
                {"first_name": {"$regex": query, "$options": "i"}},
                {"last_name": {"$regex": query, "$options": "i"}}
            ]},
            {"_id": 0}
        ))

        return jsonify(students_list), 200
    except PyMongoError as e:
        return jsonify({"error": str(e)}), 500

@app.route('/courses/<string:course_id>/students', methods=['GET'])
def get_students_in_course(course_id):
    """Retrieve all students enrolled in a specific course."""
    try:
        enrolled_students = list(admissions.find({"course_id": course_id}, {"_id": 0, "student_id": 1}))
        student_ids = [s["student_id"] for s in enrolled_students]

        student_records = list(students.find({"student_id": {"$in": student_ids}}, {"_id": 0}))
        return jsonify(student_records), 200
    except PyMongoError as e:
        return jsonify({"error": str(e)}), 500

@app.route('/departments/<string:department_id>/courses', methods=['GET'])
def get_courses_under_department(department_id):
    """Retrieve all courses under a specific department."""
    try:
        courses_list = list(courses.find({"department_id": department_id}, {"_id": 0}))
        return jsonify(courses_list), 200
    except PyMongoError as e:
        return jsonify({"error": str(e)}), 500

@app.route('/departments/<string:department_id>/staff', methods=['GET'])
def get_staff_in_department(department_id):
    """Retrieve all staff members under a specific department."""
    try:
        staff_list = list(staff.find({"department_id": department_id}, {"_id": 0}))
        return jsonify(staff_list), 200
    except PyMongoError as e:
        return jsonify({"error": str(e)}), 500

@app.route('/grades/<string:course_id>', methods=['GET'])
def get_students_and_grades(course_id):
    """Retrieve all students and their grades for a specific course."""
    try:
        grade_records = list(grades.find({"course_id": course_id}, {"_id": 0}))
        return jsonify(grade_records), 200
    except PyMongoError as e:
        return jsonify({"error": str(e)}), 500

@app.route('/')
def index():
    """API Home Route"""
    return jsonify({"message": "Welcome to Student Management System API!"}), 200

if __name__ == "__main__":
    app.run(debug=True)
