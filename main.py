from modules.face_database import FaceDatabase

db = FaceDatabase()
db.load_database()

print("Encodings:", len(db.encodings))
print("Users:", set(db.user_ids))
