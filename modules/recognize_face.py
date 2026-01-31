import cv2
import face_recognition
import numpy as np
from modules.face_database import FaceDatabase
from modules.config import CAMERA_INDEX, FACE_MATCH_THRESHOLD
from modules.attendance_manager import AttendanceManager


def recognize():
    db = FaceDatabase()
    db.load_database()

    if db.is_empty():
        print(" No registered users found")
        return

    cap = cv2.VideoCapture(CAMERA_INDEX)

    print("Face Recognition Started (Press Q to exit)")

    attendance = AttendanceManager()
    marked_users = set()

    while True:
        ret, frame = cap.read()
        if not ret:
            continue

        rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        face_locations = face_recognition.face_locations(rgb)
        face_encodings = face_recognition.face_encodings(rgb, face_locations)

        for (top, right, bottom, left), face_enc in zip(face_locations, face_encodings):
            distances = face_recognition.face_distance(db.encodings, face_enc)
            min_dist = np.min(distances)
            best_match_index = np.argmin(distances)

            if min_dist < FACE_MATCH_THRESHOLD:
                name = db.user_ids[best_match_index]
                color = (0, 255, 0)
                label = f"{name} ({min_dist:.2f})"
            else:
                name = "Unknown"
                color = (0, 0, 255)
                label = "Unknown"

            cv2.rectangle(frame, (left, top), (right, bottom), color, 2)
            cv2.putText(
                frame,
                label,
                (left, top - 10),
                cv2.FONT_HERSHEY_SIMPLEX,
                0.6,
                color,
                2
            )

            if min_dist < FACE_MATCH_THRESHOLD:
                name = db.user_ids[best_match_index]

            if name not in marked_users:
                status = attendance.mark_attendance(name)
                print(f"{name}: {status}")
                marked_users.add(name)

        cv2.imshow("Face Recognition", frame)

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    recognize()
