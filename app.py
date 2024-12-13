from flask import Flask, render_template, send_file, request
from flask_socketio  import SocketIO
from subprocess import Popen, run, CalledProcessError
from time import sleep
from shutil import rmtree
from zipfile import ZipFile
from processors import setVariable
import os, io

app = Flask(__name__)
app.config["SECRET_KEY"] = "Hemmelig"

socket = SocketIO(app)

@app.route("/")
def start():
    return render_template("index.html")
 
@app.route("/files")
def file_download():
    compiled_files = "web-build"

    if not os.path.exists(compiled_files):
        return "error"
    
    zip_buffer = io.BytesIO()
    with ZipFile(zip_buffer, "w") as zip_file:
        for file_name in os.listdir(compiled_files):
            file_path = os.path.join(compiled_files, file_name)
            if os.path.isfile(file_path):
                zip_file.write(file_path, file_name)
    
    zip_buffer.seek(0)

    return send_file(zip_buffer, mimetype="application/zip", as_attachment=True, download_name="compiled_files.zip")

def processCode(codeblocks, folder):
    
    setup = codeblocks.get("setup")
    setupCode = ""

    print(codeblocks)
    for code in codeblocks:
        if len(codeblocks.get(code)) > 0:
            actualCode = codeblocks.get(code)
            for block in actualCode:
                if "RND" in block:
                    indeks = block.index("RND")
                    minnum = ""
                    
                    i = indeks - 2
                    while block[i] != " " and block[i] != ";":
                        minnum += block[i]
                        i -= 1
                    
                    maxnum = ""
                    
                    i = indeks + 4
                    while block[i] != ";":
                        maxnum += block[i]
                        i += 1
                    
                    print(block)

                    codeblocks.get(code)[codeblocks.get(code).index(block)] = block[0:indeks-1 - len(minnum)] + f"randint({minnum[::-1]}, {maxnum});" + block[indeks + 8: len(block)]

    variables = {"defaultColour": "color", "FPS": "number", "title": "text"}

    isInIfStatement = False

    beguneIf = False
     
    for codeblock in setup:
        
        if not "tab" in codeblock and isInIfStatement == True and beguneIf == True:
            isInIfStatement = False
            inputCode += "}"
            print(codeblock)

        setupCode, isInIfStatement = setVariable(setupCode, isInIfStatement, variables, codeblock, 1)
        
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

            if "==" in codeblock or "<" in codeblock or ">" in codeblock or "!=" in codeblock:
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
        
        if "While" in codeblock:
            isInIfStatement = True
            beguneIf = True

            if "==" in codeblock or "<" in codeblock or ">" in codeblock or "!=" in codeblock:
                if "Not" in codeblock:
                    splits = codeblock[codeblock.index("t") + 2: len(codeblock)].split(";")
                    print(splits)
                    value = ""
                    for i in range(1, len(splits)):
                        value += splits[i].replace(" ", "").replace("Or", "||").replace("And", "&&").replace("Not", "!")
                    
                    setupCode += "\n\t\twhile (!" + splits[0].replace(" ", "") + value + "){"
                else:
                    splits = codeblock.split(":")[1].split(";")
                    if splits[0].replace(" ", "").isnumeric() or splits[0].replace(" ", "") in variables and variables[splits[0].replace(" ", "")] == "number":
                        value = ""
                        for i in range(1, len(splits)):
                            value += splits[i].replace(" ", "").replace("Or", "||").replace("And", "&&")
                        
                        setupCode += "\n\t\twhile (" + splits[0].replace(" ", "") + value + "){"

    
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
    
        inputCode, isInIfStatement = setVariable(inputCode, isInIfStatement, variables, codeblock, 2)

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

            if "==" in codeblock or "<" in codeblock or ">" in codeblock or "!=" in codeblock:
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
        
        if "While" in codeblock:
            isInIfStatement = True
            beguneIf = True

            if "==" in codeblock or "<" in codeblock or ">" in codeblock or "!=" in codeblock:
                if "Not" in codeblock:
                    splits = codeblock[codeblock.index("t") + 2: len(codeblock)].split(";")
                    print(splits)
                    value = ""
                    for i in range(1, len(splits)):
                        value += splits[i].replace(" ", "").replace("Or", "||").replace("And", "&&").replace("Not", "!")
                    
                    inputCode += "\n\t\twhile (!" + splits[0].replace(" ", "") + value + "){"
                else:
                    splits = codeblock.split(":")[1].split(";")
                    if splits[0].replace(" ", "").isnumeric() or splits[0].replace(" ", "") in variables and variables[splits[0].replace(" ", "")] == "number":
                        value = ""
                        for i in range(1, len(splits)):
                            value += splits[i].replace(" ", "").replace("Or", "||").replace("And", "&&")
                        
                        inputCode += "\n\t\twhile (" + splits[0].replace(" ", "") + value + "){"

    
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
    
        updateCode, isInIfStatement = setVariable(updateCode, isInIfStatement, variables, codeblock, 2)

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

            if "==" in codeblock or "<" in codeblock or ">" in codeblock or "!=" in codeblock:
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
        
        if "While" in codeblock:
            isInIfStatement = True
            beguneIf = True

            if "==" in codeblock or "<" in codeblock or ">" in codeblock or "!=" in codeblock:
                if "Not" in codeblock:
                    splits = codeblock[codeblock.index("t") + 2: len(codeblock)].split(";")
                    print(splits)
                    value = ""
                    for i in range(1, len(splits)):
                        value += splits[i].replace(" ", "").replace("Or", "||").replace("And", "&&").replace("Not", "!")
                    
                    updateCode += "\n\t\twhile (!" + splits[0].replace(" ", "") + value + "){"
                else:
                    splits = codeblock.split(":")[1].split(";")
                    if splits[0].replace(" ", "").isnumeric() or splits[0].replace(" ", "") in variables and variables[splits[0].replace(" ", "")] == "number":
                        value = ""
                        for i in range(1, len(splits)):
                            value += splits[i].replace(" ", "").replace("Or", "||").replace("And", "&&")
                        
                        updateCode += "\n\t\twhile (" + splits[0].replace(" ", "") + value + "){"

    
    if isInIfStatement == True: updateCode += "}"
    
    render = codeblocks.get("render")
    renderCode = ""

    isInIfStatement = False
    beguneIf = False

    for codeblock in render:
        if not "tab" in codeblock and isInIfStatement == True and beguneIf == True:
            isInIfStatement = False
            renderCode += "}"
            print(codeblock)

        renderCode, isInIfStatement = setVariable(renderCode, isInIfStatement, variables, codeblock, 3)

        if "Draw Rectangle" in codeblock:
            print(codeblock)
            splits = codeblock.split(": ")[1].split(";")
            value = []
            argument = ""

            for v in splits:
                if len(v) > 0:
                    if v[0].isnumeric():
                        if argument == "": value.append(v)
                        else:
                            argument += v
                            value.append(argument)
                    elif v[0] == "#" or not v[0] in "+-*/": value.append(v)
                    else:
                        if argument == "":
                            if len(value) > 0:
                                value[len(value) - 1] += v
                            else:
                                value.append(v)
                        else: argument += v
            
            print(value)

            if isInIfStatement == True:
                renderCode += f"DrawRectangle({value[0]}, {value[1]}, {value[2]}, {value[3]}, GetColor(0x{value[4][1:len(value[4])]}ff));"
            else:
                renderCode += f"\n\t\t\tDrawRectangle({value[0]}, {value[1]}, {value[2]}, {value[3]}, GetColor(0x{value[4][1:len(value[4])]}ff));"
        
        if "Draw Circle" in codeblock:
            splits = codeblock.split(": ")[1].split(";")
            value = []
            argument = ""

            for v in splits:
                if len(v) > 0:
                    if v[0].isnumeric():
                        if argument == "": value.append(v)
                        else:
                            argument += v
                            value.append(argument)
                    elif v[0] == "#" or not v[0] in "+-*/": value.append(v)
                    else:
                        if argument == "":
                            if len(value) > 0:
                                value[len(value) - 1] += v
                            else:
                                value.append(v)
                        else: argument += v
            
            if isInIfStatement == True:
                renderCode += f"DrawCircle({splits[0]}, {splits[1]}, {splits[2]}, GetColor(0x{splits[4][1:len(splits[4])]}ff));"
            else:
                renderCode += f"\n\t\t\tDrawCircle({splits[0]}, {splits[1]}, {splits[2]}, GetColor(0x{splits[4][1:len(splits[4])]}ff));"
        
        if "Draw Text" in codeblock:
            #Draw Text: 0 0 0 0 #000000 
            splits = codeblock.split(": ")[1].split(";")
            value = splits[0]
            value = []
            argument = ""

            for v in splits:
                if len(v) > 0:
                    if v[0].isnumeric():
                        if argument == "": value.append(v)
                        else:
                            argument += v
                            value.append(argument)
                    elif v[0] == "#" or not v[0] in "+-*/": value.append(v)
                    else:
                        if argument == "":
                            if len(value) > 0:
                                value[len(value) - 1] += v
                            else:
                                value.append(v)
                        else: argument += v

            if splits[0] in variables:
                if variables[splits[0]] == "number":
                    value = f'TextFormat("%i", {splits[0]})'
            else:
                value = f'"{value}"'

            if isInIfStatement == True:
                renderCode += f"DrawText({value}, {splits[1]}, {splits[2]}, {splits[3]}, GetColor(0x{splits[4][1:len(splits[4])]}ff));"
            else:
                renderCode += f"\n\t\t\tDrawText({value}, {splits[1]}, {splits[2]}, {splits[3]}, GetColor(0x{splits[4][1:len(splits[4])]}ff));"
        
        if "Create variable" in codeblock:
            #Create variable: text;"test";"test text";
            splits = codeblock.split(":")[1].split(";")

            if splits[0].replace(" ", "") == "text":
                name = splits[1].replace(" ", "")
                value = ""
                for i in range(2, len(splits)):
                    value += splits[i]
                renderCode += f"\n\t\t\tchar {name}[20] = \"{value}\";"

                variables[name] = "text"
            
            elif splits[0].replace(" ", "") == "color":
                name = splits[1].replace(" ", "")
                value = ""
                for i in range(2, len(splits)):
                    value += splits[i]
                renderCode += f"\n\t\t\tColor {name} = GetColor(0x{value[1: len(value)]}ff);"

                variables[name] = "color"
            elif splits[0].replace(" ", "") == "number":
                name = splits[1].replace(" ", "")
                value = ""
                for i in range(2, len(splits)):
                    value += splits[i]
                renderCode += f"\n\t\t\tint {name} = {value};"

                variables[name] = "number"
            else:
                print(splits[0].replace(" ", ""))

        if "Loop" in codeblock:
            isInIfStatement = True
            beguneIf = True

            renderCode += "\n\t\t\tfor (int thisvariablewillnevereverbeusedbyuser = 0; thisvariablewillnevereverbeusedbyuser <" + codeblock.split(":")[1].replace(" ", "") + " thisvariablewillnevereverbeusedbyuser++){"

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

            if "==" in codeblock or "<" in codeblock or ">" in codeblock or "!=" in codeblock:
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
        
        if "While" in codeblock:
            isInIfStatement = True
            beguneIf = True

            if "==" in codeblock or "<" in codeblock or ">" in codeblock or "!=" in codeblock:
                if "Not" in codeblock:
                    splits = codeblock[codeblock.index("t") + 2: len(codeblock)].split(";")
                    print(splits)
                    value = ""
                    for i in range(1, len(splits)):
                        value += splits[i].replace(" ", "").replace("Or", "||").replace("And", "&&").replace("Not", "!")
                    
                    renderCode += "\n\t\twhile (!" + splits[0].replace(" ", "") + value + "){"
                else:
                    splits = codeblock.split(":")[1].split(";")
                    if splits[0].replace(" ", "").isnumeric() or splits[0].replace(" ", "") in variables and variables[splits[0].replace(" ", "")] == "number":
                        value = ""
                        for i in range(1, len(splits)):
                            value += splits[i].replace(" ", "").replace("Or", "||").replace("And", "&&")
                        
                        renderCode += "\n\t\twhile (" + splits[0].replace(" ", "") + value + "){"

    if isInIfStatement == True: renderCode += "}"


    with open("outline.c", "r") as file:
        projectCode = file.read()

        projectCode = projectCode.replace("//Setup", "//Setup" + setupCode)
        projectCode = projectCode.replace("//Input", "//Input" + inputCode)
        projectCode = projectCode.replace("//Update", "//Update" + updateCode)
        projectCode = projectCode.replace("ClearBackground(defaultColour);", "ClearBackground(defaultColour);\t\t\t" + renderCode)
            
    with open(f"{folder}/project_file.c", "w") as file:
        file.write(projectCode)
        

@socket.on("build")
def build(code):
    if not os.path.exists(request.sid):
        os.mkdir(request.sid)
        os.mkdir(f"{request.sid}/web-build")

    processCode(code, request.sid)

    for file in os.listdir(f"{request.sid}/web-build"):
        if os.path.isfile(os.path.join(f"{request.sid}/web-build", file)):
            os.remove(os.path.join(f"{request.sid}/web-build", file))

    Popen(r"build.bat " + str(request.sid), shell=True)

    while not os.path.isfile(f"{request.sid}/web-build/project.html"):
        sleep(1)

    socket.emit("build-finnished", "http://localhost:8000/project.html", to=request.sid)

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

@socket.on("disconnect")
def disconnect():
    if os.path.exists(request.sid):
        rmtree(request.sid)



if __name__ == "__main__":
    socket.run(app, debug=True)