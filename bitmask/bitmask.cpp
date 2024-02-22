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

/*
Check the provided int for 8 settings, return an integer with all the true settings set to 1
E.g.: when bitmaskedSettings == 0xC0, return value is 0xC0
when bitmaskedSettings == 0x80AC00C0, return value is 0xC0
compare in test function with resultant value 
test number with 0th and 1st bit set with other stuff
Expand each nibble
*/

void printSettings(int Settings)
{
	int Mask = 7;

	int Result = Mask & Settings;
	int counter = 1;

	for (int i = 0; i < Result; i++)
	{
		if (counter & Result)
		{
			cout << counter << endl;
		}
		counter*=2;
	}

}

int getTrueSettings(int bitmaskedSettings)
{

	int Mask = 7;

	
	return 0;

}


int main() 
{
	printSettings();
	return 0;
}