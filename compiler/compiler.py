from winreg import CreateKey, SetValue, SetValueEx, REG_SZ, HKEY_CLASSES_ROOT
from json import load, dumps
from os import path, mkdir, system, getenv, popen, remove, chdir
from zipfile import ZipFile
import requests, subprocess
from time import sleep
from sys import executable, argv
from atexit import register

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
            if len(popen("choco --version").read()) == 0:
                choco_install_command = (
                    "Set-ExecutionPolicy Bypass -Scope Process -Force; "
                    "iex ((New-Object System.Net.WebClient).DownloadString('https://chocolatey.org/install.ps1'))"
                )
                system(f'powershell -NoProfile -ExecutionPolicy Bypass -Command "{choco_install_command}"')
            system(f'powershell -NoProfile -ExecutionPolicy Bypass -Command "choco install python"')
        try:
            # Define the registry key for the custom URI scheme
            scheme = "raylibvisual"

            key_path = f"{scheme}"
            
            # Open HKEY_CLASSES_ROOT
            with CreateKey(HKEY_CLASSES_ROOT, key_path) as key:
                # Set default value for the key
                SetValue(key, "", REG_SZ, f"{scheme} Protocol")
                # Create the "URL Protocol" subkey
                SetValueEx(key, "URL Protocol", 0, REG_SZ, "")
            
            # Create the shell/open/command subkeys
            with CreateKey(HKEY_CLASSES_ROOT, f"{key_path}\\shell\\open\\command") as command_key:
                # Set the default value to point to the application
                SetValue(command_key, "", REG_SZ, f'"{executable}" "%1"')

            print(f"Custom URI scheme '{scheme}' created successfully.")
        except Exception as e:
            print(f"Failed to create custom URI scheme: {e}")
        
        with open(path.join(settings_folder, "settings.json"), "w") as file:
            file.write(dumps({"setup": True}, indent=4))

if len(argv) > 1:
    sessid = argv[1].split("://")[1][:-1]

    def quit(process):
        requests.delete("http://192.168.10.183:5000/quit/" + sessid)
        process.kill()

    while True:
        response = requests.get("http://192.168.10.183:5000/compilingcheck/" + sessid)

        if response.status_code == 200:
            if response.content.decode() == "done": break

        sleep(1)

    download_url = "http://192.168.10.183:5000/files/" + sessid
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