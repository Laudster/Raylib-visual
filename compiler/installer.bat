@echo off
setlocal enabledelayedexpansion

:: Variables
set EMSDK_REPO=https://github.com/emscripten-core/emsdk.git
set RAYLIB_REPO=https://github.com/raysan5/raylib.git
set CMAKE_URL=https://github.com/Kitware/CMake/releases/download/v3.27.7/cmake-3.27.7-windows-x86_64.zip
set GIT_URL=https://github.com/git-for-windows/git/releases/download/v2.42.0.windows.1/MinGit-2.42.0-64-bit.zip

:: Create directories
set WORKDIR=%cd%\build_tools
mkdir %WORKDIR%
cd %WORKDIR%

:: Download Git (portable)
if not exist mingit.zip (
    echo Downloading Git...
    powershell -Command "& {Invoke-WebRequest -Uri %GIT_URL% -OutFile mingit.zip}"
    tar -xf mingit.zip
    set PATH=%WORKDIR%\cmd;%PATH%
)

:: Download and extract CMake (portable)
if not exist cmake.zip (
    echo Downloading CMake...
    powershell -Command "& {Invoke-WebRequest -Uri %CMAKE_URL% -OutFile cmake.zip}"
    tar -xf cmake.zip
    set PATH=%WORKDIR%\cmake-3.27.7-windows-x86_64\bin;%PATH%
)

:: Clone Emscripten
if not exist emsdk (
    echo Cloning Emscripten SDK...
    git clone %EMSDK_REPO%
    cd emsdk
    emsdk install latest
    emsdk activate latest
    set PATH=%WORKDIR%\emsdk;%WORKDIR%\emsdk\upstream\emscripten;%PATH%
    cd ..
)

:: Clone raylib
if not exist raylib (
    echo Cloning raylib...
    git clone %RAYLIB_REPO%
)

:: Build raylib for Web
echo Building raylib for Web...
cd raylib
emcmake cmake . -B build -DBUILD_SHARED_LIBS=OFF -DPLATFORM=Web
cd build
emmake make
echo raylib built successfully!

pause
