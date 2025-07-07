#include "raylib.h"
#include <stdlib.h>
#include <time.h>
#include <string.h>

Color defaultColour = {255, 255, 255, 255};

int FPS = 60;

char title[20] = "Game";

int randint(int min, int max){return rand() % (max - min + 1);}

int main()
{
    srand(time(NULL));

    //Setup


    SetTraceLogLevel(LOG_ERROR);
    InitWindow(1920, 1080, title);
    InitAudioDevice();
    SetTargetFPS(FPS);

    while (!WindowShouldClose())
    {
        Vector2 thecurrentmousepositionasitiscurrently = GetMousePosition();
        //Input


        //Update


        BeginDrawing();
            ClearBackground(defaultColour);
        EndDrawing();
    }
    
    CloseAudioDevice();
    CloseWindow();

    return 0;
}