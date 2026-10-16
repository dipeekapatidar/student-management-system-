"""
reports.py - Report generation (topper, average, pass %, grades ...)
Project  : Student Management System
Author   : Dipeeka Patidar
"""
from collections import defaultdict


def topper(students):
    if not students:
        return []
    best = max(s.marks for s in students)
    return [s for s in students if s.marks == best]


def lowest(students):
    if not students:
        return []
    worst = min(s.marks for s in students)
    return [s for s in students if s.marks == worst]


def average_marks(students):
    if not students:
        return 0.0
    return sum(s.marks for s in students) / len(students)


def pass_percentage(students):
    if not students:
        return 0.0
    passed = sum(1 for s in students if s.marks >= 40)
    return passed * 100 / len(students)


def grade_distribution(students):
    dist = defaultdict(int)
    for s in students:
        dist[s.grade] += 1
    return dict(dist)


def course_wise_average(students):
    totals = defaultdict(list)
    for s in students:
        totals[s.course].append(s.marks)
    return {course: sum(m) / len(m) for course, m in totals.items()}


def full_report(students):
    """Returns the whole report as a printable string."""
    if not students:
        return "No student records available to generate a report."
    lines = ["=" * 50, "        STUDENT PERFORMANCE REPORT", "=" * 50]
    lines.append(f"Total students   : {len(students)}")
    lines.append(f"Average marks    : {average_marks(students):.2f}")
    lines.append(f"Pass percentage  : {pass_percentage(students):.2f}%")
    lines.append("")
    for s in topper(students):
        lines.append(f"Topper           : {s.name} (Roll {s.roll_no}) - {s.marks:.2f} marks")
    for s in lowest(students):
        lines.append(f"Lowest scorer    : {s.name} (Roll {s.roll_no}) - {s.marks:.2f} marks")
    lines.append("")
    lines.append("Grade distribution:")
    for grade in ["A+", "A", "B", "C", "D", "F"]:
        count = grade_distribution(students).get(grade, 0)
        lines.append(f"   {grade:<3}: {count}")
    lines.append("")
    lines.append("Course-wise average marks:")
    for course, avg in sorted(course_wise_average(students).items()):
        lines.append(f"   {course:<18}: {avg:.2f}")
    lines.append("=" * 50)
    return "\n".join(lines)
