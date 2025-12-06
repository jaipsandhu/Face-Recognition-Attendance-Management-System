import tkinter as tk
from tkinter import messagebox
import sqlite3
from face_capture import start_capture

# create db connection
conn = sqlite3.connect("student_data.db")
cursor = conn.cursor()

cursor.execute("""
    CREATE TABLE IF NOT EXISTS images (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        uid TEXT NOT NULL,
        image_path TEXT NOT NULL,
        encoding BLOB NOT NULL,
        FOREIGN KEY(uid) REFERENCES users(uid)
    )
""")
conn.commit()


def save_data():
    name = entry_name.get().strip().capitalize()
    uid = entry_uid.get().strip()
    
    if not name or not uid:
        messagebox.showerror("Error","Please enter both Name and UID.")
        return
    
    if not uid.isdigit() or len(uid) != 5:
        messagebox.showerror("Error","UID must be exactly 5 digits.")
        return
        
    try:
        cursor.execute("INSERT INTO users (uid,name) VALUES (?,?)", (uid,name))
        conn.commit()

        messagebox.showinfo("Success", f"Data saved! UID in DB: {uid}")

       
        capture_btn.config(state="normal", command=lambda: start_capture(uid))
        
        start_capture(uid)

    except sqlite3.IntegrityError:
        messagebox.showerror("Error", "This UID already exists. Please enter a unique UID.")
    except Exception as e:
        messagebox.showerror("Database Error", f"An error occurred: {e}")


# GUI
root = tk.Tk()
root.title("Student Data Entry")
root.geometry("300x200")

# Name input
tk.Label(root, text="Name:").pack(pady=5)
entry_name = tk.Entry(root)
entry_name.pack(pady=5)

# UID input
tk.Label(root, text="UID (5 digits):").pack(pady=5)
entry_uid = tk.Entry(root)
entry_uid.pack(pady=5)

# Save button
save_button = tk.Button(root, text="Save", command=save_data)
save_button.pack(pady=10)

capture_btn = tk.Button(root, text="Capture Face", state="disabled",  width=20)
capture_btn.pack(pady=10)

root.mainloop()
