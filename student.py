"""
student.py - Student data model
Project  : Student Management System
Author   : Dipeeka Patidar
"""


class Student:
    def __init__(self, roll_no, name, age, course, marks):
        self.roll_no = int(roll_no)
        self.name = str(name)
        self.age = int(age)
        self.course = str(course)
        self.marks = float(marks)

    @property
    def grade(self):
        if self.marks >= 90:
            return "A+"
        if self.marks >= 80:
            return "A"
        if self.marks >= 70:
            return "B"
        if self.marks >= 60:
            return "C"
        if self.marks >= 40:
            return "D"
        return "F"

    @property
    def result(self):
        return "Pass" if self.marks >= 40 else "Fail"

    def to_dict(self):
        return {
            "roll_no": self.roll_no,
            "name": self.name,
            "age": self.age,
            "course": self.course,
            "marks": self.marks,
        }

    @staticmethod
    def from_dict(data):
        return Student(
            data["roll_no"], data["name"], data["age"],
            data["course"], data["marks"],
        )

    @staticmethod
    def table_header():
        line = "-" * 74
        head = f"{'Roll':<6}{'Name':<22}{'Age':<5}{'Course':<16}{'Marks':<8}{'Grade':<6}{'Result'}"
        return f"{line}\n{head}\n{line}"

    def table_row(self):
        return (f"{self.roll_no:<6}{self.name[:20]:<22}{self.age:<5}"
                f"{self.course[:14]:<16}{self.marks:<8.2f}{self.grade:<6}{self.result}")
