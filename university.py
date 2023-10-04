from faculty import Faculty
from student import Student

class University:
    def __init__(self):
        self.faculties = []
        self.students = []

    def create_faculty(self, name, field):
        faculty = Faculty(name, field)
        self.faculties.append(faculty)
        return faculty

    def create_student(self, student_id, name, email):
        student = Student(student_id, name, email)
        self.students.append(student)
        return student

    def assign_student_to_faculty(self, student, faculty):
        faculty.assign_student(student)

    def graduate_student(self, student):
        student.graduated = True

    def display_enrolled_students(self, faculty):
        enrolled_students = [student for student in faculty.students if not student.graduated]
        self.__display_students__(enrolled_students)

    def display_graduates(self, faculty):
        graduated_students = [student for student in faculty.students if student.graduated]
        self.__display_students__(graduated_students)

    def display_university_faculties(self):
        print("University Faculties:")
        for faculty in self.faculties:
            print(f"{faculty.name} - {faculty.field}")

    def display_faculties_by_field(self, field):
        faculties_by_field = [faculty for faculty in self.faculties if faculty.field == field]
        print(f"Faculties in {field} field:")
        for faculty in faculties_by_field:
            print(f"{faculty.name} - {faculty.field}")

    def find_faculty_by_student_identifier(self, identifier):
        for faculty in self.faculties:
            for student in faculty.students:
                if student.email == identifier or student.student_id == identifier:
                    return faculty
        return None

    def __display_students__(self, students):
        print("Students:")
        for student in students:
            print(f"{student.name} - {student.email}")
