from flask import Flask, render_template
from flask_socketio  import SocketIO
from subprocess import Popen
import os

app = Flask(__name__)
app.config["SECRET_KEY"] = "Hemmelig"

socket = SocketIO(app)

@app.route("/")
def start():
    return render_template("index.html")

@socket.on("build")
def build():
    for file in os.listdir("web-build"):
        if os.path.isfile(os.path.join("web-build", file)):
            os.remove(os.path.join("web-build", file))

    Popen(r"build.bat", shell=False)

    while not os.path.isfile("web-build/project.html"):
        pass

    socket.emit("build-finnished", "http://localhost:8000/project.html")

if __name__ == "__main__":
    socket.run(app, debug=True)