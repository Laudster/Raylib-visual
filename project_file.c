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
	int platformSize = randint(20, 700);
	int score = 0;
	int dead = 0;


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
		 platformSize = randint(200, 700);
		 platformX = 2000;}
		if (platformX<101&&playerPos-50<platformSize||platformX<101&&playerPos--50>platformSize+350){
		 dead = 1;}


        BeginDrawing();
            ClearBackground(defaultColour);			
			DrawCircle(100, playerPos, 50, GetColor(0xff));
			DrawRectangle(platformX, 0, 50, platformSize, GetColor(0xff0000ff));
			DrawRectangle(platformX, platformSize+ 350, 50, 2000, GetColor(0xff0000ff));
		if (dead==1){DrawRectangle(0, 0, 2000, 2000, GetColor(0x000000ff));}
        EndDrawing();
    }
    
    CloseAudioDevice();
    CloseWindow();

    return 0;
}