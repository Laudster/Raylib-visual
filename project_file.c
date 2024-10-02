#include "raylib.h"
#include <stdlib.h>

/*
Command:
emcc -o web-build/project.html project_file.c -Wall -std=c99 -D_DEFAULT_SOURCE -Wno-missing-braces -Wunused-result -Os -I. -I C:/raylib/raylib/src -I C:/raylib/raylib/src/external -L. -L C:/raylib/raylib/src -s USE_GLFW=3 -s ASYNCIFY -s TOTAL_MEMORY=67108864 -s FORCE_FILESYSTEM=1 --preload-file sounds --shell-file C:/raylib/raylib/src/shell.html C:/raylib/raylib/src/web/libraylib.a -DPLATFORM_WEB -s 'EXPORTED_FUNCTIONS=["_free","_malloc","_main"]' -s EXPORTED_RUNTIME_METHODS=ccall
*/

Color defaultColour = {255, 255, 255, 255};

int FPS = 60;

char title[20] = "Game";

int main()
{
    SetTraceLogLevel(LOG_ERROR);
    InitWindow(1920, 1080, title);
    SetTargetFPS(FPS);

    //Input

    //Update

    while (!WindowShouldClose())
    {
        BeginDrawing();
			
			ClearBackground(GetColor(0x1f1e1eff));
			DrawRectangle(860, 480, 100, 60, GetColor(0xffffffff));
			DrawText("test", 865, 490, 40, GetColor(0xcd3737ff));
        EndDrawing();
    }
    
    CloseAudioDevice();
    CloseWindow();

    return 0;
}