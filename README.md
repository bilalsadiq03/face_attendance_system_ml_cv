# Face Authentication Attendance System

A real-time **Face Authentication based Attendance System** that uses computer vision and machine learning to register users, authenticate them using a live camera feed, prevent basic spoofing attempts, and mark **Punch-In / Punch-Out** attendance.

This project is designed as a **practical AI/ML internship assignment**, focusing on real-world constraints, modular design, and explainable ML decisions.

---

## Features

- Real-time face registration using webcam  
- Face authentication using pretrained face embeddings  
- Punch-In / Punch-Out attendance system  
- Works with live camera input  
- Handles varying lighting conditions  
- Basic spoof prevention using blink-based liveness detection  
- Web-based UI using Flask  
- Modular and extensible project structure  

---

##  System Architecture

```text
Camera Input
   ↓
Lighting Normalization (CLAHE)
   ↓
Face Detection & Encoding
   ↓
Face Matching (Euclidean Distance)
   ↓
Liveness Verification (Eye Blink)
   ↓
Attendance Logic (Punch-In / Punch-Out)
   ↓
CSV Storage
```

## Model and Approach

### Face Recognition
- Uses a pretrained face embedding model (128-D vectors) via face_recognition
- Based on dlib / ResNet architecture
- No custom classifier training required
- Authentication performed using Euclidean distance thresholding

### Why embeddings instead of a classifier?
- New users can be added without retraining
- Faster and more scalable
- Industry-standard approach for face authentication systems


## Spoof Prevention (Liveness Detection)

- Implemented eye blink detection using Eye Aspect Ratio (EAR)
- Attendance is marked only after a blink is detected
- Prevents static photo-based spoofing

## Project Structure
```bash
face_attendance_system/
│
├── app.py
├── main.py
├── requirements.txt
├── README.md
├── .gitignore
│
├── templates/
│   └── index.html
│
├── modules/
│   ├── config.py
│   ├── camera_test.py
│   ├── register_face.py
│   ├── face_database.py
│   ├── recognize_face.py
│   ├── attendance_manager.py
│   ├── preprocess.py
│   └── liveness.py
│
└── data/
    └── faces/
```

## Setup Instructions

### 1. Clone the Repository
```bash
git clone https://github.com/bilalsadiq03/face_attendance_system_ml_cv
cd face_attendance_system_ml_cv
```

### 2. Create Virtual Environment (Recommended)
```bash 
python -m venv .venv
```
Activate:

Windows
```bash
.venv\Scripts\activate
```

Linux/MacOS
```bash
source .venv/bin/activate
```

### 3. Install Dependencies
```bash
pip install -r requirements.txt
```

### 4. Download Required Model File
```bash
shape_predictor_68_face_landmarks.dat
```

Source:
```bash
https://github.com/davisking/dlib-models
```

## How to Run the Project

### Option 1: Web UI (Recommended)
```bash
python app.py
```
Open in browser:
```bash
http://127.0.0.1:5000
```

### Option 2: CLI Mode (Without UI)
Register User:
```bash
python modules/register_face.py
```
Start Attendance:
python main.py
```

## Attendance Storage
Attendance is stored locally in attendance.csv file.


## Future Improvements
- CNN-based advanced anti-spoofing
- Database integration (PostgreSQL / MongoDB)
- WebRTC-based remote camera streaming
- Role-based user management
- Shift and break tracking

