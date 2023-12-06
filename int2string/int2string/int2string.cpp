#include <iostream>

char* int2str(int integer) {

	char* pOutputstring = new char[4];
	char* pStartOfString = pOutputstring;

	while (integer != 0)
	{
		int Outputlastdigit = (integer % 10) + 48;
		// assign the char to the current position of poutputstring
		*pOutputstring = Outputlastdigit;
		pOutputstring++;
		integer /= 10;
	}
	//Zero terminating the string 
	
	*pOutputstring = '\0';
	return pStartOfString;

}

int main()
{
	char* returnstring = int2str(123);
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
