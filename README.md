# Face-Recognition-Attendance-Management-System

Overview

This project implements a complete face-recognition-based attendance management system using Python. The system allows administrators to register students, capture facial images, generate facial encodings, and automatically mark attendance in real time through webcam input. The application integrates machine learning-based facial recognition (using the face_recognition library built on dlib), OpenCV for camera operations, Tkinter for graphical interfaces, and SQLite3 for local database storage.

Features

Student registration with name and unique student ID (UID)

Automated face image capture through webcam

Facial encoding generation and training

Real-time face recognition and attendance marking

Attendance stored with date, timestamp, and status

GUI for viewing attendance by UID or by date

Complete system reset functionality to support testing cycles

Technologies Used

Python

face_recognition (dlib-based face encoding and matching)

OpenCV

Tkinter

SQLite3

NumPy

os and shutil for filesystem operations

Project Folder Structure
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

File Descriptions
data_acquisition.py

A Tkinter-based GUI that accepts student details (Name and UID), validates input, stores data in the SQLite database, and triggers the face-capture process.

face_capture.py

Captures 10 facial images per registered student using the webcam and stores them in the dataset directory. Each image is encoded and stored in the database.

face_train.py

Iterates through the dataset directory, computes facial encodings for all collected images, and saves them into encodings.pickle. This file is required for recognition.

mark_attendance.py

Performs real-time face detection and recognition using the webcam. When a known face is identified, attendance is marked in the database with date and timestamp. Each student is recorded only once per day.

datareport.py

A Tkinter-based application for viewing attendance. Provides:

Attendance lookup by UID

Day-wise attendance sheet

clear_data.py

Clears the database tables, deletes the encodings file, and removes all dataset images. Useful for resetting the system during testing.

Execution Order

Run data_acquisition.py to register students and capture face images.

Run face_train.py to generate encodings.

Run mark_attendance.py to start real-time attendance marking.

Run datareport.py to view attendance records.

Optionally, use clear_data.py to reset all system data.

How to Run

Install required Python libraries:

pip install face_recognition opencv-python numpy


Run the system modules as per the execution order above.
