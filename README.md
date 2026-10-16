# Student Management System (Python)
Developed by **Dipeeka Patidar**

A console-based project to manage student records.

## Features
- Add, update, delete and search students (by roll number, name or course)
- Data stored in **JSON or CSV** (switch anytime from Settings, data converts automatically)
- Sort by name (A-Z / Z-A), marks (high-low / low-high) or roll number
- Admin login (password stored hashed using PBKDF2 + salt)
- Reports: topper, lowest scorer, average marks, pass %, grade distribution, course-wise average, export to CSV
- Exception handling: invalid numbers, empty input, duplicate roll numbers, damaged data files, Ctrl+C

## Default login (first run)
- Username: `admin`
- Password: `dipeeka@123`  (change it from Settings after login)

## How to run
1. Install Python 3.8 or newer (https://www.python.org/downloads/) - tick "Add Python to PATH".
2. Extract the zip, open a terminal inside the folder.
3. Run: `python main.py`  (Mac/Linux: `python3 main.py`)
   Windows: you can also double-click `run_windows.bat`.

No extra libraries are needed.

## Project structure
| File | Purpose |
|------|---------|
| main.py | Menu and program flow |
| auth.py | Admin login and password change |
| manager.py | Add / update / delete / search / sort logic |
| student.py | Student class (grade and result calculation) |
| storage.py | JSON / CSV reading and writing |
| reports.py | Report calculations |
| utils.py | Safe input helpers (validation) |
| data/ | Created files: students.json / students.csv, admin.json, config.json |

## Grading scheme
90+ A+, 80+ A, 70+ B, 60+ C, 40+ D, below 40 F (Fail)
# student-management-system-
