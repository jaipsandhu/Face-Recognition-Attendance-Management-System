import cv2
import face_recognition
import pickle
import sqlite3
from datetime import datetime


date_input = input("Enter date for attendance (YYYY-MM-DD): ")

with open("encodings.pickle", "rb") as f:
    data = pickle.load(f)

conn = sqlite3.connect("student_data.db")
cursor = conn.cursor()

# Create attendance table if not exists
cursor.execute("""
CREATE TABLE IF NOT EXISTS attendance (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    uid TEXT NOT NULL,
    date TEXT NOT NULL,
    status TEXT NOT NULL,
    timestamp TEXT NOT NULL
)
""")
conn.commit()

def mark_present(uid):
    cursor.execute("SELECT * FROM attendance WHERE uid=? AND date=?", (uid, date_input))
    if cursor.fetchone():
        return  # already marked
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    cursor.execute("INSERT INTO attendance (uid, date, status, timestamp) VALUES (?, ?, ?, ?)",
                   (uid, date_input, "Present", timestamp))
    conn.commit()
    print(f"[MARKED PRESENT] {uid} at {timestamp}")

#camera
video = cv2.VideoCapture(0)

print("[INFO] Press 'q' to stop attendance marking")

while True:
    ret, frame = video.read()
    if not ret:
        print("Failed to capture frame")
        break

    rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    face_locations = face_recognition.face_locations(rgb_frame)
    face_encodings = face_recognition.face_encodings(rgb_frame, face_locations)

    for encoding, (top, right, bottom, left) in zip(face_encodings, face_locations):
        matches = face_recognition.compare_faces(data["encodings"], encoding)
        uid = "Unknown"

        if True in matches:
            matchedIdxs = [i for (i, b) in enumerate(matches) if b]
            counts = {}

            for i in matchedIdxs:
                uid_name = data["names"][i]  
                counts[uid_name] = counts.get(uid_name, 0) + 1

            uid = max(counts, key=counts.get)
            mark_present(uid)
        else:
            uid = "Unknown"

        # green box display
        color = (0, 255, 0) if uid != "Unknown" else (0, 0, 255)
        cv2.rectangle(frame, (left, top), (right, bottom), color, 2)
        cv2.putText(frame, uid, (left, top - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.6, color, 2)

    cv2.imshow("Attendance System", frame)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break


video.release()
cv2.destroyAllWindows()
conn.close()
print("[INFO] Attendance marking finished!")
