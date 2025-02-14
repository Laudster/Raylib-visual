REM Set the directory passed as the argument
set DIR=%1
set OUTPUT_DIR=%DIR%\web-build
set SOURCE_FILE=%DIR%\project_file.c

REM Run the emcc command
emcc -o "%OUTPUT_DIR%\project.html" "%SOURCE_FILE%" -Wall -std=c99 -D_DEFAULT_SOURCE -Wno-missing-braces -Wunused-result -Os -I. -I C:/raylib/raylib/src -I C:/raylib/raylib/src/external -L. -L C:/raylib/raylib/src -s USE_GLFW=3 -s ASYNCIFY -s TOTAL_MEMORY=67108864 -s FORCE_FILESYSTEM=1 --preload-file sounds --shell-file C:/raylib/raylib/src/shell.html C:/raylib/raylib/src/web/libraylib.a -DPLATFORM_WEB -s "EXPORTED_FUNCTIONS=[_free,_malloc,_main]" -s EXPORTED_RUNTIME_METHODS=ccall
