#include <iostream>
using namespace std;

/*
1) pass 2 parameters: Mask and Value
2) Compare each individual bit to check if the 
3) compare each bit Between the value and mask using suitable operator 
4) Return the Resultant Value
*/


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


int main() 
{
	check(7, 5);
	return 0;
}