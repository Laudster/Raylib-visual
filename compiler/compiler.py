import os, json

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
            print("python not installed")
            os.system(rf'powershell Invoke-WebRequest -Uri "https://www.python.org/ftp/python/3.12.0/python-3.12.0-amd64.exe" -OutFile "$env:TEMP\python-installer.exe"; Start-Process -FilePath "$env:TEMP\python-installer.exe" -ArgumentList "/quiet InstallAllUsers=1 PrependPath=1" -Wait; Remove-Item "$env:TEMP\python-installer.exe"')

input("Exit program")

"""
import winreg as reg

def create_custom_uri_scheme(scheme, app_path):
    try:
        # Define the registry key for the custom URI scheme
        key_path = f"{scheme}"
        
        # Open HKEY_CLASSES_ROOT
        with reg.CreateKey(reg.HKEY_CLASSES_ROOT, key_path) as key:
            # Set default value for the key
            reg.SetValue(key, "", reg.REG_SZ, f"{scheme} Protocol")
            # Create the "URL Protocol" subkey
            reg.SetValueEx(key, "URL Protocol", 0, reg.REG_SZ, "")
        
        # Create the shell/open/command subkeys
        with reg.CreateKey(reg.HKEY_CLASSES_ROOT, f"{key_path}\\shell\\open\\command") as command_key:
            # Set the default value to point to the application
            reg.SetValue(command_key, "", reg.REG_SZ, f'"{app_path}" "%1"')

        print(f"Custom URI scheme '{scheme}' created successfully.")
    except Exception as e:
        print(f"Failed to create custom URI scheme: {e}")

# Replace with your desired URI scheme and application path
scheme_name = "myapp"  # Custom URI scheme, e.g., myapp://
application_path = "C:\\Path\\To\\YourApp.exe"  # Full path to your app

create_custom_uri_scheme(scheme_name, application_path)
"""