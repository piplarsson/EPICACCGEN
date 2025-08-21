import sys
import re
import secrets
import string
import random
import calendar
import webbrowser
import subprocess
from dataclasses import dataclass
from pathlib import Path
from datetime import datetime, date

# =============================
# Configuration
# =============================

OUTPUT_FILE = Path("account_details.txt")
PASSWORD_LENGTH = 12
DOB_YEAR_MIN = 1970
DOB_YEAR_MAX = 2004  # reasonable adult range

TEMP_MAIL_URL = "https://temp-mail.org/"
EPIC_SIGNUP_URL = "https://www.epicgames.com/id/register"

SAFE_PUNCT = "!@#$%^&*()-_=+[]{}:;,./?"
PASSWORD_ALPHABET = string.ascii_letters + string.digits + SAFE_PUNCT

# Common English names
FIRST_NAMES = [
    "Oliver", "George", "Harry", "Jack", "Noah",
    "Olivia", "Amelia", "Isla", "Ava", "Mia",
    "Liam", "Emma", "Sophia", "Charlotte", "James",
    "Benjamin", "Lucas", "Henry", "Ethan", "Grace"
]
LAST_NAMES = [
    "Smith", "Johnson", "Williams", "Brown", "Jones",
    "Miller", "Davis", "Garcia", "Rodriguez", "Wilson",
    "Taylor", "Thomas", "Moore", "Martin", "Jackson"
]

ENGLISH_COUNTRIES = [
    "United States",
    "United Kingdom",
    "Canada",
    "Australia",
    "Ireland",
    "New Zealand",
]

DEFAULT_COUNTRY = "United States"

# =============================
# OS helpers (topmost & clipboard)
# =============================

def set_window_always_on_top_safe() -> None:
    """Make console 'always on top' on Windows without moving/resizing."""
    if sys.platform != "win32":
        return
    try:
        from ctypes import windll  # type: ignore
        HWND_TOPMOST = -1
        SWP_NOMOVE = 0x0002
        SWP_NOSIZE = 0x0001
        flags = SWP_NOMOVE | SWP_NOSIZE
        hwnd = windll.user32.GetForegroundWindow()
        if hwnd:
            windll.user32.SetWindowPos(hwnd, HWND_TOPMOST, 0, 0, 0, 0, flags)
    except Exception:
        pass

def copy_to_clipboard(text: str) -> bool:
    """
    Copy text to clipboard.
    - Windows: uses 'clip'
    - Others: tries tkinter if available
    """
    try:
        if sys.platform == "win32":
            p = subprocess.Popen(["clip"], stdin=subprocess.PIPE, text=True)
            p.communicate(text)
            return p.returncode == 0
        else:
            try:
                import tkinter as tk  # type: ignore
                r = tk.Tk()
                r.withdraw()
                r.clipboard_clear()
                r.clipboard_append(text)
                r.update()
                r.destroy()
                return True
            except Exception:
                return False
    except Exception:
        return False

# =============================
# Validation
# =============================

EMAIL_REGEX = re.compile(r"^[^@\s]+@[^@\s]+\.[^@\s]+$")

def is_valid_email(email: str) -> bool:
    return bool(EMAIL_REGEX.match(email.strip()))

# =============================
# Dates & names
# =============================

def convert_month_number(month_number: int) -> str:
    return calendar.month_abbr[month_number]

def generate_valid_date(min_year: int = DOB_YEAR_MIN, max_year: int = DOB_YEAR_MAX) -> str:
    """Return a valid date string (DD/Mon/YYYY) within the given range."""
    year = secrets.choice(range(min_year, max_year + 1))
    month = secrets.choice(range(1, 13))
    while True:
        day = secrets.choice(range(1, 32))
        try:
            d = date(year, month, day)
            return f"{d.day:02d}/{convert_month_number(d.month)}/{d.year}"
        except ValueError:
            continue

def generate_names() -> tuple[str, str]:
    """English first/last name."""
    return secrets.choice(FIRST_NAMES), secrets.choice(LAST_NAMES)

def sanitize_display_name(base: str) -> str:
    """
    Conservative display name rules:
    - 3–16 characters
    - starts with a letter
    - a–z, 0–9, underscore only
    """
    allowed = string.ascii_lowercase + string.digits + "_"
    base = base.lower()

    if not base or not base[0].isalpha():
        base = "a" + base

    filtered = [ch if ch in allowed else "_" for ch in base]
    s = "".join(filtered)

    s = s[:16]
    while len(s) < 3:
        s += str(secrets.randbelow(10))
    return s

def generate_display_name(first: str, last: str) -> str:
    """Builds a likely-unique, policy-friendly display name."""
    base = first + last + str(secrets.randbelow(9000) + 1000)  # 1000–9999
    return sanitize_display_name(base)

# =============================
# Passwords
# =============================

