#include <iostream>

int* str2int(char* string)
{

	size_t i = strlen(string);
	

	int* pOutputInteger = new int[4];
	int* pStartOutputInteger = pOutputInteger;

	//*pOutputInteger = string[1];


	return pOutputInteger;
}

int main()
{
	char array[] = "1234";
	int* returninteger = str2int(array);
	delete[] returninteger;

	return 0;
}