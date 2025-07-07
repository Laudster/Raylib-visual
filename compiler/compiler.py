from json import load, dumps
from os import path, mkdir, getenv, popen, remove, chdir
from zipfile import ZipFile
import requests, subprocess, winreg
from time import sleep
from sys import executable, argv, exit
from atexit import register

def uri_scheme_exists() -> bool:
    key_path = "raylibvisual\\shell\\open\\command"
    
    try:
        with winreg.OpenKey(winreg.HKEY_CLASSES_ROOT, key_path):
            return True
    except FileNotFoundError:
        return False

# Command:
# pyinstaller --onefile --upx-dir "C:/ProgramData/chocolatey/lib/upx/tools/upx-4.2.4-win64" -m .\app.manifest --uac-admin .\compiler.py

appdata = getenv("appdata")
settings_folder = path.join(appdata, "Raylib-Visual")

if path.exists(settings_folder):
    if not path.exists(path.join(settings_folder, "settings.json")):
        with open(path.join(settings_folder, "settings.json"), "w") as file:
            file.write(dumps({"setup": False}, indent=4))
else:
    mkdir(settings_folder)
    with open(path.join(settings_folder, "settings.json"), "w") as file:
        file.write(dumps({"setup": False}, indent=4))


with open(path.join(settings_folder, "settings.json"), "r") as file:
    data = load(file)

    if data["setup"] == False:
        if len(popen("python --version").read()) == 0:
            print("You need to install python for this program to work")
            print("Python can be installed from python.org")
            print("When installing python remember to select the option add to path")
            input()
            exit()
        else:
            url = "http://104.248.194.141/get-setup"

            response = requests.get(url, stream=True)

            if response.status_code == 200:
                with open("temp-setup-file.exe", "wb") as f:
                    for chunk in response.iter_content(chunk_size=8192):
                        f.write(chunk)
                
                print("Finnished downloading setup")
                subprocess.Popen(["temp-setup-file.exe"] + [path.basename(executable)], shell=True, close_fds=True)
                
                while not uri_scheme_exists():
                    sleep(0.5)

                sleep(1)

                print("Finished setup process")
                remove("temp-setup-file.exe")
            else:
                print("Server is wrong")


if len(argv) > 1:
    sessid = argv[1].split("://")[1][:-1]

    def quit(process):
        requests.delete("http://104.248.194.141/quit/" + sessid)
        process.kill()

    while True:
        response = requests.get("http://104.248.194.141/compilingcheck/" + sessid)

        if response.status_code == 200:
            if response.content.decode() == "done": break

        sleep(1)

    download_url = "http://104.248.194.141/files/" + sessid
    response = requests.get(download_url)

    chdir(path.dirname(executable))

    if response.status_code == 200:
        with open("compiled_files.zip", "wb") as f:
            f.write(response.content)

        if not path.exists("game"): mkdir("game")

        with ZipFile("compiled_files.zip", "r") as files:
            files.extractall(path="game")

        remove("compiled_files.zip")

        chdir("game")

        with open("project.js", "a") as file:
            file.write('document.getElementById("header").remove();document.getElementById("output").remove();')

        server_process = subprocess.Popen(
            ['python', '-m', 'http.server', '8001'],
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL
        )
        register(lambda: quit(server_process))
        print("Game running on http://localhost:8001/project.html")

    else:
        print("files were not found")

input("Exit program")