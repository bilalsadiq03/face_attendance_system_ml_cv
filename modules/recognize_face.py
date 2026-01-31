import cv2
import numpy as np
import face_recognition

from modules.face_database import FaceDatabase
from modules.attendance_manager import AttendanceManager
from modules.liveness import LivenessDetector
from modules.preprocess import normalize_lightening
from modules.config import CAMERA_INDEX, FACE_MATCH_THRESHOLD


def recognize():
    db = FaceDatabase()
    db.load_database()

    if db.is_empty():
        print("No registered users found")
        return

    attendance = AttendanceManager()
    liveness = LivenessDetector()
    marked_users = set()

    cap = cv2.VideoCapture(CAMERA_INDEX, cv2.CAP_DSHOW)
    print("Face Recognition Started (Press Q to exit)")

    while True:
        ret, frame = cap.read()
        if not ret:
            continue

        is_live = liveness.check_liveness(frame)

        rgb = normalize_lightening(frame)

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

                if not is_live:
                    cv2.putText(
                        frame,
                        "Blink to verify liveness",
                        (20, 40),
                        cv2.FONT_HERSHEY_SIMPLEX,
                        0.8,
                        (0, 0, 255),
                        2
                    )
                else:
                    if name not in marked_users:
                        status = attendance.mark_attendance(name)
                        print(f"{name}: {status}")
                        marked_users.add(name)
                        liveness.reset()

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

        cv2.imshow("Face Authentication Attendance", frame)

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()


if __name__ == "__main__":
    recognize()
