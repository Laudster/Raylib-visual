#include "raylib.h"
#include <stdlib.h>
#include <string.h>

/*
Command:
emcc -o web-build/project.html project_file.c -Wall -std=c99 -D_DEFAULT_SOURCE -Wno-missing-braces -Wunused-result -Os -I. -I C:/raylib/raylib/src -I C:/raylib/raylib/src/external -L. -L C:/raylib/raylib/src -s USE_GLFW=3 -s ASYNCIFY -s TOTAL_MEMORY=67108864 -s FORCE_FILESYSTEM=1 --preload-file sounds --shell-file C:/raylib/raylib/src/shell.html C:/raylib/raylib/src/web/libraylib.a -DPLATFORM_WEB -s 'EXPORTED_FUNCTIONS=["_free","_malloc","_main"]' -s EXPORTED_RUNTIME_METHODS=ccall
*/

Color defaultColour = {255, 255, 255, 255};

int FPS = 60;

char title[20] = "Game";

int main()
{
    //Setup
	int change = 0;
	int color = 0;


    SetTraceLogLevel(LOG_ERROR);
    InitWindow(1920, 1080, title);
    InitAudioDevice();
    SetTargetFPS(FPS);

    while (!WindowShouldClose())
    {
        //Input
		if (IsMouseButtonPressed(MOUSE_BUTTON_LEFT)){
		 change = 1;}


        //Update
		if (change==1&&color==0){ defaultColour = GetColor(0x000000ff);
		 color = 1;
		 change = 0;}
		if (change==1&&color==1){ defaultColour = GetColor(0xffffffff);
		 color = 0;
		 change = 0;}


        BeginDrawing();
            ClearBackground(defaultColour);			
        EndDrawing();
    }
    
    CloseAudioDevice();
    CloseWindow();

    return 0;
}