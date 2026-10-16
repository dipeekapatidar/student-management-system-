"""
============================================================
  STUDENT MANAGEMENT SYSTEM  (Python, console based)
  Developed by : Dipeeka Patidar
============================================================
Features:
  * Add / update / delete / search student records
  * Data stored in JSON or CSV files
  * Sort records by name or marks
  * Admin login authentication
  * Reports: topper, average marks, pass %, grades ...
  * Exception handling for invalid inputs

Run with:   python main.py
"""
import auth
import reports
import storage
from manager import StudentManager
from utils import (clear_screen, confirm, get_float, get_int, get_name,
                   get_text, pause)

AUTHOR = "Dipeeka Patidar"


def banner():
    print("=" * 60)
    print("        STUDENT MANAGEMENT SYSTEM")
    print(f"        Developed by {AUTHOR}")
    print("=" * 60)


def show_students(students, title="Student Records"):
    print(f"\n--- {title} ---")
    if not students:
        print("  No records found.")
        return
    print(students[0].table_header())
    for s in students:
        print(s.table_row())
    print("-" * 74)
    print(f"  Total: {len(students)}")


# ---------------- menu actions ----------------
def add_student(mgr):
    print("\n--- Add New Student ---")
    roll = get_int("Roll number: ", min_value=1)
    if mgr.find_by_roll(roll):
        print(f"  [!] Roll number {roll} already exists.")
        return
    name = get_name("Name: ")
    age = get_int("Age (5-100): ", 5, 100)
    course = get_text("Course: ")
    marks = get_float("Marks (0-100): ", 0, 100)
    try:
        mgr.add(roll, name, age, course, marks)
        print("  Student added successfully!")
    except ValueError as err:
        print(f"  [!] {err}")


def update_student(mgr):
    print("\n--- Update Student ---")
    roll = get_int("Enter roll number to update: ", min_value=1)
    student = mgr.find_by_roll(roll)
    if not student:
        print("  [!] Student not found.")
        return
    show_students([student], "Current details")
    print("(Press Enter to keep the old value)")
    name = get_name(f"New name [{student.name}]: ", allow_empty=True)
    age = get_int(f"New age [{student.age}]: ", 5, 100, allow_empty=True)
    course = get_text(f"New course [{student.course}]: ", allow_empty=True)
    marks = get_float(f"New marks [{student.marks}]: ", 0, 100, allow_empty=True)
    try:
        mgr.update(roll, name or None, age, course or None, marks)
        print("  Record updated successfully!")
    except LookupError as err:
        print(f"  [!] {err}")


def delete_student(mgr):
    print("\n--- Delete Student ---")
    roll = get_int("Enter roll number to delete: ", min_value=1)
    student = mgr.find_by_roll(roll)
    if not student:
        print("  [!] Student not found.")
        return
    show_students([student], "Record to delete")
    if confirm("Are you sure you want to delete this record?"):
        mgr.delete(roll)
        print("  Record deleted.")
    else:
        print("  Deletion cancelled.")


def search_student(mgr):
    print("\n--- Search Student ---")
    print("1. By roll number\n2. By name\n3. By course")
    choice = get_int("Choose (1-3): ", 1, 3)
    if choice == 1:
        roll = get_int("Roll number: ", min_value=1)
        s = mgr.find_by_roll(roll)
        show_students([s] if s else [], "Search Result")
    elif choice == 2:
        show_students(mgr.search_by_name(get_text("Name (or part of it): ")), "Search Result")
    else:
        show_students(mgr.search_by_course(get_text("Course (or part of it): ")), "Search Result")


def sort_students(mgr):
    print("\n--- Sort Records ---")
    print("1. By name (A-Z)\n2. By name (Z-A)\n3. By marks (high to low)"
          "\n4. By marks (low to high)\n5. By roll number")
    choice = get_int("Choose (1-5): ", 1, 5)
    if choice == 1:
        show_students(mgr.sorted_by_name(), "Sorted by Name (A-Z)")
    elif choice == 2:
        show_students(mgr.sorted_by_name(reverse=True), "Sorted by Name (Z-A)")
    elif choice == 3:
        show_students(mgr.sorted_by_marks(), "Sorted by Marks (High-Low)")
    elif choice == 4:
        show_students(mgr.sorted_by_marks(reverse=False), "Sorted by Marks (Low-High)")
    else:
        show_students(mgr.sorted_by_roll(), "Sorted by Roll Number")


def report_menu(mgr):
    print("\n--- Reports ---")
    print("1. Full report\n2. Topper(s)\n3. Average marks\n4. Pass percentage"
          "\n5. Export all records to report.csv")
    choice = get_int("Choose (1-5): ", 1, 5)
    data = mgr.students
    if not data:
        print("  No records available.")
        return
    if choice == 1:
        print("\n" + reports.full_report(data))
    elif choice == 2:
        show_students(reports.topper(data), "Topper(s)")
    elif choice == 3:
        print(f"\n  Average marks of all students: {reports.average_marks(data):.2f}")
    elif choice == 4:
        print(f"\n  Pass percentage: {reports.pass_percentage(data):.2f}%")
    else:
        path = storage.export_report_csv(mgr.sorted_by_roll())
        if path:
            print(f"  Exported to: {path}")


def settings_menu(mgr):
    print("\n--- Settings ---")
    print(f"Current storage format: {storage.get_format().upper()}")
    print("1. Change admin password\n2. Switch storage format (JSON <-> CSV)\n3. Back")
    choice = get_int("Choose (1-3): ", 1, 3)
    if choice == 1:
        auth.change_password()
    elif choice == 2:
        new_fmt = "csv" if storage.get_format() == "json" else "json"
        if confirm(f"Switch storage to {new_fmt.upper()}?"):
            if mgr.switch_format(new_fmt):
                print(f"  Storage switched to {new_fmt.upper()}. Existing data was converted.")


def main_menu():
    mgr = StudentManager()
    actions = {
        1: add_student, 2: update_student, 3: delete_student,
        4: lambda m: show_students(m.sorted_by_roll(), "All Students"),
        5: search_student, 6: sort_students, 7: report_menu, 8: settings_menu,
    }
    while True:
        print("\n" + "=" * 60)
        print(f"  MAIN MENU   (storage: {storage.get_format().upper()})")
        print("=" * 60)
        print(" 1. Add student        5. Search student")
        print(" 2. Update student     6. Sort records")
        print(" 3. Delete student     7. Reports")
        print(" 4. View all students  8. Settings")
        print(" 0. Logout & Exit")
        choice = get_int("Enter your choice: ", 0, 8)
        if choice == 0:
            print(f"\n  Thank you for using the system. - {AUTHOR}")
            break
        try:
            actions[choice](mgr)
        except Exception as err:  # safety net so the program never crashes
            print(f"  [!] Something went wrong: {err}")
        pause()


def main():
    clear_screen()
    banner()
    try:
        user = auth.login()
        if user is None:
            print("\n  Too many failed attempts. Exiting.")
            return
        main_menu()
    except (KeyboardInterrupt, EOFError):
        print("\n\n  Program closed by user. Goodbye!")


if __name__ == "__main__":
    main()
