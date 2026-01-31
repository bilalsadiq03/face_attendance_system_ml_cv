from flask import Flask, render_template, redirect, request
import threading
from modules.register_face import register_user
from modules.recognize_face import recognize

app = Flask(__name__)

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/register", methods=["POST"])
def register():
    user_id = request.form["user_id"]
    threading.Thread(target=register_user, args=(user_id,)).start()
    return redirect("/")

@app.route("/start-attendance")
def start_attendance():
    threading.Thread(target=recognize).start()
    return redirect("/")

if __name__ == "__main__":
    app.run(debug=True)
