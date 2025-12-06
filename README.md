# Face-Recognition-Attendance-Management-System

## Overview
This project implements a complete face-recognition-based attendance management system using Python. The system allows administrators to register students, capture facial images, generate facial encodings, and automatically mark attendance in real time through webcam input. The application integrates machine learning-based facial recognition (using the `face_recognition` library built on dlib), OpenCV for camera operations, Tkinter for graphical interfaces, and SQLite3 for local database storage.

---

## Features
- Student registration with name and unique student ID (UID)
- Automated face image capture through webcam
- Facial encoding generation and training
- Real-time face recognition and attendance marking
- Attendance stored with date, timestamp, and status
- GUI for viewing attendance by UID or by date
- Complete system reset functionality to support testing cycles

---

## Technologies Used
- Python  
- face_recognition (dlib-based face encoding and matching)  
- OpenCV  
- Tkinter  
- SQLite3  
- NumPy  
- os and shutil for filesystem operations  

---

## Project Folder Structure

```
FaceRecognition_AttendanceSystem/
│
├── data_acquisition.py       # GUI for adding students (run this first)
├── face_capture.py           # Captures face images for each student
├── face_train.py             # Generates and stores facial encodings (run after capturing faces)
├── mark_attendance.py        # Real-time attendance marking using webcam
├── datareport.py             # GUI for viewing attendance by UID or date
├── clear_data.py             # Deletes database, encodings, and dataset
│
├── student_data.db           # SQLite database (auto-generated)
├── encodings.pickle          # Facial encodings file (generated after training)
├── dataset/                  # Folder containing captured images for each student
│     └── UID/
│         └── img_0.jpg ... img_9.jpg
│
└── README.md                 # Project documentation
```

---

## File Descriptions

### data_acquisition.py
Tkinter GUI for entering student details (Name and UID). Saves data into the database and initiates face capture.

### face_capture.py
Captures 10 images per student using a webcam and stores them inside the dataset folder. Encodes images and stores the encoding in the database.

### face_train.py
Reads all stored images, generates facial encodings, and saves them into `encodings.pickle`.

### mark_attendance.py
Runs real-time face recognition using a webcam. Marks attendance in the database once per day for each recognized UID.

### datareport.py
GUI tool to view attendance by:
- Student UID
- Specific date

### clear_data.py
Deletes all database tables, stored encodings, and the dataset directory to reset the system.

---

## Execution Order
1. Run `data_acquisition.py` to register students and capture face images.  
2. Run `face_train.py` to generate facial encodings.  
3. Run `mark_attendance.py` to perform real-time attendance marking.  
4. Run `datareport.py` to view attendance.  
5. (Optional) Run `clear_data.py` to reset the system.

---

## How to Run

### Install Dependencies
```
pip install face_recognition opencv-python numpy tkinter
```

### Run the modules according to the execution order above.
