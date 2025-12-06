import tkinter as tk
from tkinter import ttk, messagebox
import sqlite3


conn = sqlite3.connect("student_data.db")
cursor = conn.cursor()

root = tk.Tk()
root.title("Attendance Viewer")
root.geometry("700x500")

#view by uid
def view_by_uid():
    for widget in main_frame.winfo_children():
        widget.destroy()

    tk.Label(main_frame, text="Enter UID:", font=("Arial", 12)).pack(pady=5)
    uid_entry = tk.Entry(main_frame, font=("Arial", 12))
    uid_entry.pack(pady=5)

    def search_uid():
        uid = uid_entry.get().strip()
        if not uid:
            messagebox.showerror("Error", "Please enter a UID")
            return

        cursor.execute("SELECT date, status, timestamp FROM attendance WHERE uid=?", (uid,))
        records = cursor.fetchall()

        for item in tree.get_children():
            tree.delete(item)

        for r in records:
            tree.insert("", "end", values=r)

        if not records:
            messagebox.showinfo("Info", "No attendance records found for this UID.")

    tk.Button(main_frame, text="Search", command=search_uid, bg="#0078D7", fg="white").pack(pady=5)

    
    columns = ("Date", "Status", "Timestamp")
    tree = ttk.Treeview(main_frame, columns=columns, show="headings")
    for col in columns:
        tree.heading(col, text=col)
        tree.column(col, width=150)
    tree.pack(pady=10, fill="both", expand=True)

# daywise attendance
def view_by_date():
    for widget in main_frame.winfo_children():
        widget.destroy()

    tk.Label(main_frame, text="Enter Date (YYYY-MM-DD):", font=("Arial", 12)).pack(pady=5)
    date_entry = tk.Entry(main_frame, font=("Arial", 12))
    date_entry.pack(pady=5)

    def search_date():
        date = date_entry.get().strip()
        if not date:
            messagebox.showerror("Error", "Please enter a date")
            return

        
        cursor.execute("SELECT uid, name FROM users")
        all_students = cursor.fetchall()

       
        cursor.execute("SELECT uid, status FROM attendance WHERE date=?", (date,))
        marked = dict(cursor.fetchall())

        for item in tree.get_children():
            tree.delete(item)

        
        for uid, name in all_students:
            status = marked.get(uid, "Absent")
            tree.insert("", "end", values=(uid, name, status))

    tk.Button(main_frame, text="Show Attendance", command=search_date, bg="#0078D7", fg="white").pack(pady=5)

    
    columns = ("UID", "Name", "Status")
    tree = ttk.Treeview(main_frame, columns=columns, show="headings")
    for col in columns:
        tree.heading(col, text=col)
        tree.column(col, width=150)
    tree.pack(pady=10, fill="both", expand=True)


sidebar = tk.Frame(root, bg="#202020", width=180)
sidebar.pack(side="left", fill="y")

tk.Label(sidebar, text="Attendance Management System", bg="#202020", fg="white", font=("Arial", 14, "bold")).pack(pady=20)

tk.Button(sidebar, text="Search by Student ID", command=view_by_uid, width=20, bg="#444", fg="white").pack(pady=10)
tk.Button(sidebar, text="View Day-wise Sheet", command=view_by_date, width=20, bg="#444", fg="white").pack(pady=10)


main_frame = tk.Frame(root, bg="#f0f0f0")
main_frame.pack(side="right", fill="both", expand=True)

root.mainloop()
conn.close()
