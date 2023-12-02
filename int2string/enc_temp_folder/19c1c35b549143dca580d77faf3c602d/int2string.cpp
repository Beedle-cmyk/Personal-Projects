#include <iostream>

char* int2str(int integer) {

	char* poutputstring = new char[4];

	while (integer != 0)
	{
		int Outputlastdigit = (integer % 10) + 48;
		// assign the char to the current position of poutputstring
		*poutputstring = Outputlastdigit;
		poutputstring++;
		integer /= 10;
	}
	return poutputstring;

}

int main()
{
	// std::cout << "Hello World!\n";
	// Testing commiting a change
	// Commiting a second change
	// Final commit practice

	char* returnstring = int2str(123);
	delete[] returnstring;

	// int foo = 103;
	// int moduloValue = 0;

	/*while (foo > 0)
	{
		moduloValue = foo % 10;
		foo /= 10;
	}*/

	// Pretend we have the starting number 9
	// binary: 1001
	// If 9 is left-shifted by 1 bit, you have a new number:
	// 10010, or 18
	// Now pretend you have a 32 bit integer
	//  You want to get each bit off the number
	// and convert that bit to a character.
	// E.g:
	// 00110011 10111010 10000001 10101010
	// If you right-shift this number by 1, all the bits move over by 1, and the most significant bit is 0
	// 00011001 11011101 01000000 11010101
	// If you can capture the bit that was shifted off, it's simple to figure out if it's a string '1' or '0'
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
