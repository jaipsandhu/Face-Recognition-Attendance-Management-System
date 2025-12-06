import cv2
import face_recognition
import sqlite3
import os

def start_capture(uid):
    conn = sqlite3.connect("student_data.db")
    cursor = conn.cursor()
    
    save_dir = f"dataset/{uid}"
    os.makedirs(save_dir, exist_ok=True)

    cap = cv2.VideoCapture(0)
    if not cap.isOpened():
        print("❌ Error: Cannot access camera.")
        return

    cv2.namedWindow("Face Capture - Press 'Q' to Quit")
    count = 0

    print("\n Camera started. Show your face clearly to capture images.")
    print("Press 'Q' anytime to exit.\n")

    while count < 10:
        ret, frame = cap.read()
        if not ret:
            print("⚠️ Failed to grab frame.")
            break

        # Convert for face_recognition
        rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        boxes = face_recognition.face_locations(rgb_frame)

        message = ""

        if len(boxes) > 1:
            message = " More than one face detected!"
        elif len(boxes) == 0:
            message = "No face detected. Adjust position."
        else:
            # Encode and save
            encodings = face_recognition.face_encodings(rgb_frame, boxes)
            if encodings:
                encoding_blob = encodings[0].tobytes()
                img_path = f"{save_dir}/img_{count}.jpg"
                cv2.imwrite(img_path, frame)

                cursor.execute("""
                    INSERT INTO images (uid, image_path, encoding)
                    VALUES (?, ?, ?)
                """, (uid, img_path, encoding_blob))
                conn.commit()

                count += 1
                message = f"Captured {count}/10"

        # Show feedback text on frame
        cv2.putText(frame, message, (20, 40), cv2.FONT_HERSHEY_SIMPLEX,
                    0.8, (0, 0, 255) if "⚠️" in message else (0, 255, 0), 2)

        cv2.imshow("Face Capture - Press 'Q' to Quit", frame)

        # Exit on 'q'
        if cv2.waitKey(1) & 0xFF == ord('q'):
            print(" User stopped capture early.")
            break

    cap.release()
    cv2.destroyAllWindows()
    conn.close()
    print("\n Face capture completed successfully!\n")
