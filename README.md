# Epic Account Data Generator

A Python utility that generates **realistic account details** optimized for the Epic Games signup form.  
It helps you quickly fill in the registration page by:
- Opening **Temp-Mail** in your browser to get a disposable email.
- Opening the **Epic Games signup page**.
- Generating a random **first name**, **last name**, **display name**, **strong password**, and **birth date**.
- Copying each field to your clipboard step by step so you can paste directly into the signup form.

---

## ✨ Features
- Random **English names** (first & last).
- Display name follows Epic’s typical rules (3–16 chars, starts with a letter, only `a–z`, `0–9`, `_`).
- Strong password with at least 1 uppercase, 1 lowercase, 1 digit, and 1 special character.
- Valid random birth date within a reasonable adult age range (1970–2004 by default).
- Country optimized for **English-speaking users** (default: United States, optional: UK, Canada, Australia, Ireland, New Zealand).
- Stores all generated account details in `account_details.txt`.
- Guided workflow: press Enter to copy each value to your clipboard.

---

## 🚀 How It Works
1. Choose `1` in the console menu.
2. Your browser will open **Temp-Mail** → copy a temporary email.
3. Paste the email into the program.
4. The program generates account details.
5. The Epic Games signup page opens automatically.
6. The program shows each field (Email → First name → Last name → Password → Display name).  
   - Press **Enter** to copy it to your clipboard.  
   - **Paste** into the Epic signup form (Ctrl+V).
7. Continue through the form, set your country, agree to ToS, and create the account.

---

## 🛠 Requirements
- **Python 3.10+** (tested with 3.12 and 3.13)
- Works on **Windows**, **Linux**, and **macOS**.
- No external packages needed – uses only the Python standard library.

### Clipboard support:
- Windows → uses built-in `clip` command.
- Linux/macOS → requires `tkinter` (often preinstalled).
  - Ubuntu/Debian: `sudo apt install python3-tk`
  - Fedora: `sudo dnf install python3-tkinter`

---

## ▶️ Run the Program
```bash
python main.py
```

## 📂 Project Structure
```bash
├── main.py              # Main script
├── account_details.txt  # Generated accounts (auto-created)
├── README.md            # This documentation
```

## ⚠️ Disclaimer
This tool is for educational and personal testing purposes only.
Using fake or disposable data to create accounts may violate Epic Games’ Terms of Service.
Use responsibly.
