#include <iostream>
using namespace std;
#define settingIsNightTime  0x1
#define settingIsRain       0x2
#define settingIs6PM        0x04
#define settingIsAreaClear  0x08
#define settingIsTornado    0x10
#define settingIsAlive      0x20
#define settingIsAwake      0x40
#define settingIsHappy      0x80

/*
This function should receive an int which contains many settings and should print one statement per setting, indicating whether or not the setting is set. E.g., one print line per setting:
#define settingIsNightTime = 0x1
#define settingIsRain = 0x2
#define settingIs6PM = 0x04
#define settingIsAreaClear = 0x08
#define settingIsTornado = 0x10
#define settingIsAlive = 0x20
#define settingIsAwake = 0x40
#define settingIsHappy = 0x80
*/

void printSettings(int Settings)
{
	int Mask = 7;

	int Result = Settings & Mask;

	if (Result)
	{
		cout << Result;
	}
	else
	{
		cout << "No";
	}

}

void TestFunction()
{


}


int main() 
{
	printSettings(6);
	return 0;
}