from modules.face_database import FaceDatabase
from modules.recognize_face import recognize


db = FaceDatabase()
db.load_database()

print("Encodings:", len(db.encodings))
print("Users:", set(db.user_ids))

if __name__ == "__main__":
    recognize()