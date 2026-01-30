import os
import numpy as np
from modules.config import DATA_PATH

class FaceDatabase:
    def __init__(self):
        self.encodings = []
        self.user_ids = []

    def load_database(self):
        if not os.path.exists(DATA_PATH):
            print("⚠ No face database found")
            return

        for file in os.listdir(DATA_PATH):
            if file.endswith(".npy"):
                user_id = file.replace(".npy", "")
                user_encs = np.load(os.path.join(DATA_PATH, file))

                for enc in user_encs:
                    self.encodings.append(enc)
                    self.user_ids.append(user_id)

        print(f"Loaded {len(set(self.user_ids))} users")

    def is_empty(self):
        return len(self.encodings) == 0
