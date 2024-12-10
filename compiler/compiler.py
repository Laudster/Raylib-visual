import os, sys, ctypes, json

appdata = os.getenv('APPDATA')  # Gets the Roaming folder

settings_folder = os.path.join(appdata, "Raylib-visual")

def install():
    if ctypes.windll.shell32.IsUserAnAdmin():
        print("has admin perms")
    else:
        print("no admin perms")
        input()
        sys.exit(1)

    output = os.popen("choco --version")

    if len(output.read()) == 0:
        print("choco not installed")
        choco_install_command = (
            "Set-ExecutionPolicy Bypass -Scope Process -Force; "
            "iex ((New-Object System.Net.WebClient).DownloadString('https://chocolatey.org/install.ps1'))"
        )
        powershell_command = f'powershell -NoProfile -ExecutionPolicy Bypass -Command "{choco_install_command}"'
        os.system(powershell_command)
        sys.exit()
    else:
        print("choco should be installed")


    output = os.popen("python --version")

    if len(output.read()) == 0:
        print("python not installed")
        powershell_command = f'powershell -NoProfile -ExecutionPolicy Bypass -Command "choco install python"'
        os.system(powershell_command)
    else:
        print("python should be installed")

    output = os.popen("git --version")

    if len(output.read()) == 0:
        print("git not installed")
        powershell_command = f'powershell -NoProfile -ExecutionPolicy Bypass -Command "choco install git"'
        os.system(powershell_command)
        sys.exit()
    else:
        print("git should be installed")


    output = os.popen("make --version")

    if len(output.read()) == 0:
        print("make not installed")
        powershell_command = f'powershell -NoProfile -ExecutionPolicy Bypass -Command "choco install make"'
        os.system(powershell_command)
    else:
        print("make should be installed")

    os.chdir(settings_folder)

    powershell_command = f'powershell -NoProfile -ExecutionPolicy Bypass -Command "git clone https://github.com/emscripten-core/emsdk.git"'
    os.system(powershell_command)
    os.chdir("emsdk")
    os.system('cmd /c emsdk install latest')
    os.system('cmd /c emsdk activate latest --permanent')

    os.chdir("..")
    powershell_command = f'powershell -NoProfile -ExecutionPolicy Bypass -Command "git clone https://github.com/raysan5/raylib.git"'
    os.system(powershell_command)
    os.chdir("raylib")
    os.chdir("src")
    if not os.path.exists("web"): os.makedirs("web")

    with open("Makefile", "r") as file_read:
        lines = file_read.readlines()

        for i, v in enumerate(lines):
            if "Define target platform" in v:
                lines[i+1] = "PLATFORM             ?= PLATFORM_WEB\n"
            if "RAYLIB_RELEASE_PATH  ?= $(RAYLIB_SRC_PATH)" in v:
                lines[i] = "RAYLIB_RELEASE_PATH  ?= $(RAYLIB_SRC_PATH)/web\n"
        
        with open("Makefile", "w") as file_edit:
            file_edit.writelines(lines)
    
    os.system('cmd /c make -e PLATFORM=PLATFORM_WEB -B')

    input()

def compile_check(file):
    with open(os.path.join(settings_folder, "test.c"), "w") as f:
        f.write('#include "raylib.h"\nint main() {\n\tInitWindow(800, 600, "Raylib with emcc");\n\tCloseWindow();\n\treturn 0;\n}')

    build_fodler = os.path.join(settings_folder, "web-build")

    if os.path.isfile(os.path.join(build_fodler, "test.html")):
        for v in os.listdir(build_fodler):
            os.remove(os.path.join(build_fodler, v))
        os.rmdir(build_fodler)

    os.makedirs(build_fodler, exist_ok=True)

    try:
        os.system(f'emcc -o {os.path.join(build_fodler, "test.html")} {os.path.join(settings_folder, "test.c")} -Wall -std=c99 -D_DEFAULT_SOURCE -Wno-missing-braces -Wunused-result -Os -I. -I {settings_folder}/raylib/src -I {settings_folder}/raylib/src/external -L. -L {settings_folder}/raylib/src -s USE_GLFW=3 -s ASYNCIFY -s TOTAL_MEMORY=67108864 -s FORCE_FILESYSTEM=1 --shell-file {settings_folder}/raylib/src/shell.html {settings_folder}/raylib/src/web/libraylib.a -DPLATFORM_WEB -s "EXPORTED_FUNCTIONS=[_free,_malloc,_main]" -s EXPORTED_RUNTIME_METHODS=ccall')
    finally:
        print("Checked if ready for build")

    if os.path.isfile(os.path.join(build_fodler, "test.html")):
        print("Configured for build")
        file.write('{"installed": true}')
        sys.exit()
    else:
        print("file does not exist")
        install()


if os.path.exists(settings_folder):
    print("raylib folder exists")

    with open(os.path.join(settings_folder, "settings.json"), "w+") as file:
        if len(file.read()) != 0:
            data = json.load(file)
            if data["installed"] == True:
                print("ready for compile")
                sys.exit()
            else:
                compile_check(file)
        else:
            compile_check(file)
else:
    os.makedirs(settings_folder, exist_ok=True)
    with open(os.path.join(settings_folder, "settings.json"), "w+") as file:
        compile_check(file)


# Pyinstall command: pyinstaller --onefile --uac-admin compiler.py