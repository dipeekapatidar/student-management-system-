"""
manager.py - Core operations: add, update, delete, search, sort
Project  : Student Management System
Author   : Dipeeka Patidar
"""
import storage
from student import Student


class StudentManager:
    def __init__(self):
        self.students = storage.load_students()

    # ---------- helpers ----------
    def _save(self):
        return storage.save_students(self.students)

    def find_by_roll(self, roll_no):
        for s in self.students:
            if s.roll_no == roll_no:
                return s
        return None

    # ---------- CRUD ----------
    def add(self, roll_no, name, age, course, marks):
        if self.find_by_roll(roll_no):
            raise ValueError(f"Roll number {roll_no} already exists.")
        self.students.append(Student(roll_no, name, age, course, marks))
        self._save()

    def update(self, roll_no, name=None, age=None, course=None, marks=None):
        student = self.find_by_roll(roll_no)
        if not student:
            raise LookupError(f"No student found with roll number {roll_no}.")
        if name:
            student.name = name
        if age is not None:
            student.age = age
        if course:
            student.course = course
        if marks is not None:
            student.marks = marks
        self._save()

    def delete(self, roll_no):
        student = self.find_by_roll(roll_no)
        if not student:
            raise LookupError(f"No student found with roll number {roll_no}.")
        self.students.remove(student)
        self._save()

    # ---------- search ----------
    def search_by_name(self, text):
        text = text.lower()
        return [s for s in self.students if text in s.name.lower()]

    def search_by_course(self, text):
        text = text.lower()
        return [s for s in self.students if text in s.course.lower()]

    # ---------- sort ----------
    def sorted_by_name(self, reverse=False):
        return sorted(self.students, key=lambda s: s.name.lower(), reverse=reverse)

    def sorted_by_marks(self, reverse=True):
        return sorted(self.students, key=lambda s: s.marks, reverse=reverse)

    def sorted_by_roll(self):
        return sorted(self.students, key=lambda s: s.roll_no)

    # ---------- storage switching ----------
    def switch_format(self, new_format):
        """Convert all data to the other file format (json <-> csv)."""
        if storage.save_students(self.students, new_format):
            storage.set_format(new_format)
            return True
        return False
