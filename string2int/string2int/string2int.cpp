#include <iostream>
#define zeroInASCII       48
#define minusSignInASCII  45
#define blankSpaceInASCII 32

int str2int(const char* pInputString)
{
	/*
	//decreasing value as to not start at the null pointer (therefore start at the next value over)
	int currentStringSize = strlen(pInputString) - 1;
	bool isNegative = false;
	int index = 0;

	if (pInputString[0] == minusSignInASCII)
	{
		index++;
		isNegative = true;
	}


	int coefficient = pow(10, currentStringSize-index);
	int OutputInteger = 0;

	for (index; index <= currentStringSize; index++)
	{
		if (pInputString[index] == blankSpaceInASCII)
		{
			coefficient /= 10;
			index++;
		}
		else
		{
			int temp = coefficient * (pInputString[index] - zeroInASCII);
			OutputInteger += temp;
			coefficient /= 10;
		}
	}

	if (isNegative == true)
	{
		OutputInteger *= -1;
	}

	return OutputInteger;
	*/

	
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
	
	//The position string starts at the final position and decreases until it reaches the first position
	//If this first position is minusSignInASCII it skips it by stopping when the position is 0 (First position)
	while (currentStringPosition > -1 + isNegativeNumber)
	{
		if (pInputString[currentStringPosition] == blankSpaceInASCII)
		{
			currentStringPosition--;
		}
		else
		{
			//decreasing by 48 to obtain integer ASCII value
			int temp = coefficient * (pInputString[currentStringPosition] - zeroInASCII);
			OutputInteger += temp;
			coefficient *= 10;
			currentStringPosition--;
		}
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
	teststr2int(" 0   ", 0);
	teststr2int("1               2                 3", 123);
	teststr2int("-12                 4", -124);


	return 0;
}