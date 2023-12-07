#include <iostream>

char* int2str(int integer)
{
	// calculate how many characters are required to store
	int temp = integer;

	//begin counter at 1 to account for null terminator
	int charCount = 1;

	while (temp != 0)
	{
		temp /= 10;
		charCount++;
	}

	// open a location in memory for use the size of 4 char
	char* pOutputString = new char[charCount];
	//char* pStartOfString = pOutputstring;	
	char* pEndOfString = pOutputString + (charCount - 1);

	//Zero terminating the string 
	*pEndOfString = '\0';
	pEndOfString--;

	while (integer != 0)
	{
		// add 48 for ASCII conversion
		int Outputlastdigit = (integer % 10) + 48;
		// assign the char to the current position of poutputstring
		*pEndOfString = Outputlastdigit;
		pEndOfString--;
		integer /= 10;
	}
	
	return pOutputString;
}

int main()
{
	char* returnstring = int2str(1234567);
	// Remove used memory at location once done with it
	delete[] returnstring;
}

// Run program: Ctrl + F5 or Debug > Start Without Debugging menu
// Debug program: F5 or Debug > Start Debugging menu

// Tips for Getting Started: 
//   1. Use the Solution Explorer window to add/manage files
//   2. Use the Team Explorer window to connect to source control
//   3. Use the Output window to see build output and other messages
//   4. Use the Error List window to view errors
//   5. Go to Project > Add New Item to create new code files, or Project > Add Existing Item to add existing code files to the project
//   6. In the future, to open this project again, go to File > Open > Project and select the .sln file
