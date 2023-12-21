#include <iostream>

char* int2str(int integer)
{
		//begin counter at 1 to account for null terminator
		int charCount = 1;

		//setting negative flag where "if == 1" then the value is negative
		int Negative = 0;


		// check if number is a negative value
		if (integer < 0)
		{
			//convert number into positive value so that it meets conditions for loop
			integer = integer * -1;
			charCount++;
			Negative = 1;
		}


		// calculate how many characters are required to store
		int temp = integer;
		while (temp != 0)
		{
			temp /= 10;
			charCount++;
		}
		if (integer == 0)
		{
			charCount++;
		}


		// open a location in memory for use the size of 4 char
		char* pOutputString = new char[charCount];

		// starting at the last position in memory
		char* pEndOfString = pOutputString + (charCount - 1);

		//Zero terminating the string 
		*pEndOfString = '\0';
		pEndOfString--;

		// if the value is zero then return value will automatically be 48
		if (integer == 0)
		{
			*pEndOfString = 48;
		}


		while (integer > 0)
		{
			// add 48 for ASCII conversion
			int Outputlastdigit = (integer % 10) + 48;
			// assign the char to the current position of poutputstring
			*pEndOfString = Outputlastdigit;
			pEndOfString--; 
			integer /= 10;
		}
		if (Negative == 1)
		{
			//the starting value will be the ASCII value of "-"
			*pEndOfString = 45;
		}

		return pOutputString;
}

void testint2str(int Test, const char* expectedString)
{
	char* actualString = int2str(Test);
	int comparison = strcmp(actualString, expectedString);

	if (comparison != 0)
	{
		std::cout << "Error: " << actualString << " is not equal to " << expectedString;
	}

	// Remove used memory at location once done with it
	delete[] actualString;

}

int main()
{
	testint2str(123, "123");
	testint2str(-123, "-123");
	testint2str(0, "0");
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