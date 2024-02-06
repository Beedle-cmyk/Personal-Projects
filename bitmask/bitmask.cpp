#include <iostream>
using namespace std;
#define settingIsNightTime = 0x1
#define settingIsRain      = 0x2
#define settingIs6PM       = 0x04
#define settingIsAreaClear = 0x08
#define settingIsTornado   = 0x10
#define settingIsAlive     = 0x20
#define settingIsAwake     = 0x40
#define settingIsHappy     = 0x80


/*
1) pass 2 parameters: Mask and Value
2) Compare each individual bit to check if the 
3) compare each bit Between the value and mask using suitable operator 
4) Return the Resultant Value
*/

// Checking for 1 setting, C++ #define hex


void check(int Mask, int Value)
{

	while (Value > 0)
	{
		int C1 = Value % 2;
		int C2 = Mask % 2;

		if (C1 & C2)
		{
			cout << "1";
		}
		else
		{
			cout << "0";
		}

		Value = Value/2;
		Mask = Mask/2;

	}
}


void printSettings(int Settings)
{

}


int main() 
{
	check(7, 5);
	return 0;
}