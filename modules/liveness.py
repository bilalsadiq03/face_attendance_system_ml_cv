import cv2
import dlib
import numpy as np
from scipy.spatial import distance

# Load facial landmark detector
detector = dlib.get_frontal_face_detector()
predictor = dlib.shape_predictor(
    "shape_predictor_68_face_landmarks.dat"
)

LEFT_EYE = [36, 37, 38, 39, 40, 41]
RIGHT_EYE = [42, 43, 44, 45, 46, 47]

EAR_THRESHOLD = 0.23
BLINK_FRAMES = 2


def eye_aspect_ratio(eye):
    A = distance.euclidean(eye[1], eye[5])
    B = distance.euclidean(eye[2], eye[4])
    C = distance.euclidean(eye[0], eye[3])
    return (A + B) / (2.0 * C)


class LivenessDetector:
    def __init__(self):
        self.counter = 0
        self.blinked = False

    def check_liveness(self, frame):
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        faces = detector(gray)

        for face in faces:
            shape = predictor(gray, face)
            shape = np.array([[p.x, p.y] for p in shape.parts()])

            left_eye = shape[LEFT_EYE]
            right_eye = shape[RIGHT_EYE]

            ear = (
                eye_aspect_ratio(left_eye) +
                eye_aspect_ratio(right_eye)
            ) / 2.0

            if ear < EAR_THRESHOLD:
                self.counter += 1
            else:
                if self.counter >= BLINK_FRAMES:
                    self.blinked = True
                self.counter = 0

        return self.blinked
