from university import University

class FileManager:
    def save_data(university, file_path):
        data = {
        "faculties": [{
            "name": faculty.name,
            "field": faculty.field,
            "students": [{
                "student_id": student.student_id,
                "name": student.name,
                "email": student.email,
                "graduated": student.graduated
            } for student in faculty.students]
        } for faculty in university.faculties],
        "students": [{
            "student_id": student.student_id,
            "name": student.name,
            "email": student.email,
            "graduated": student.graduated
        } for student in university.students]
    }

        with open(file_path, 'w') as file:
            for faculty_data in data["faculties"]:
                file.write(f"{faculty_data['name']}|{faculty_data['field']}\n")
                for student_data in faculty_data["students"]:
                    file.write(f"{student_data['student_id']}|{student_data['name']}|{student_data['email']}|{student_data['graduated']}\n")

            for student_data in data["students"]:
                file.write(f"{student_data['student_id']}|{student_data['name']}|{student_data['email']}|{student_data['graduated']}\n")

    def load_data(file_path):
        try:
            with open(file_path, 'r') as file:
                lines = file.readlines()

            university = University()
            faculty = None

            for line in lines:
                parts = line.strip().split('|')

                if len(parts) == 2:  
                    faculty = university.create_faculty(parts[0], parts[1])
                elif len(parts) == 4:  
                    student = university.create_student(parts[0], parts[1], parts[2])
                    student.graduated = parts[3] == 'True'
                    if faculty:
                        university.assign_student_to_faculty(student, faculty)

            return university

        except FileNotFoundError:
            print(f"File not found: {file_path}")
            return None

