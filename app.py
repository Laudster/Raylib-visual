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

def processCode(codeblocks):
    
    setup = codeblocks.get("setup")
    setupCode = ""
     
    for codeblock in setup:
        if "Set variable" in codeblock:
            splits = codeblock.split(":")[1].split(";")
            if '"' in splits[1]:
                name = splits[0].replace(" ", "")
                setupCode += f"\n\tstrcpy({name}, {splits[1]});"
            else:
                print(f"\n\t{splits[0]} = {splits[1]};")
        
        if "Create variable" in codeblock:
            #Create variable: text;"test";"test text";
            splits = codeblock.split(":")[1].split(";")

            if splits[0].replace(" ", "") == "text":
                name = splits[1].replace(" ", "")
                value = splits[2]
                setupCode += f"\n\tchar {name[1:len(name)-1]}[20] = {value};"
            elif splits[0].replace(" ", "") == "number":
                name = splits[1].replace(" ", "")
                value = splits[2]
                setupCode += f"\n\tint {name[1:len(name)-1]} = {value[1:len(value)-1]};"
            else:
                print(splits[0].replace(" ", ""))

    render = codeblocks.get("render")
    renderCode = ""

    print(render)

    for codeblock in render:
        if "Clear Background" in codeblock:
            color = codeblock.split(":")[1].split(" ")[1]
            renderCode += f"\n\t\t\tClearBackground(GetColor(0x{color[1:len(color) - 1]}ff));"
        
        if "Draw Rectangle" in codeblock:
            #Draw Rectangle: 0 0 0 0 #000000
            splits = codeblock.split(": ")[1].split(";")
            renderCode += f"\n\t\t\tDrawRectangle({splits[0]}, {splits[1]}, {splits[2]}, {splits[3]}, GetColor(0x{splits[4][1:len(splits[4])]}ff));"
        
        if "Draw Text" in codeblock:
            #Draw Text: 0 0 0 0 #000000 
            splits = codeblock.split(": ")[1].split(";")
            renderCode += f"\n\t\t\tDrawText(\"{splits[0]}\", {splits[1]}, {splits[2]}, {splits[3]}, GetColor(0x{splits[4][1:len(splits[4])]}ff));"

    with open("outline.c", "r") as file:
        projectCode = file.read()

        projectCode = projectCode.replace("//Setup", "//Setup" + setupCode)
        projectCode = projectCode.replace("BeginDrawing();", "BeginDrawing();\n\t\t\t" + renderCode)
            
    with open("project_file.c", "w") as file:
        file.write(projectCode)
        

@socket.on("build")
def build(code):
    processCode(code)


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