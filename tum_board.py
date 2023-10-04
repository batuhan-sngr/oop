from university import University
from faculty import Faculty
from student import Student
from file_manager import FileManager

class AppLoop:

    file_path = "university.txt"

    def __init__(self):
        self.university = University()
        self.running = True

    def create_new_faculty(self):
        name = input("Enter faculty name: ")
        field = input("Enter faculty field: ")
        self.university.create_faculty(name, field)
        print("Faculty created successfully.")

    def create_and_assign_student(self):
        student_id = input("Enter student ID: ")
        name = input("Enter student name: ")
        email = input("Enter student email: ")

        faculty_name = input("Enter faculty name to assign to: ")
        faculty = next((f for f in self.university.faculties if f.name == faculty_name), None)

        if faculty:
            student = self.university.create_student(student_id, name, email)
            self.university.assign_student_to_faculty(student, faculty)
            print(f"Student {name} assigned to {faculty_name} successfully.")
        else:
            print(f"Faculty {faculty_name} not found.")

    def graduate_student(self):
        student_id = input("Enter student ID to graduate: ")
        student = next((s for s in self.university.students if s.student_id == student_id), None)

        if student:
            self.university.graduate_student(student)
            print(f"Student {student.name} graduated.")
        else:
            print(f"Student with ID {student_id} not found.")

    def display_enrolled_students(self):
        faculty_name = input("Enter faculty name: ")
        faculty = next((f for f in self.university.faculties if f.name == faculty_name), None)

        if faculty:
            self.university.display_enrolled_students(faculty)
        else:
            print(f"Faculty {faculty_name} not found.")

    def display_graduates(self):
        faculty_name = input("Enter faculty name: ")
        faculty = next((f for f in self.university.faculties if f.name == faculty_name), None)

        if faculty:
            self.university.display_graduates(faculty)
        else:
            print(f"Faculty {faculty_name} not found.")

    def tell_if_student_belongs(self):
        student_id = input("Enter student ID: ")
        faculty = self.university.find_faculty_by_student_identifier(student_id)

        if faculty:
            print(f"Yes, the student belongs to {faculty.name}.")
        else:
            print("No, the student does not belong to any faculty.")

    def search_faculty_by_student_identifier(self):
        identifier = input("Enter student ID or email: ")
        faculty = self.university.find_faculty_by_student_identifier(identifier)

        if faculty:
            print(f"Student with ID or email {identifier} belongs to {faculty.name} faculty.")
        else:
            print("Student not found.")

    def display_university_faculties(self):
        self.university.display_university_faculties()

    def display_faculties_by_field(self):
        field = input("Enter field name: ")
        self.university.display_faculties_by_field(field)

    def save_data(self):
        FileManager.save_data(self.university, self.file_path)
        print("Data saved.")

    def load_data(self):
        loaded_university = FileManager.load_data(self.file_path)

        if loaded_university:
            print("Data loaded.")
            self.university = loaded_university
        else:
            print("Failed to load data.")

    def exit_program(self):
        print("Exiting program. Goodbye!")
        self.running = False

    def run(self):
        while self.running:
            print("\n=== TUM Board ===")

            print("Main Menu:")
            print("1. Faculty Operations")
            print("2. Student Operations")
            print("3. General Operations")
            print("0. Exit")

            choice = input("Enter your choice: ")

            if choice == "0":
                print("Have a Good Day!")
                self.running = False
            elif choice == "1":
                self.faculty_menu()
            elif choice == "2":
                self.student_menu()
            elif choice == "3":
                self.general_menu()
            else:
                print("Invalid choice. Please enter a valid option.")

    def faculty_menu(self):
        while self.running:
            print("\n=== Faculty Operations ===")

            print("1. Create a new faculty")
            print("2. Display University faculties")
            print("3. Display faculties by field")
            print("0. Go back to the main menu")

            choice = input("Enter your choice: ")

            if choice == "0":
                print("Going back to the main menu.")
                break
            elif choice == "1":
                self.create_new_faculty()
            elif choice == "2":
                self.display_university_faculties()
            elif choice == "3":
                self.display_faculties_by_field()
            else:
                print("Invalid choice. Please enter a valid option.")

    def student_menu(self):
        while self.running:
            print("\n=== Student Operations ===")

            print("1. Create and assign a student to a faculty")
            print("2. Graduate a student from a faculty")
            print("3. Display current enrolled students in a faculty")
            print("4. Display graduates from a faculty")
            print("5. Tell if a student belongs to a faculty")
            print("6. Search what faculty a student belongs to by email or ID")
            print("0. Go back to the main menu")

            choice = input("Enter your choice: ")

            if choice == "0":
                print("Going back to the main menu.")
                break
            elif choice == "1":
                self.create_and_assign_student()
            elif choice == "2":
                self.graduate_student()
            elif choice == "3":
                self.display_enrolled_students()
            elif choice == "4":
                self.display_graduates()
            elif choice == "5":
                self.tell_if_student_belongs()
            elif choice == "6":
                self.search_faculty_by_student_identifier()
            else:
                print("Invalid choice. Please enter a valid option.")

    def general_menu(self):
        while self.running:
            print("\n=== General Operations ===")

            print("1. Save data")
            print("2. Load data")
            print("0. Go back to the main menu")

            choice = input("Enter your choice: ")

            if choice == "0":
                print("Going back to the main menu.")
                break
            elif choice == "1":
                self.save_data()
            elif choice == "2":
                self.load_data()
            else:
                print("Invalid choice. Please enter a valid option.")
if __name__ == "__main__":
    app = AppLoop()
    app.run()
