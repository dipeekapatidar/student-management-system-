"""
auth.py - Admin login authentication (passwords are stored hashed, never as plain text)
Project  : Student Management System
Author   : Dipeeka Patidar

Default login (first run):
    username : admin
    password : dipeeka@123
(Change it from the menu after logging in.)
"""
import hashlib
import json
import secrets

from storage import DATA_DIR
from utils import get_password, get_text

ADMIN_FILE = DATA_DIR / "admin.json"
MAX_ATTEMPTS = 3


def _hash(password, salt_hex):
    return hashlib.pbkdf2_hmac(
        "sha256", password.encode("utf-8"), bytes.fromhex(salt_hex), 100_000
    ).hex()


def _create_admin(username, password):
    DATA_DIR.mkdir(exist_ok=True)
    salt = secrets.token_hex(16)
    with open(ADMIN_FILE, "w", encoding="utf-8") as f:
        json.dump({"username": username, "salt": salt,
                   "password_hash": _hash(password, salt)}, f, indent=4)


def _load_admin():
    try:
        with open(ADMIN_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
        _create_admin("admin", "dipeeka@123")
        with open(ADMIN_FILE, "r", encoding="utf-8") as f:
            return json.load(f)


def login():
    """Returns the username on success, or None after 3 failed attempts."""
    admin = _load_admin()
    print("\n=========== ADMIN LOGIN ===========")
    for attempt in range(1, MAX_ATTEMPTS + 1):
        username = get_text("Username: ")
        password = get_password("Password: ")
        if (username == admin["username"]
                and secrets.compare_digest(_hash(password, admin["salt"]),
                                           admin["password_hash"])):
            print(f"\n  Login successful. Welcome, {username}!")
            return username
        left = MAX_ATTEMPTS - attempt
        print(f"  [!] Wrong username or password. Attempts left: {left}")
    return None


def change_password():
    admin = _load_admin()
    old = get_password("Enter current password: ")
    if _hash(old, admin["salt"]) != admin["password_hash"]:
        print("  [!] Current password is wrong.")
        return False
    new = get_password("Enter new password (min 6 characters): ")
    if len(new) < 6:
        print("  [!] Password too short. Not changed.")
        return False
    again = get_password("Confirm new password: ")
    if new != again:
        print("  [!] Passwords do not match. Not changed.")
        return False
    _create_admin(admin["username"], new)
    print("  Password changed successfully.")
    return True
