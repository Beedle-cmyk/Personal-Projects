#include <iostream>

int* str2int(const char* string)
{
	//decleration of index representing the position in the string
	int i = 0;
	int Negative = 0;

	if (string[i] == 45)
	{
		Negative = 1;
	}

	//finding the amount of characters in the string
	while (string[i] != '\0')
	{
		i += 1;
	}
	//decreasing value as to not start at the null pointer (therefore start at the next value over)
	i--;

	//allocating memory to store an integer
	int* pOutputInteger = new int;

	//setting up a coefficient change from tenths to hundredths, etc
	int coefficient = 1;
	int total = 0;

	while (i > -1 + Negative)
	{
		//decreasing by 48 to obtain integer ASCII value
		int OutputInteger = coefficient*(string[i] - 48);
		total += OutputInteger;
		*pOutputInteger = total;
		coefficient *= 10;
		i--;
	}

	if (Negative == 1)
	{
		*pOutputInteger = total * -1;

	}
	return pOutputInteger;
}

void teststr2int(const char* Test, int expectedInteger) 
{
	int* actualInteger = str2int(Test);
	int comparison = actualInteger - expectedInteger;

	if (comparison != 0)
	{
		std::cout << "Error:" << actualInteger << " is not equal to " << expectedInteger;
	}
	

	delete[] actualInteger;

}

int main()
{
	teststr2int("123", 123);
	teststr2int("-123", -123);
	teststr2int("0", 0);


	return 0;
}