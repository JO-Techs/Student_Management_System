# Student_Management_System

Entities and Attributes:
Student

student_id (Primary Key)
first_name
last_name
date_of_birth
gender
contact
email
address
year
admission_date
course_id (Foreign Key)
Admission

admission_id (Primary Key)
student_id (Foreign Key)
course_id (Foreign Key)
admission_date
admission_status
Course

course_id (Primary Key)
course_name
duration
credit
department_id (Foreign Key)
Department

department_id (Primary Key)
department_name
head_of_department
contact
Staff

staff_id (Primary Key)
first_name
last_name
gender
address
email
contact
role
department_id (Foreign Key)
Exam

exam_id (Primary Key)
course_id (Foreign Key)
e_name
e_date
Grade

grade_id (Primary Key)
student_id (Foreign Key)
course_id (Foreign Key)
exam_id (Foreign Key)
grade
marks
Relationships:
Student - Admission → One-to-One (A student has one admission record).
Student - Course → Many-to-One (Many students can enroll in one course).
Course - Department → Many-to-One (Many courses belong to one department).
Course - Exam → One-to-Many (A course can have multiple exams).
Student - Exam - Grade → Many-to-Many (A student takes many exams and receives grades).
Department - Staff → One-to-Many (A department has multiple staff members).

1. Student Management
   Add a new student (Insert a new student record)
   Update student details (Modify student information)
   Delete a student (Remove a student record)
   View student details (Retrieve a student record)
   List all students (Display all students)
   Search student by name or ID
2. Admission Management
   Process student admission (Insert a new admission record)
   Update admission details (Modify admission status)
   View admission details (Retrieve admission records)
   List all admissions (Display all admissions)
   Delete admission record
3. Course Management
   Add a new course (Insert a new course)
   Update course details
   Delete a course
   View course details
   List all courses
   Get students enrolled in a specific course
4. Department Management
   Add a department
   Update department details
   Delete a department
   View department details
   List all departments
   List courses under a department
   List staff members under a department
5. Staff Management
   Add a new staff member
   Update staff details
   Delete a staff member
   View staff details
   List all staff members
   Search staff by name or ID
6. Exam & Grades Management
   Schedule a new exam
   Update exam details
   Delete an exam
   View exam details
   List all exams for a course
   Enter student grades
   Update student grades
   Delete a grade record
   View student grades
   Get all students and their grades for a specific course
