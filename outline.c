#include "raylib.h"
#include <stdlib.h>
#include <time.h>
#include <string.h>

Color bakgrunnFarge = {255, 255, 255, 255};

int FPS = 60;

char tittel[20] = "Game";

int randint(int min, int max){return rand() % (max - min + 1);}

int main()
{
    srand(time(NULL));

    //Setup


    SetTraceLogLevel(LOG_ERROR);
    InitWindow(1920, 1080, tittel);
    InitAudioDevice();
    SetTargetFPS(FPS);

    while (!WindowShouldClose())
    {
        Vector2 thecurrentmousepositionasitiscurrently = GetMousePosition();
        //Input


        //Update


        BeginDrawing();
            ClearBackground(bakgrunnFarge);
        EndDrawing();
    }
    
    CloseAudioDevice();
    CloseWindow();

    return 0;
}