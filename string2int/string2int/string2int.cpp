#include <iostream>
#define zeroInASCII 48
#define minusSignInASCII 45

int str2int(const char* pInputString)
{
	//decreasing value as to not start at the null pointer (therefore start at the next value over)
	int currentStringPosition = strlen(pInputString) - 1;
	int isNegativeNumber = false;

	if (pInputString[0] == minusSignInASCII)
	{
		isNegativeNumber = true;
	}

	//setting up a coefficient change from tenths to hundredths, etc
	int coefficient = 1;
	int OutputInteger = 0;

	while (currentStringPosition > -1 + isNegativeNumber)
	{
		//decreasing by 48 to obtain integer ASCII value
		int temp = coefficient * (pInputString[currentStringPosition] - zeroInASCII);
		OutputInteger += temp;
		coefficient *= 10;
		currentStringPosition--;
	}


	if (isNegativeNumber == true)
	{
		OutputInteger *= -1;

	}
	return OutputInteger;
}

void teststr2int(const char* Test, int expectedInteger) 
{
	int actualInteger = str2int(Test);

	if (actualInteger != expectedInteger)
	{
		std::cout << "Error:" << actualInteger << " is not equal to " << expectedInteger << std::endl;
	}
	else
	{
		std::cout << "Pass " << actualInteger << " is equal to " << expectedInteger << std::endl;
	}
	
}

int main()
{
	teststr2int("123", 123);
	teststr2int("-123", -123);
	teststr2int("0", 0);


	return 0;
}