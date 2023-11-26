#include <stdio.h>
#include <stdbool.h>
#include <stdlib.h>
// #include <iostream.h>

char* int2str(int integer)
{

   char* outputstring = malloc(4*sizeof(char));

   /*
   for each decimal digit in integer 
   get it
   convert to char
   add char to output string
   divide integer by 10
   do this until intger == 0
   
   */ 
  while (integer != 0)
  {
    int leastSignificantDigit = integer % 10;-
    // cout >> "leastSignificantDigit: " << leastSignificantDigit << endl;
    char characterRepresentationOfLeastSignificantDigit = leastSignificantDigit + 48;
    outputstring = outputstring + characterRepresentationOfLeastSignificantDigit;
    integer = integer / 10;
  }
}

int main(){

    char* stri = int2str(123);
    free(stri);

    return 0;
}