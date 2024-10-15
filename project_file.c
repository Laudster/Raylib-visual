#include "raylib.h"
#include <stdlib.h>
#include <string.h>

Color defaultColour = {255, 255, 255, 255};

int FPS = 60;

char title[20] = "Game";

int main()
{
    //Setup


    SetTraceLogLevel(LOG_ERROR);
    InitWindow(1920, 1080, title);
    InitAudioDevice();
    SetTargetFPS(FPS);

    while (!WindowShouldClose())
    {
        //Input
		while (0==0){ defaultColour = GetColor(0x000000ff);}


        //Update


        BeginDrawing();
            ClearBackground(defaultColour);			
        EndDrawing();
    }
    
    CloseAudioDevice();
    CloseWindow();

    return 0;
}