from flask import Flask, render_template
from flask_socketio  import SocketIO
from subprocess import Popen, run, CalledProcessError
from time import sleep
from processors import setVariable
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

    print(codeblocks)

    variables = {"defaultColour": "color", "FPS": "number", "title": "text"}

    isInIfStatement = False

    beguneIf = False
     
    for codeblock in setup:
        
        if not "tab" in codeblock and isInIfStatement == True and beguneIf == True:
            isInIfStatement = False
            inputCode += "}"
            print(codeblock)

        if "Set variable" in codeblock:
            if isInIfStatement: beguneIf = True

        setupCode = setVariable(setupCode, isInIfStatement, variables, codeblock)
        
        if "Create variable" in codeblock:
            #Create variable: text;"test";"test text";
            splits = codeblock.split(":")[1].split(";")

            if splits[0].replace(" ", "") == "text":
                name = splits[1].replace(" ", "")
                value = splits[2]
                setupCode += f"\n\tchar {name}[20] = \"{value}\";"

                variables[name] = "text"
            
            elif splits[0].replace(" ", "") == "color":
                name = splits[1].replace(" ", "")
                value = splits[2]
                setupCode += f"\n\tColor {name} = GetColor(0x{value[1: len(value)]}ff);"

                variables[name] = "color"
            elif splits[0].replace(" ", "") == "number":
                name = splits[1].replace(" ", "")
                value = splits[2]
                setupCode += f"\n\tint {name} = {value};"

                variables[name] = "number"
            else:
                print(splits[0].replace(" ", ""))

        if "If" in codeblock:
            isInIfStatement = True
            beguneIf = True
            if "IsKeyDown" in codeblock:
                key = ""

                if "Space" in codeblock: key = "KEY_SPACE"
                if "Arrow Down" in codeblock: key = "KEY_DOWN"
                if "Arrow Up" in codeblock: key = "KEY_UP"
                if "Arrow Left" in codeblock: key = "KEY_LEFT"
                if "Arrow Right" in codeblock: key = "KEY_RIGHT"

                setupCode += "\n\t\tif (IsKeyDown("+ key + ")){"

            if "==" in codeblock:
                #'If: Not 0;== 1;
                if "Not" in codeblock:
                    splits = codeblock[codeblock.index("t") + 2: len(codeblock)].split(";")
                    print(splits)
                    value = ""
                    for i in range(1, len(splits)):
                        value += splits[i].replace(" ", "").replace("Or", "||").replace("And", "&&").replace("Not", "!")
                    if "Else" in codeblock:
                        setupCode += "\n\t\telse if (!" + splits[0].replace(" ", "") + value + "){"
                    else:
                        setupCode += "\n\t\tif (!" + splits[0].replace(" ", "") + value + "){"
                else:
                    splits = codeblock.split(":")[1].split(";")
                    if splits[0].replace(" ", "").isnumeric() or splits[0].replace(" ", "") in variables and variables[splits[0].replace(" ", "")] == "number":
                        value = ""
                        for i in range(1, len(splits)):
                            value += splits[i].replace(" ", "").replace("Or", "||").replace("And", "&&")
                        if "Else" in codeblock:
                            setupCode += "\n\t\telse if (" + splits[0].replace(" ", "") + value + "){"
                        else:
                            setupCode += "\n\t\tif (" + splits[0].replace(" ", "") + value + "){"

        elif "Else" in codeblock:
            isInIfStatement = True
            beguneIf = True
            setupCode += "\n\t\telse{"

    
    if isInIfStatement == True: setupCode += "}"

    input = codeblocks.get("input")
    inputCode = ""

    isInIfStatement = False

    beguneIf = False

    for codeblock in input:
        if not "tab" in codeblock and isInIfStatement == True and beguneIf == True:
            isInIfStatement = False
            inputCode += "}"
            print(codeblock)
        
        if "Set variable" in codeblock:
            if isInIfStatement: beguneIf = True
    
        inputCode = setVariable(inputCode, isInIfStatement, variables, codeblock)

        if "If" in codeblock:
            isInIfStatement = True
            beguneIf = True
            if "IsKeyDown" in codeblock:
                key = ""

                if "Space" in codeblock: key = "KEY_SPACE"
                if "Arrow Down" in codeblock: key = "KEY_DOWN"
                if "Arrow Up" in codeblock: key = "KEY_UP"
                if "Arrow Left" in codeblock: key = "KEY_LEFT"
                if "Arrow Right" in codeblock: key = "KEY_RIGHT"

                inputCode += "\n\t\tif (IsKeyDown("+ key + ")){"
            
            if "IsMouseDown" in codeblock:
                if "Left" in codeblock: key = "MOUSE_BUTTON_LEFT"
                if "Right" in codeblock: key = "MOUSE_BUTTON_RIGHT"
                if "Middle" in codeblock: key = "MOUSE_BUTTON_MIDDLE"

                inputCode += "\n\t\tif (IsMouseButtonPressed("+ key + ")){"

            if "==" in codeblock:
                #'If: Not 0;== 1;
                if "Not" in codeblock:
                    splits = codeblock[codeblock.index("t") + 2: len(codeblock)].split(";")
                    print(splits)
                    value = ""
                    for i in range(1, len(splits)):
                        value += splits[i].replace(" ", "").replace("Or", "||").replace("And", "&&").replace("Not", "!")
                    if "Else" in codeblock:
                        inputCode += "\n\t\telse if (!" + splits[0].replace(" ", "") + value + "){"
                    else:
                        inputCode += "\n\t\tif (!" + splits[0].replace(" ", "") + value + "){"
                else:
                    splits = codeblock.split(":")[1].split(";")
                    if splits[0].replace(" ", "").isnumeric() or splits[0].replace(" ", "") in variables and variables[splits[0].replace(" ", "")] == "number":
                        value = ""
                        for i in range(1, len(splits)):
                            value += splits[i].replace(" ", "").replace("Or", "||").replace("And", "&&")
                        if "Else" in codeblock:
                            inputCode += "\n\t\telse if (" + splits[0].replace(" ", "") + value + "){"
                        else:
                            inputCode += "\n\t\tif (" + splits[0].replace(" ", "") + value + "){"

        elif "Else" in codeblock:
            isInIfStatement = True
            beguneIf = True
            inputCode += "\n\t\telse{"

    
    if isInIfStatement == True:
        print("end")
        inputCode += "}"

    update = codeblocks.get("update")
    updateCode = ""
    isInIfStatement = False

    beguneIf = False

    for codeblock in update:
        if not "tab" in codeblock and isInIfStatement == True and beguneIf == True:
            isInIfStatement = False
            updateCode += "}"
            print(codeblock)

        if "Set variable" in codeblock:
            if isInIfStatement: beguneIf = True
    
        updateCode = setVariable(updateCode, isInIfStatement, variables, codeblock)

        if "If" in codeblock:
            isInIfStatement = True
            beguneIf = True
            if "IsKeyDown" in codeblock:
                key = ""

                if "Space" in codeblock: key = "KEY_SPACE"
                if "Arrow Down" in codeblock: key = "KEY_DOWN"
                if "Arrow Up" in codeblock: key = "KEY_UP"
                if "Arrow Left" in codeblock: key = "KEY_LEFT"
                if "Arrow Right" in codeblock: key = "KEY_RIGHT"

                updateCode += "\n\t\tif (IsKeyDown("+ key + ")){"
            
            if "IsMouseDown" in codeblock:
                if "Left" in codeblock: key = "MOUSE_BUTTON_LEFT"

                updateCode += "\n\t\tif (IsMouseButtonPressed("+ key + ")){"

            if "==" in codeblock:
                #'If: Not 0;== 1;
                if "Not" in codeblock:
                    splits = codeblock[codeblock.index("t") + 2: len(codeblock)].split(";")
                    print(splits)
                    value = ""
                    for i in range(1, len(splits)):
                        value += splits[i].replace(" ", "").replace("Or", "||").replace("And", "&&").replace("Not", "!")
                    if "Else" in codeblock:
                        updateCode += "\n\t\telse if (!" + splits[0].replace(" ", "") + value + "){"
                    else:
                        updateCode += "\n\t\tif (!" + splits[0].replace(" ", "") + value + "){"
                else:
                    splits = codeblock.split(":")[1].split(";")
                    if splits[0].replace(" ", "").isnumeric() or splits[0].replace(" ", "") in variables and variables[splits[0].replace(" ", "")] == "number":
                        value = ""
                        for i in range(1, len(splits)):
                            value += splits[i].replace(" ", "").replace("Or", "||").replace("And", "&&")
                        if "Else" in codeblock:
                            updateCode += "\n\t\telse if (" + splits[0].replace(" ", "") + value + "){"
                        else:
                            updateCode += "\n\t\tif (" + splits[0].replace(" ", "") + value + "){"

        elif "Else" in codeblock:
            isInIfStatement = True
            beguneIf = True
            updateCode += "\n\t\telse{"

    
    if isInIfStatement == True: updateCode += "}"
    
    render = codeblocks.get("render")
    renderCode = ""

    isInIfStatement = False
    beguneIf = False

    for codeblock in render:
        if not "tab" in codeblock and isInIfStatement == True and beguneIf == True:
            isInIfStatement = False
            inputCode += "}"
            print(codeblock)
        
        if "Set variable" in codeblock:
            if isInIfStatement: beguneIf = True

        renderCode = setVariable(renderCode, isInIfStatement, variables, codeblock)

        if "Draw Rectangle" in codeblock:
            splits = codeblock.split(": ")[1].split(";")
            if isInIfStatement == True:
                renderCode += f"DrawRectangle({splits[0]}, {splits[1]}, {splits[2]}, {splits[3]}, GetColor(0x{splits[4][1:len(splits[4])]}ff));"
            else:
                renderCode += f"\n\t\t\tDrawRectangle({splits[0]}, {splits[1]}, {splits[2]}, {splits[3]}, GetColor(0x{splits[4][1:len(splits[4])]}ff));"
        
        if "Draw Circle" in codeblock:
            splits = codeblock.split(": ")[1].split(";")
            if isInIfStatement == True:
                renderCode += f"DrawCircle({splits[0]}, {splits[1]}, {splits[2]}, GetColor(0x{splits[4][1:len(splits[4])]}ff));"
            else:
                renderCode += f"\n\t\t\tDrawCircle({splits[0]}, {splits[1]}, {splits[2]}, GetColor(0x{splits[4][1:len(splits[4])]}ff));"
        
        if "Draw Text" in codeblock:
            #Draw Text: 0 0 0 0 #000000 
            splits = codeblock.split(": ")[1].split(";")
            value = splits[0]
            if splits[0] in variables:
                if variables[splits[0]] == "number":
                    value = f'TextFormat("%i", {splits[0]})'
            else:
                value = f'"{value}"'

            if isInIfStatement == True:
                renderCode += f"DrawText({value}, {splits[1]}, {splits[2]}, {splits[3]}, GetColor(0x{splits[4][1:len(splits[4])]}ff));"
            else:
                renderCode += f"\n\t\t\tDrawText({value}, {splits[1]}, {splits[2]}, {splits[3]}, GetColor(0x{splits[4][1:len(splits[4])]}ff));"
        
        if "If" in codeblock:
            isInIfStatement = True
            beguneIf = True
            if "IsKeyDown" in codeblock:
                key = ""

                if "Space" in codeblock: key = "KEY_SPACE"
                if "Arrow Down" in codeblock: key = "KEY_DOWN"
                if "Arrow Up" in codeblock: key = "KEY_UP"
                if "Arrow Left" in codeblock: key = "KEY_LEFT"
                if "Arrow Right" in codeblock: key = "KEY_RIGHT"

                renderCode += "\n\t\tif (IsKeyDown("+ key + ")){"

            if "==" in codeblock:
                #'If: Not 0;== 1;
                if "Not" in codeblock:
                    splits = codeblock[codeblock.index("t") + 2: len(codeblock)].split(";")
                    print(splits)
                    value = ""
                    for i in range(1, len(splits)):
                        value += splits[i].replace(" ", "").replace("Or", "||").replace("And", "&&").replace("Not", "!")
                    if "Else" in codeblock:
                        renderCode += "\n\t\telse if (!" + splits[0].replace(" ", "") + value + "){"
                    else:
                        renderCode += "\n\t\tif (!" + splits[0].replace(" ", "") + value + "){"
                else:
                    splits = codeblock.split(":")[1].split(";")
                    if splits[0].replace(" ", "").isnumeric() or splits[0].replace(" ", "") in variables and variables[splits[0].replace(" ", "")] == "number":
                        value = ""
                        for i in range(1, len(splits)):
                            value += splits[i].replace(" ", "").replace("Or", "||").replace("And", "&&")
                        if "Else" in codeblock:
                            renderCode += "\n\t\telse if (" + splits[0].replace(" ", "") + value + "){"
                        else:
                            renderCode += "\n\t\tif (" + splits[0].replace(" ", "") + value + "){"

        elif "Else" in codeblock:
            isInIfStatement = True
            beguneIf = True
            renderCode += "\n\t\telse{"

    if isInIfStatement == True: renderCode += "}"


    with open("outline.c", "r") as file:
        projectCode = file.read()

        projectCode = projectCode.replace("//Setup", "//Setup" + setupCode)
        projectCode = projectCode.replace("//Input", "//Input" + inputCode)
        projectCode = projectCode.replace("//Update", "//Update" + updateCode)
        projectCode = projectCode.replace("ClearBackground(defaultColour);", "ClearBackground(defaultColour);\t\t\t" + renderCode)
            
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
def shutdown(): # chatgpt løsning, fungerer men er litt for mye for en så enkel task og gir error etter å ha blitt ferdig
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