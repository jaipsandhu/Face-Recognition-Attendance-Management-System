import sqlite3
import os
import shutil

DB_FILE = "student_data.db"
ENCODINGS_FILE = "encodings.pkl"  
DATASET_DIR = "dataset"

print("WARNING: This will permanently delete ALL data (DB tables + encodings + face images)!")
confirm =input("Type 'YES' to confirm: ")

if confirm.strip().upper() == "YES":
    try:
       
        conn = sqlite3.connect(DB_FILE)
        cursor = conn.cursor()

        cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
        tables = [t[0] for t in cursor.fetchall()]

        if tables:
            for table in tables:
                cursor.execute(f"DELETE FROM {table}")
                print(f"[INFO] Cleared table: {table}")
            conn.commit()
        else:
            print("[INFO] No tables found in the database.")

        if os.path.exists(ENCODINGS_FILE):
            os.remove(ENCODINGS_FILE)
            print(f"[INFO] Deleted {ENCODINGS_FILE}")
        else:
            print("[INFO] No encodings file found.")

        if os.path.exists(DATASET_DIR):
            shutil.rmtree(DATASET_DIR)
            print(f"[INFO] Deleted folder: {DATASET_DIR}")
        else:
            print("[INFO] No dataset folder found.")

        print("ALL DATA CLEARED SUCCESSFULLY.")

    except Exception as e:
        print("Error while clearing data:", e)
    finally:
        conn.close()
else:
    print("Operation cancelled.")
