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
	int playerPos = 500;
	int platformX = 2000;
	int platformY = randint(100, 700);
	int Dead = 0;
	int Score = 0;


    SetTraceLogLevel(LOG_ERROR);
    InitWindow(1920, 1080, title);
    InitAudioDevice();
    SetTargetFPS(FPS);

    while (!WindowShouldClose())
    {
        //Input
		if (IsKeyDown(KEY_UP)){ playerPos = playerPos- 5;}
		if (IsKeyDown(KEY_DOWN)){ playerPos = playerPos+ 5;}


        //Update
		 platformX = platformX- 10;
		if (platformX<-50){
		 platformY = randint(100, 700);
		 platformX = 2000; Score = Score+ 1;}
		if (platformX==100&&playerPos<platformY||platformX==100&&playerPos>platformY+350){
		 Dead = 1;}


        BeginDrawing();
            ClearBackground(defaultColour);			
			DrawText(TextFormat("%i", Score), 800, 500, 200, GetColor(0x000000ff));
			DrawCircle(100, playerPos, 50, GetColor(0xff));
			DrawRectangle(platformX, 0, 50, platformY, GetColor(0xd63d3dff));
			DrawRectangle(platformX, platformY+ 350, 50, 2000, GetColor(0xf13d3dff));
		if (Dead==1){DrawRectangle(0, 0, 2000, 2000, GetColor(0x000000ff));}
        EndDrawing();
    }
    
    CloseAudioDevice();
    CloseWindow();

    return 0;
}