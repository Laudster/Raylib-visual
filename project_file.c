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


        //Update


        BeginDrawing();
            ClearBackground(defaultColour);			
			int i = 0;
			for (int thisvariablewillnevereverbeusedbyuser = 0; thisvariablewillnevereverbeusedbyuser <10; thisvariablewillnevereverbeusedbyuser++){ i = i+ 1;
			int y = 0; y = i* 20;DrawRectangle(50, y, 10, 10, GetColor(0x000000ff));}
        EndDrawing();
    }
    
    CloseAudioDevice();
    CloseWindow();

    return 0;
}