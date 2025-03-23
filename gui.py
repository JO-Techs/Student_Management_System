import tkinter as tk
from tkinter import ttk, messagebox
import requests
import uuid

# Flask API Base URL
API_URL = "http://127.0.0.1:5000"

class StudentManagementGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Student Management System")
        self.root.geometry("800x600")

        self.create_widgets()

    def create_widgets(self):
        """Creates the main GUI layout with buttons and data display."""

        title_label = tk.Label(self.root, text="Student Management System", font=("Arial", 16, "bold"))
        title_label.pack(pady=10)

        # Tab Control
        self.tab_control = ttk.Notebook(self.root)

        self.student_tab = ttk.Frame(self.tab_control)
        self.admission_tab = ttk.Frame(self.tab_control)
        self.course_tab = ttk.Frame(self.tab_control)
        self.department_tab = ttk.Frame(self.tab_control)
        self.staff_tab = ttk.Frame(self.tab_control)
        self.exam_tab = ttk.Frame(self.tab_control)
        self.grade_tab = ttk.Frame(self.tab_control)


        self.tab_control.add(self.student_tab, text="Students")
        self.tab_control.add(self.admission_tab, text="Admissions")
        self.tab_control.add(self.course_tab, text="Courses")
        self.tab_control.add(self.department_tab, text="Departments")
        self.tab_control.add(self.staff_tab, text="Staff")
        self.tab_control.add(self.exam_tab, text="Exams")
        self.tab_control.add(self.grade_tab, text="Grades")

        self.tab_control.pack(expand=1, fill="both")

        # Initialize tab contents
        self.create_student_tab()
        self.create_admission_tab()
        self.create_course_tab()
        self.create_department_tab()
        self.create_staff_tab()
        self.create_exam_tab()
        self.create_grade_tab()

    def create_student_tab(self):
        """Create UI elements for student management."""
        ttk.Label(self.student_tab, text="Student Management", font=("Arial", 12, "bold")).grid(row=0, column=0, columnspan=2, pady=10)
        
        ttk.Label(self.student_tab, text="Student ID:").grid(row=1, column=0, padx=10, pady=5)
        self.student_id_entry = ttk.Entry(self.student_tab)
        self.student_id_entry.grid(row=1, column=1, padx=10, pady=5)

        ttk.Label(self.student_tab, text="First Name:").grid(row=2, column=0, padx=10, pady=5)
        self.first_name_entry = ttk.Entry(self.student_tab)
        self.first_name_entry.grid(row=2, column=1, padx=10, pady=5)

        ttk.Label(self.student_tab, text="Last Name:").grid(row=3, column=0, padx=10, pady=5)
        self.last_name_entry = ttk.Entry(self.student_tab)
        self.last_name_entry.grid(row=3, column=1, padx=10, pady=5)

        # Buttons
        self.add_student_btn = ttk.Button(self.student_tab, text="Add Student", command=self.add_student)
        self.add_student_btn.grid(row=4, column=0, columnspan=2, pady=5)

        self.update_student_btn = ttk.Button(self.student_tab, text="Update Student", command=self.update_student)
        self.update_student_btn.grid(row=5, column=0, columnspan=2, pady=5)

        self.delete_student_btn = ttk.Button(self.student_tab, text="Delete Student", command=self.delete_student)
        self.delete_student_btn.grid(row=6, column=0, columnspan=2, pady=5)  # <-- New Delete Button

        self.get_students_btn = ttk.Button(self.student_tab, text="List Students", command=self.get_students)
        self.get_students_btn.grid(row=7, column=0, columnspan=2, pady=5)

        self.get_students_btn = ttk.Button(self.student_tab, text="previous", command=self.get_students)
        self.get_students_btn.grid(row=8, column=0, columnspan=2, pady=5)

        self.get_students_btn = ttk.Button(self.student_tab, text="next", command=self.get_students)
        self.get_students_btn.grid(row=5, column=1, columnspan=2, pady=10)

        self.get_students_btn = ttk.Button(self.student_tab, text="previous", command=self.get_students)
        self.get_students_btn.grid(row=6, column=1, columnspan=2, pady=11)
        

        # Listbox to display students
        self.student_listbox = tk.Listbox(self.student_tab, width=80, height=10)
        self.student_listbox.grid(row=8, column=0, columnspan=2, padx=10, pady=5)
        ttk.Label(self.student_tab, text="Search Student:").grid(row=9, column=0, padx=10, pady=5)
        self.search_student_entry = ttk.Entry(self.student_tab)
        self.search_student_entry.grid(row=9, column=1, padx=10, pady=5)

        self.search_student_btn = ttk.Button(self.student_tab, text="Search", command=self.search_students)
        self.search_student_btn.grid(row=10, column=0, columnspan=2, pady=5)

        



    def add_student(self):
        """Adds a student using the Flask API."""
        student_data = {
            "student_id": self.student_id_entry.get(),
            "first_name": self.first_name_entry.get(),
            "last_name": self.last_name_entry.get(),
        }

        response = requests.post(f"{API_URL}/students", json=student_data)
        if response.status_code == 201:
            messagebox.showinfo("Success", "Student added successfully!")
            self.get_students()
        else:
            messagebox.showerror("Error", response.json().get("error", "Unknown error"))

    def get_students(self):
        """Fetches and displays the list of students."""
        response = requests.get(f"{API_URL}/students")
        if response.status_code == 200:
            self.student_listbox.delete(0, tk.END)
            for student in response.json():
                self.student_listbox.insert(tk.END, f"{student['student_id']} - {student['first_name']} {student['last_name']}")
        else:
            messagebox.showerror("Error", "Failed to fetch student list")
    def update_student(self):
        """Updates an existing student's details using the Flask API."""
        student_id = self.student_id_entry.get().strip()
        first_name = self.first_name_entry.get().strip()
        last_name = self.last_name_entry.get().strip()

        if not student_id:
            messagebox.showerror("Error", "Student ID is required for updating!")
            return

        update_data = {}
        if first_name:
            update_data["first_name"] = first_name
        if last_name:
            update_data["last_name"] = last_name

        if not update_data:
            messagebox.showerror("Error", "Enter at least one field to update!")
            return

        response = requests.put(f"{API_URL}/students/{student_id}", json=update_data)

        if response.status_code == 200:
            messagebox.showinfo("Success", "Student updated successfully!")
            self.get_students()  # Refresh the list
        else:
            messagebox.showerror("Error", response.json().get("error", "Update failed"))
    def delete_student(self):
        """Deletes a student using the Flask API."""
        student_id = self.student_id_entry.get().strip()

        # If Student ID is not entered, check for a selected student in the listbox
        if not student_id:
            selected_item = self.student_listbox.curselection()
            if not selected_item:
                messagebox.showerror("Error", "Select a student from the list or enter a Student ID to delete!")
                return
            student_text = self.student_listbox.get(selected_item)
            student_id = student_text.split(" - ")[0]  # Extract Student ID

        # Confirm deletion
        confirm = messagebox.askyesno("Confirm Delete", f"Are you sure you want to delete Student {student_id}?")
        if not confirm:
            return

        # Send DELETE request to Flask API
        response = requests.delete(f"{API_URL}/students/{student_id}")

        # Handle response
        if response.status_code == 200:
            messagebox.showinfo("Success", "Student deleted successfully!")
            self.get_students()  # Refresh list
        else:
            messagebox.showerror("Error", response.json().get("error", "Delete failed"))

    def search_students(self):
        """Search students by name or ID using the Flask API."""
        query = self.search_student_entry.get().strip()
        
        if not query:
            messagebox.showerror("Error", "Enter a name or ID to search!")
            return

        response = requests.get(f"{API_URL}/students/search?query={query}")
        
        if response.status_code == 200:
            self.student_listbox.delete(0, tk.END)
            students = response.json()
            if not students:
                messagebox.showinfo("Info", "No students found.")
            for student in students:
                self.student_listbox.insert(tk.END, f"{student['student_id']} - {student['first_name']} {student['last_name']}")
        else:
            messagebox.showerror("Error", response.json().get("error", "Search failed"))


    def create_admission_tab(self):
        """Create UI elements for admission management."""
        ttk.Label(self.admission_tab, text="Admission Management", font=("Arial", 12, "bold")).grid(row=0, column=0, columnspan=2, pady=10)
        ttk.Label(self.admission_tab, text="Student ID:").grid(row=1, column=0, padx=10, pady=5)
        self.admission_student_id_entry = ttk.Entry(self.admission_tab)
        self.admission_student_id_entry.grid(row=1, column=1, padx=10, pady=5)

        ttk.Label(self.admission_tab, text="Admission ID:").grid(row=2, column=0, padx=10, pady=5)
        self.admission_id_entry = ttk.Entry(self.admission_tab)
        self.admission_id_entry.grid(row=2, column=1, padx=10, pady=5)

        ttk.Label(self.admission_tab, text="Status:").grid(row=3, column=0, padx=10, pady=5)
        self.admission_status_entry = ttk.Entry(self.admission_tab)
        self.admission_status_entry.grid(row=3, column=1, padx=10, pady=5)

        self.add_admission_btn = ttk.Button(self.admission_tab, text="Add Admission", command=self.add_admission)
        self.add_admission_btn.grid(row=4, column=0, columnspan=2, pady=10)

        self.get_admissions_btn = ttk.Button(self.admission_tab, text="List Admissions", command=self.get_admissions)
        self.get_admissions_btn.grid(row=5, column=0, columnspan=2, pady=10)

        self.admission_listbox = tk.Listbox(self.admission_tab, width=80, height=10)
        self.admission_listbox.grid(row=6, column=0, columnspan=2, padx=10, pady=5)

        self.delete_admission_btn = ttk.Button(self.admission_tab, text="Delete Admission", command=self.delete_admission)
        self.delete_admission_btn.grid(row=7, column=0, columnspan=2, pady=10)

    def add_admission(self):
        """Adds an admission record using the Flask API."""
        admission_data = {
            "student_id": self.admission_student_id_entry.get(),
            "admission_id": self.admission_id_entry.get(),
            "status": self.admission_status_entry.get(),
        }

        response = requests.post(f"{API_URL}/admissions", json=admission_data)
        if response.status_code == 201:
            messagebox.showinfo("Success", "Admission added successfully!")
            self.get_admissions()
        else:
            messagebox.showerror("Error", response.json().get("error", "Unknown error"))

    def get_admissions(self):
        """Fetches and displays the list of admissions."""
        response = requests.get(f"{API_URL}/admissions")
        if response.status_code == 200:
            self.admission_listbox.delete(0, tk.END)
            for admission in response.json():
                self.admission_listbox.insert(
                    tk.END,
                    f"ID: {admission['admission_id']} | Student: {admission['student_id']} | Status: {admission['status']}"
                )
        else:
            messagebox.showerror("Error", "Failed to fetch admission list")

    def delete_admission(self):
        """Deletes an admission record based on Admission ID."""
        selected_item = self.admission_listbox.curselection()
        if not selected_item:
            messagebox.showerror("Error", "Select an admission record to delete")
            return

        admission_text = self.admission_listbox.get(selected_item)
        admission_id = admission_text.split("|")[0].strip().split(":")[1].strip()

        response = requests.delete(f"{API_URL}/admissions/{admission_id}")
        if response.status_code == 200:
            messagebox.showinfo("Success", "Admission deleted successfully!")
            self.get_admissions()
        else:
            messagebox.showerror("Error", response.json().get("error", "Unknown error"))

    def create_course_tab(self):
        """Create UI elements for course management."""
        ttk.Label(self.course_tab, text="Course ID:").grid(row=0, column=0, padx=10, pady=5)
        self.course_id_entry = ttk.Entry(self.course_tab)
        self.course_id_entry.grid(row=0, column=1, padx=10, pady=5)

        ttk.Label(self.course_tab, text="Course Name:").grid(row=1, column=0, padx=10, pady=5)
        self.course_name_entry = ttk.Entry(self.course_tab)
        self.course_name_entry.grid(row=1, column=1, padx=10, pady=5)

        ttk.Label(self.course_tab, text="Department:").grid(row=2, column=0, padx=10, pady=5)
        self.course_department_entry = ttk.Entry(self.course_tab)
        self.course_department_entry.grid(row=2, column=1, padx=10, pady=5)

        self.add_course_btn = ttk.Button(self.course_tab, text="Add Course", command=self.add_course)
        self.add_course_btn.grid(row=3, column=0, columnspan=2, pady=10)

        self.get_courses_btn = ttk.Button(self.course_tab, text="List Courses", command=self.get_courses)
        self.get_courses_btn.grid(row=4, column=0, columnspan=2, pady=10)

        self.course_listbox = tk.Listbox(self.course_tab, width=80, height=10)
        self.course_listbox.grid(row=5, column=0, columnspan=2, padx=10, pady=5)

        self.delete_course_btn = ttk.Button(self.course_tab, text="Delete Course", command=self.delete_course)
        self.delete_course_btn.grid(row=6, column=0, columnspan=2, pady=10)
        ttk.Label(self.course_tab, text="Course ID for Students:").grid(row=7, column=0, padx=10, pady=5)
        self.course_students_entry = ttk.Entry(self.course_tab)
        self.course_students_entry.grid(row=7, column=1, padx=10, pady=5)

        self.get_course_students_btn = ttk.Button(self.course_tab, text="Get Students", command=self.get_students_in_course)
        self.get_course_students_btn.grid(row=8, column=0, columnspan=2, pady=5)


    def add_course(self):
        """Adds a course using the Flask API."""
        course_data = {
            "course_id": self.course_id_entry.get(),
            "course_name": self.course_name_entry.get(),
            "department": self.course_department_entry.get(),
        }

        response = requests.post(f"{API_URL}/courses", json=course_data)
        if response.status_code == 201:
            messagebox.showinfo("Success", "Course added successfully!")
            self.get_courses()
        else:
            messagebox.showerror("Error", response.json().get("error", "Unknown error"))

    def get_courses(self):
        """Fetches and displays the list of courses."""
        response = requests.get(f"{API_URL}/courses")
        if response.status_code == 200:
            self.course_listbox.delete(0, tk.END)
            for course in response.json():
                self.course_listbox.insert(tk.END, f"{course['course_id']} - {course['course_name']} (Dept: {course['department']})")
        else:
            messagebox.showerror("Error", "Failed to fetch course list")

    def delete_course(self):
        """Deletes a course based on Course ID."""
        selected_item = self.course_listbox.curselection()
        if not selected_item:
            messagebox.showerror("Error", "Select a course to delete")
            return

        course_text = self.course_listbox.get(selected_item)
        course_id = course_text.split("-")[0].strip()

        response = requests.delete(f"{API_URL}/courses/{course_id}")
        if response.status_code == 200:
            messagebox.showinfo("Success", "Course deleted successfully!")
            self.get_courses()
        else:
            messagebox.showerror("Error", response.json().get("error", "Unknown error"))

    def get_students_in_course(self):
        """Fetch students enrolled in a specific course."""
        course_id = self.course_students_entry.get().strip()
        
        if not course_id:
            messagebox.showerror("Error", "Enter a Course ID!")
            return

        response = requests.get(f"{API_URL}/courses/{course_id}/students")
        
        if response.status_code == 200:
            self.student_listbox.delete(0, tk.END)
            students = response.json()
            if not students:
                messagebox.showinfo("Info", "No students found for this course.")
            for student in students:
                self.student_listbox.insert(tk.END, f"{student['student_id']} - {student['first_name']} {student['last_name']}")
        else:
            messagebox.showerror("Error", response.json().get("error", "Failed to fetch students"))


    def create_department_tab(self):
        """Create UI elements for department management."""
        ttk.Label(self.department_tab, text="Department ID:").grid(row=0, column=0, padx=10, pady=5)
        self.dept_id_entry = ttk.Entry(self.department_tab)
        self.dept_id_entry.grid(row=0, column=1, padx=10, pady=5)

        ttk.Label(self.department_tab, text="Department Name:").grid(row=1, column=0, padx=10, pady=5)
        self.dept_name_entry = ttk.Entry(self.department_tab)
        self.dept_name_entry.grid(row=1, column=1, padx=10, pady=5)

        self.add_dept_btn = ttk.Button(self.department_tab, text="Add Department", command=self.add_department)
        self.add_dept_btn.grid(row=2, column=0, columnspan=2, pady=10)

        self.get_dept_btn = ttk.Button(self.department_tab, text="List Departments", command=self.get_departments)
        self.get_dept_btn.grid(row=3, column=0, columnspan=2, pady=10)

        self.delete_dept_btn = ttk.Button(self.department_tab, text="Delete Department", command=self.delete_department)
        self.delete_dept_btn.grid(row=4, column=0, columnspan=2, pady=10)

        self.dept_listbox = tk.Listbox(self.department_tab, width=80, height=10)
        self.dept_listbox.grid(row=5, column=0, columnspan=2, padx=10, pady=5)
        ttk.Label(self.department_tab, text="Department ID for Courses:").grid(row=6, column=0, padx=10, pady=5)
        self.department_courses_entry = ttk.Entry(self.department_tab)
        self.department_courses_entry.grid(row=6, column=1, padx=10, pady=5)

        self.get_department_courses_btn = ttk.Button(self.department_tab, text="Get Courses", command=self.get_courses_under_department)
        self.get_department_courses_btn.grid(row=7, column=0, columnspan=2, pady=5)


    def add_department(self):
        """Adds a department using the Flask API."""
        dept_data = {
            "department_id": self.dept_id_entry.get(),
            "department_name": self.dept_name_entry.get(),
        }

        response = requests.post(f"{API_URL}/departments", json=dept_data)
        if response.status_code == 201:
            messagebox.showinfo("Success", "Department added successfully!")
            self.get_departments()
        else:
            messagebox.showerror("Error", response.json().get("error", "Unknown error"))

    def get_departments(self):
        """Fetches and displays the list of departments."""
        response = requests.get(f"{API_URL}/departments")
        if response.status_code == 200:
            self.dept_listbox.delete(0, tk.END)
            for dept in response.json():
                self.dept_listbox.insert(tk.END, f"{dept['department_id']} - {dept['department_name']}")
        else:
            messagebox.showerror("Error", "Failed to fetch department list")

    def delete_department(self):
        """Deletes a department based on Department ID."""
        selected_item = self.dept_listbox.curselection()
        if not selected_item:
            messagebox.showerror("Error", "Select a department to delete")
            return

        dept_text = self.dept_listbox.get(selected_item)
        dept_id = dept_text.split("-")[0].strip()

        response = requests.delete(f"{API_URL}/departments/{dept_id}")
        if response.status_code == 200:
            messagebox.showinfo("Success", "Department deleted successfully!")
            self.get_departments()
        else:
            messagebox.showerror("Error", response.json().get("error", "Unknown error"))

    def get_courses_under_department(self):
        """Fetch courses under a specific department."""
        department_id = self.department_courses_entry.get().strip()
        
        if not department_id:
            messagebox.showerror("Error", "Enter a Department ID!")
            return

        response = requests.get(f"{API_URL}/departments/{department_id}/courses")
        
        if response.status_code == 200:
            self.course_listbox.delete(0, tk.END)
            courses = response.json()
            if not courses:
                messagebox.showinfo("Info", "No courses found for this department.")
            for course in courses:
                self.course_listbox.insert(tk.END, f"{course['course_id']} - {course['course_name']}")
        else:
            messagebox.showerror("Error", response.json().get("error", "Failed to fetch courses"))


    def create_staff_tab(self):
        """Create UI elements for staff management."""
        ttk.Label(self.staff_tab, text="Staff ID:").grid(row=0, column=0, padx=10, pady=5)
        self.staff_id_entry = ttk.Entry(self.staff_tab)
        self.staff_id_entry.grid(row=0, column=1, padx=10, pady=5)

        ttk.Label(self.staff_tab, text="Name:").grid(row=1, column=0, padx=10, pady=5)
        self.staff_name_entry = ttk.Entry(self.staff_tab)
        self.staff_name_entry.grid(row=1, column=1, padx=10, pady=5)

        ttk.Label(self.staff_tab, text="Department:").grid(row=2, column=0, padx=10, pady=5)
        self.staff_department_entry = ttk.Entry(self.staff_tab)
        self.staff_department_entry.grid(row=2, column=1, padx=10, pady=5)

        self.add_staff_btn = ttk.Button(self.staff_tab, text="Add Staff", command=self.add_staff)
        self.add_staff_btn.grid(row=3, column=0, columnspan=2, pady=10)

        self.get_staff_btn = ttk.Button(self.staff_tab, text="List Staff", command=self.get_staff)
        self.get_staff_btn.grid(row=4, column=0, columnspan=2, pady=10)

        self.search_staff_btn = ttk.Button(self.staff_tab, text="Search Staff", command=self.search_staff)
        self.search_staff_btn.grid(row=5, column=0, columnspan=2, pady=10)

        self.delete_staff_btn = ttk.Button(self.staff_tab, text="Delete Staff", command=self.delete_staff)
        self.delete_staff_btn.grid(row=6, column=0, columnspan=2, pady=10)

        # Department Staff Lookup
        ttk.Label(self.staff_tab, text="Department ID for Staff:").grid(row=7, column=0, padx=10, pady=5)
        self.department_staff_entry = ttk.Entry(self.staff_tab)
        self.department_staff_entry.grid(row=7, column=1, padx=10, pady=5)

        self.get_department_staff_btn = ttk.Button(self.staff_tab, text="Get Staff", command=self.get_staff_in_department)
        self.get_department_staff_btn.grid(row=8, column=0, columnspan=2, pady=5)

        # Shift listbox down to row 9
        self.staff_listbox = tk.Listbox(self.staff_tab, width=80, height=10)
        self.staff_listbox.grid(row=9, column=0, columnspan=2, padx=10, pady=5)

    def add_staff(self):
        """Adds a staff member using the Flask API."""
        staff_data = {
            "staff_id": self.staff_id_entry.get(),
            "name": self.staff_name_entry.get(),
            "department": self.staff_department_entry.get(),
        }

        response = requests.post(f"{API_URL}/staff", json=staff_data)
        if response.status_code == 201:
            messagebox.showinfo("Success", "Staff added successfully!")
            self.get_staff()
        else:
            messagebox.showerror("Error", response.json().get("error", "Unknown error"))

    def get_staff(self):
        """Fetches and displays the list of staff members."""
        response = requests.get(f"{API_URL}/staff")
        if response.status_code == 200:
            self.staff_listbox.delete(0, tk.END)
            for staff in response.json():
                self.staff_listbox.insert(tk.END, f"{staff['staff_id']} - {staff['name']} (Dept: {staff['department']})")
        else:
            messagebox.showerror("Error", "Failed to fetch staff list")

    def search_staff(self):
        """Searches for staff by name or ID."""
        search_query = self.staff_id_entry.get()
        if not search_query:
            search_query = self.staff_name_entry.get()

        if not search_query:
            messagebox.showerror("Error", "Enter Staff ID or Name to search")
            return

        response = requests.get(f"{API_URL}/staff/search/{search_query}")
        if response.status_code == 200:
            self.staff_listbox.delete(0, tk.END)
            for staff in response.json():
                self.staff_listbox.insert(tk.END, f"{staff['staff_id']} - {staff['name']} (Dept: {staff['department']})")
        else:
            messagebox.showerror("Error", "No staff found")

    def delete_staff(self):
        """Deletes a staff member based on Staff ID."""
        selected_item = self.staff_listbox.curselection()
        if not selected_item:
            messagebox.showerror("Error", "Select a staff member to delete")
            return

        staff_text = self.staff_listbox.get(selected_item)
        staff_id = staff_text.split("-")[0].strip()

        response = requests.delete(f"{API_URL}/staff/{staff_id}")
        if response.status_code == 200:
            messagebox.showinfo("Success", "Staff deleted successfully!")
            self.get_staff()
        else:
            messagebox.showerror("Error", response.json().get("error", "Unknown error"))

    def get_staff_in_department(self):
        """Fetch staff members under a specific department."""
        department_id = self.department_staff_entry.get().strip()
        
        if not department_id:
            messagebox.showerror("Error", "Enter a Department ID!")
            return

        response = requests.get(f"{API_URL}/departments/{department_id}/staff")
        
        if response.status_code == 200:
            self.staff_listbox.delete(0, tk.END)
            staff_list = response.json()
            if not staff_list:
                messagebox.showinfo("Info", "No staff members found in this department.")
            for staff in staff_list:
                self.staff_listbox.insert(tk.END, f"{staff['staff_id']} - {staff['name']}")
        else:
            messagebox.showerror("Error", response.json().get("error", "Failed to fetch staff"))

    def create_exam_tab(self):
        ttk.Label(self.exam_tab, text="Exam Management", font=("Arial", 12, "bold")).grid(row=0, column=0, columnspan=2, pady=10)

        ttk.Label(self.exam_tab, text="Exam ID:").grid(row=1, column=0)
        self.exam_id_entry = ttk.Entry(self.exam_tab)
        self.exam_id_entry.grid(row=1, column=1)

        ttk.Label(self.exam_tab, text="Course ID:").grid(row=2, column=0)
        self.course_id_entry = ttk.Entry(self.exam_tab)
        self.course_id_entry.grid(row=2, column=1)

        ttk.Label(self.exam_tab, text="Exam Date (YYYY-MM-DD):").grid(row=3, column=0)
        self.exam_date_entry = ttk.Entry(self.exam_tab)
        self.exam_date_entry.grid(row=3, column=1)

        ttk.Button(self.exam_tab, text="Schedule Exam", command=self.add_exam).grid(row=4, column=0, pady=5)
        ttk.Button(self.exam_tab, text="List Exams", command=self.get_exams).grid(row=4, column=1, pady=5)
        ttk.Button(self.exam_tab, text="Search exam", command=self.add_exam).grid(row=5, column=2, pady=5)

        self.exam_listbox = tk.Listbox(self.exam_tab, width=80, height=10)
        self.exam_listbox.grid(row=5, column=0, columnspan=2, padx=10, pady=5)

    def create_grade_tab(self):
        ttk.Label(self.grade_tab, text="Grade Management", font=("Arial", 12, "bold")).grid(row=0, column=0, columnspan=2, pady=10)

        ttk.Label(self.grade_tab, text="Grade ID:").grid(row=1, column=0)
        self.grade_id_entry = ttk.Entry(self.grade_tab)
        self.grade_id_entry.grid(row=1, column=1)

        ttk.Label(self.grade_tab, text="Student ID:").grid(row=2, column=0)
        self.grade_student_id_entry = ttk.Entry(self.grade_tab)
        self.grade_student_id_entry.grid(row=2, column=1)

        ttk.Label(self.grade_tab, text="Exam ID:").grid(row=3, column=0)
        self.grade_exam_id_entry = ttk.Entry(self.grade_tab)
        self.grade_exam_id_entry.grid(row=3, column=1)

        ttk.Label(self.grade_tab, text="Grade:").grid(row=4, column=0)
        self.grade_entry = ttk.Entry(self.grade_tab)
        self.grade_entry.grid(row=4, column=1)

        ttk.Button(self.grade_tab, text="Assign Grade", command=self.add_grade).grid(row=5, column=0, pady=5)
        ttk.Button(self.grade_tab, text="List Grades", command=self.get_grades).grid(row=5, column=1, pady=5)

        self.grade_listbox = tk.Listbox(self.grade_tab, width=80, height=10)
        self.grade_listbox.grid(row=6, column=0, columnspan=2, padx=10, pady=5)


    def add_exam(self):
        exam_data = {
            "exam_id": self.exam_id_entry.get(),
            "course_id": self.course_id_entry.get(),
            "exam_date": self.exam_date_entry.get(),
        }
        response = requests.post(f"{API_URL}/exams", json=exam_data)
        if response.status_code == 201:
            messagebox.showinfo("Success", "Exam scheduled successfully!")
            self.get_exams()
        else:
            messagebox.showerror("Error", response.json().get("error", "Unknown error"))

    def get_exams(self):
        response = requests.get(f"{API_URL}/exams")
        if response.status_code == 200:
            self.exam_listbox.delete(0, tk.END)
            for exam in response.json():
                self.exam_listbox.insert(tk.END, f"Exam {exam['exam_id']} - Course {exam['course_id']} - {exam['exam_date']}")
        else:
            messagebox.showerror("Error", "Failed to fetch exam list")

    def add_grade(self):
        grade_data = {
            "grade_id": self.grade_id_entry.get(),  # Include Grade ID
            "student_id": self.grade_student_id_entry.get(),
            "exam_id": self.grade_exam_id_entry.get(),
            "grade": self.grade_entry.get(),
        }
        
        response = requests.post(f"{API_URL}/grades", json=grade_data)
        if response.status_code == 201:
            messagebox.showinfo("Success", "Grade assigned successfully!")
            self.get_grades()
        else:
            messagebox.showerror("Error", response.json().get("error", "Unknown error"))

    def get_grades(self):
        response = requests.get(f"{API_URL}/grades")
        if response.status_code == 200:
            self.grade_listbox.delete(0, tk.END)
            for grade in response.json():
                self.grade_listbox.insert(
                    tk.END, 
                    f"Grade ID: {grade['grade_id']} - Student {grade['student_id']} - Exam {grade['exam_id']} - Grade {grade['grade']}"
                )
        else:
            messagebox.showerror("Error", "Failed to fetch grade list")


if __name__ == "__main__":
    root = tk.Tk()
    app = StudentManagementGUI(root)
    root.mainloop()
