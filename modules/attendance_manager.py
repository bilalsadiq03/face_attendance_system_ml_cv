import csv
import os
from datetime import datetime


ATTENDANCE_FILE = "attendance.csv"

class AttendanceManager:
    def __init__(self):
        self.file_exists = os.path.exists(ATTENDANCE_FILE)

    def mark_attendance(self, user_id):
        today = datetime.now().strftime("%Y-%m-%d")
        now = datetime.now().strftime("%H:%M:%S")

        records = self._read_records()

        user_records_today = [
            r for r in records if r["user"] == user_id and r["date"] == today
        ]

        if not user_records_today:
            # Punch In
            self._write_record(user_id, today, now, "")
            return "PUNCH_IN"

        last_record = user_records_today[-1]

        if last_record["out"] == "":
            # Punch Out
            last_record["out"] = now
            self._write_all(records)
            return "PUNCH_OUT"

        return "ALREADY_MARKED"
    
    def _read_records(self):
        if not self.file_exists:
            return []

        with open(ATTENDANCE_FILE, newline="") as f:
            return list(csv.DictReader(f))

    def _write_record(self, user, date, time_in, time_out):
        with open(ATTENDANCE_FILE, "a", newline="") as f:
            writer = csv.writer(f)
            if not self.file_exists:
                writer.writerow(["user", "date", "in", "out"])
                self.file_exists = True
            writer.writerow([user, date, time_in, time_out])

    def _write_all(self, records):
        with open(ATTENDANCE_FILE, "w", newline="") as f:
            writer = csv.DictWriter(f, fieldnames=["user", "date", "in", "out"])
            writer.writeheader()
            writer.writerows(records)