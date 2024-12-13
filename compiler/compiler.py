import os, json, requests, winreg
from zipfile import ZipFile
from sys import executable

appdata = os.getenv("appdata")
settings_folder = os.path.join(appdata, "Raylib-Visual")

if os.path.exists(settings_folder):
    if not os.path.exists(os.path.join(settings_folder, "settings.json")):
        with open(os.path.join(settings_folder, "settings.json"), "w") as file:
            file.write(json.dumps({"setup": False}, indent=4))
else:
    os.mkdir(settings_folder)
    with open(os.path.join(settings_folder, "settings.json"), "w") as file:
        file.write(json.dumps({"setup": False}, indent=4))


with open(os.path.join(settings_folder, "settings.json"), "r") as file:
    data = json.load(file)

    if data["setup"] == False:
        if len(os.popen("python --version").read()) == 0:
            if len(os.popen("choco --version").read()) == 0:
                choco_install_command = (
                    "Set-ExecutionPolicy Bypass -Scope Process -Force; "
                    "iex ((New-Object System.Net.WebClient).DownloadString('https://chocolatey.org/install.ps1'))"
                )
                os.system(f'powershell -NoProfile -ExecutionPolicy Bypass -Command "{choco_install_command}"')
            os.system(f'powershell -NoProfile -ExecutionPolicy Bypass -Command "choco install python"')
            try:
                # Define the registry key for the custom URI scheme
                scheme = "raylibvisual"

                key_path = f"{scheme}"
                
                # Open HKEY_CLASSES_ROOT
                with winreg.CreateKey(winreg.HKEY_CLASSES_ROOT, key_path) as key:
                    # Set default value for the key
                    winreg.SetValue(key, "", winreg.REG_SZ, f"{scheme} Protocol")
                    # Create the "URL Protocol" subkey
                    winreg.SetValueEx(key, "URL Protocol", 0, winreg.REG_SZ, "")
                
                # Create the shell/open/command subkeys
                with winreg.CreateKey(winreg.HKEY_CLASSES_ROOT, f"{key_path}\\shell\\open\\command") as command_key:
                    # Set the default value to point to the application
                    winreg.SetValue(command_key, "", winreg.REG_SZ, f'"{executable}" "%1"')

                print(f"Custom URI scheme '{scheme}' created successfully.")
            except Exception as e:
                print(f"Failed to create custom URI scheme: {e}")

download_url = "http://127.0.0.1:5000/files"
response = requests.get(download_url)

if response.status_code == 200:
    with open("compiled_files.zip", "wb") as f:
        f.write(response.content)
else:
    print("files were not found")

if not os.path.exists("game"): os.mkdir("game")

with ZipFile("compiled_files.zip", "r") as files:
    files.extractall(path="game")

os.remove("compiled_files.zip")

os.chdir("game")

os.system(r'powershell python -m http.server')

input("Exit program")