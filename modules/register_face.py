import cv2
import face_recognition
import numpy as np
import os
from modules.config import CAMERA_INDEX, FACE_SAMPLES, DATA_PATH

def register_user(user_id):
    os.makedirs(DATA_PATH, exist_ok=True)

    cap = cv2.VideoCapture(CAMERA_INDEX, cv2.CAP_DSHOW)
    encodings  = []

    print("Face registration Started. Please look at the camera.")

    collected = 0

    while collected < FACE_SAMPLES:
        ret, frame = cap.read()
        if not ret:
            continue

        rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        face_locations = face_recognition.face_locations(rgb)

        if len(face_locations) == 1:
            face_encoding = face_recognition.face_encodings(rgb, face_locations)[0]
            encodings.append(face_encoding)
            collected += 1
            print(f"Collected sample {collected}/{FACE_SAMPLES}")
            cv2.waitKey(400)

        cv2.imshow("Register Face", frame)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()

    np.save(f"{DATA_PATH}{user_id}.npy", encodings)
    print(f" User {user_id} registered successfully")

if __name__ == "__main__":
    user_id = input("Enter User ID: ")
    register_user(user_id)