def generate_password(length: int = PASSWORD_LENGTH) -> str:
    """
    Strong password with:
    - minimum 10 chars
    - at least 1 lowercase, 1 uppercase, 1 digit, 1 special
    """
    if length < 10:
        length = 10

    req = [
        secrets.choice(string.ascii_lowercase),
        secrets.choice(string.ascii_uppercase),
        secrets.choice(string.digits),
        secrets.choice(SAFE_PUNCT),
    ]
    remaining = [secrets.choice(PASSWORD_ALPHABET) for _ in range(length - len(req))]
    chars = req + remaining
    secrets.SystemRandom().shuffle(chars)
    return "".join(chars)

# =============================
# Dataclass & I/O
# =============================

@dataclass
class AccountDetails:
    email: str
    first_name: str
    last_name: str
    display_name: str
    date_str: str
    password: str
    country: str
    created_at: str

    def to_text_block(self) -> str:
        lines = [
            f"Email: {self.email}",
            f"First name: {self.first_name}",
            f"Last name: {self.last_name}",
            f"Create password: {self.password}",
            f"Add a display name: {self.display_name}",
            f"Date: {self.date_str}",
            f"Country: {self.country}",
            f"Created: {self.created_at}",
            "-" * 31,
        ]
        return "\n".join(lines)

def append_to_file(block: str, file_path: Path = OUTPUT_FILE) -> None:
    file_path.parent.mkdir(parents=True, exist_ok=True)
    with file_path.open("a", encoding="utf-8") as f:
        f.write(block + "\n")

# =============================
# Generation
# =============================

def generate_account(email: str, country: str) -> AccountDetails:
    first, last = generate_names()
    display = generate_display_name(first, last)
    dob = generate_valid_date()
    pwd = generate_password(PASSWORD_LENGTH)
    now_iso = datetime.now().isoformat(timespec="seconds")
    return AccountDetails(
        email=email.strip(),
        first_name=first,
        last_name=last,
        display_name=display,
        date_str=dob,
        password=pwd,
        country=country,
        created_at=now_iso,
    )

# =============================
# Interactive flow
# =============================

def choose_country() -> str:
    print("\nSelect country (press Enter for default):")
    for i, c in enumerate(ENGLISH_COUNTRIES, start=1):
        default_mark = " (default)" if c == DEFAULT_COUNTRY else ""
        print(f"{i}. {c}{default_mark}")

    raw = input("Choice [1-6, Enter=default]: ").strip()
    if raw.isdigit():
        idx = int(raw)
        if 1 <= idx <= len(ENGLISH_COUNTRIES):
            return ENGLISH_COUNTRIES[idx - 1]
    return DEFAULT_COUNTRY

def guide_copy_field(label: str, value: str) -> None:
    """Show value and copy it to clipboard when user presses Enter."""
    print(f"\n{label}: {value}")
    input("Press Enter to copy to clipboard... ")
    ok = copy_to_clipboard(value)
    if ok:
        print("✅ Copied! Paste it in the form (Ctrl+V).")
    else:
        print("⚠️ Could not copy automatically. Please copy manually from above.")

def menu_loop() -> None:
    set_window_always_on_top_safe()

    while True:
        print("\nPlease select an option:")
        print("1. Create new account data (optimized for Epic form)")
        print("2. Quit")

        choice = input("Enter your choice: ").strip()

        if choice == "1":
            # 1) open Temp-Mail
            print("Opening temporary email service...")
            webbrowser.open(TEMP_MAIL_URL, new=2)

            # 2) ask for email
            email = input("Paste your temporary email address here: ").strip()
            if not is_valid_email(email):
                print("Invalid email format. Try again.\n")
                continue

            # 3) choose an English-speaking country (default US)
            country = choose_country()

            # 4) generate details
            acc = generate_account(email, country)
            block = acc.to_text_block()
            append_to_file(block)

            # 5) open Epic signup
            print("Opening Epic signup...")
            webbrowser.open(EPIC_SIGNUP_URL, new=2)

            print("\n--- Guided fill (press Enter to copy each field) ---")
            guide_copy_field("Email address", acc.email)
            guide_copy_field("First name", acc.first_name)
            guide_copy_field("Last name", acc.last_name)
            guide_copy_field("Create password", acc.password)
            guide_copy_field("Add a display name", acc.display_name)
            print(f"\nCountry: {acc.country} (pick it in the dropdown if not preselected).")
            print("\nRemember to agree to the Terms of Service before clicking Continue.")

            more = input("\nGenerate another? (Y/N): ").strip().upper()
            if more == "N":
                break

        elif choice == "2":
            break
        else:
            print("Invalid choice. Please try again.\n")

    input("Press Enter to exit...")

# =============================
# Entrypoint
# =============================

if __name__ == "__main__":
    menu_loop()
