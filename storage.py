"""
storage.py - Save / load student records using JSON or CSV files
Project  : Student Management System
Author   : Dipeeka Patidar
"""
import csv
import json
from pathlib import Path

from student import Student

BASE_DIR = Path(__file__).resolve().parent
DATA_DIR = BASE_DIR / "data"
JSON_FILE = DATA_DIR / "students.json"
CSV_FILE = DATA_DIR / "students.csv"
CONFIG_FILE = DATA_DIR / "config.json"
FIELDS = ["roll_no", "name", "age", "course", "marks"]


def _ensure_dir():
    DATA_DIR.mkdir(exist_ok=True)


def get_format():
    """Returns the storage format currently selected ('json' or 'csv')."""
    _ensure_dir()
    try:
        with open(CONFIG_FILE, "r", encoding="utf-8") as f:
            fmt = json.load(f).get("storage_format", "json")
        return fmt if fmt in ("json", "csv") else "json"
    except (FileNotFoundError, json.JSONDecodeError):
        return "json"


def set_format(fmt):
    _ensure_dir()
    with open(CONFIG_FILE, "w", encoding="utf-8") as f:
        json.dump({"storage_format": fmt}, f, indent=4)


def load_students(fmt=None):
    """Load all students. Returns an empty list if the file is missing/corrupt."""
    fmt = fmt or get_format()
    _ensure_dir()
    students = []
    try:
        if fmt == "json":
            with open(JSON_FILE, "r", encoding="utf-8") as f:
                for item in json.load(f):
                    students.append(Student.from_dict(item))
        else:
            with open(CSV_FILE, "r", newline="", encoding="utf-8") as f:
                for row in csv.DictReader(f):
                    students.append(Student.from_dict(row))
    except FileNotFoundError:
        return []
    except (json.JSONDecodeError, KeyError, ValueError, TypeError):
        print(f"  [!] Warning: {fmt.upper()} data file is damaged or invalid. Starting with empty records.")
        return []
    return students


def save_students(students, fmt=None):
    fmt = fmt or get_format()
    _ensure_dir()
    try:
        if fmt == "json":
            with open(JSON_FILE, "w", encoding="utf-8") as f:
                json.dump([s.to_dict() for s in students], f, indent=4)
        else:
            with open(CSV_FILE, "w", newline="", encoding="utf-8") as f:
                writer = csv.DictWriter(f, fieldnames=FIELDS)
                writer.writeheader()
                for s in students:
                    writer.writerow(s.to_dict())
        return True
    except OSError as err:
        print(f"  [!] Could not save data: {err}")
        return False


def export_report_csv(rows, filename="report.csv"):
    """Export any list of Student objects to a separate CSV file."""
    _ensure_dir()
    path = DATA_DIR / filename
    try:
        with open(path, "w", newline="", encoding="utf-8") as f:
            writer = csv.DictWriter(f, fieldnames=FIELDS)
            writer.writeheader()
            for s in rows:
                writer.writerow(s.to_dict())
        return path
    except OSError as err:
        print(f"  [!] Could not export: {err}")
        return None
