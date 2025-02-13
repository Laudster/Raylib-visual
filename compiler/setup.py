from winreg import CreateKey, SetValue, SetValueEx, REG_SZ, HKEY_CLASSES_ROOT
from os import path, getenv
from sys import argv, executable
from json import dumps

if len(argv) > 1:
    appdata = getenv("appdata")
    settings_folder = path.join(appdata, "Raylib-Visual")

    try:
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
            SetValue(command_key, "", REG_SZ, f'"{path.dirname(executable)}\\{argv[1]}" "%1"')

        print(f"Custom URI scheme '{scheme}' created successfully.")

        with open(path.join(settings_folder, "settings.json"), "w") as file:
            file.write(dumps({"setup": True}, indent=4))


    except Exception as e:
        print(f"Failed to create custom URI scheme: {e}")

    input()