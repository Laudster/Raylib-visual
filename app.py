from flask import Flask, render_template
from flask_socketio  import SocketIO
from subprocess import Popen, run, CalledProcessError
from time import sleep
import os

app = Flask(__name__)
app.config["SECRET_KEY"] = "Hemmelig"

socket = SocketIO(app)

@app.route("/")
def start():
    return render_template("index.html")

def processCode(codeblock):
    if "Clear Background" in codeblock:
        color = codeblock.split(":")[1].split(" ")[1]
        c_code = f"ClearBackground(GetColor(0x{color[1:len(color)]}ff));"

        with open("outline.c", "r") as file:
            projectCode = file.read()

            projectCode = projectCode.replace("BeginDrawing();", "BeginDrawing();\n\t\t\t" + c_code)
        
        with open("project_file.c", "w") as file:
            file.write(projectCode)
        

@socket.on("build")
def build(code):
    render = code.get("render")

    if len(render) > 0:
        processCode(render[0])
    else:
        with open("outline.c", "r") as file:
            projectCode = file.read()
        
        with open("project_file.c", "w") as file:
            file.write(projectCode)


    for file in os.listdir("web-build"):
        if os.path.isfile(os.path.join("web-build", file)):
            os.remove(os.path.join("web-build", file))

    Popen(r"build.bat", shell=True)

    while not os.path.isfile("web-build/project.html"):
        sleep(1)

    socket.emit("build-finnished", "http://localhost:8000/project.html")

@socket.on("shutdown")
def shutdown(): # mildertidig chatgpt løsning, fungerer men er litt for mye for en så enkel oppgave og gir error etter å ha gjort det
    port = 8000
    try:
        # First, find the process ID using the specified port
        netstat_command = f"netstat -ano | findstr :{port}"
        result = run(netstat_command, capture_output=True, text=True, shell=True)

        if result.stdout:
            # Parse the output to get the process ID
            lines = result.stdout.strip().split("\n")
            for line in lines:
                parts = line.split()
                pid = parts[-1]  # The last column contains the PID
                # Check if the process exists before attempting to kill it
                check_command = f"tasklist /FI \"PID eq {pid}\""
                check_result = run(check_command, capture_output=True, text=True, shell=True)
                
                if pid in check_result.stdout:
                    # Kill the process using the PID
                    kill_command = f"taskkill /PID {pid} /F"
                    run(kill_command, check=True, shell=True)
                    print(f"Successfully terminated process with PID {pid} using TCP port {port}.")
                else:
                    print(f"Process with PID {pid} is already terminated.")

        else:
            print(f"No processes found using TCP port {port}.")

    except CalledProcessError as e:
        print(f"Error occurred while trying to kill processes: {e}")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")



if __name__ == "__main__":
    socket.run(app, debug=True)