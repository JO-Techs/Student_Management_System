import logging
from pymongo import MongoClient, ASCENDING
from pymongo.errors import PyMongoError, ServerSelectionTimeoutError

logging.basicConfig(level=logging.INFO)

def connect_to_mongo():
    """Connect to MongoDB and initialize all collections with indexes"""
    try:
        client = MongoClient('mongodb://localhost:27017/', serverSelectionTimeoutMS=5000)
        db = client['student_management']
        logging.info("✅ Connected to MongoDB successfully!")

        # Define collections
        collections = {
            "students": db.students,
            "admissions": db.admissions,
            "courses": db.courses,
            "departments": db.departments,
            "staff": db.staff,
            "exams": db.exams,
            "grades": db.grades
        }


        # Create unique indexes for ID fields
        collections["students"].create_index([("student_id", ASCENDING)], unique=True)
        collections["admissions"].create_index([("admission_id", ASCENDING)], unique=True)
        collections["courses"].create_index([("course_id", ASCENDING)], unique=True)
        collections["departments"].create_index([("department_id", ASCENDING)], unique=True)
        collections["staff"].create_index([("staff_id", ASCENDING)], unique=True)
        collections["exams"].create_index([("exam_id", ASCENDING)], unique=True)
        collections["grades"].create_index([("grade_id", ASCENDING)], unique=True)



        logging.info("✅ Indexes created successfully!")
        return collections

    except ServerSelectionTimeoutError:
        logging.error("❌ MongoDB connection timeout")
        raise
    except PyMongoError as e:
        logging.error(f"❌ MongoDB error: {e}")
        raise

# Initialize collections
collections = connect_to_mongo()

# Assign collections to variables for easy import
students = collections["students"]
admissions = collections["admissions"]
courses = collections["courses"]
departments = collections["departments"]
staff = collections["staff"]
exams = collections["exams"]
grades = collections["grades"]
