class Faculty:
    def __init__(self, name, field):
        self.name = name
        self.field = field
        self.students = []

    def assign_student(self, student):
        self.students.append(student)

    def graduate_student(self, student):
        student.graduated = True

