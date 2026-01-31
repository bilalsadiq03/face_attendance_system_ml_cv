import cv2


def normalize_lightening(frame):
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    clahe = cv2.createCLAHE(clipLimit=2.0, tileGridSize=(8, 8))
    enhanced = clahe.apply(gray)

    enhanced_rgb = cv2.cvtColor(enhanced, cv2.COLOR_GRAY2BGR)

    return enhanced_rgb