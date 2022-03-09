#include <iostream>
#include <fstream>
#include "Token.cpp"
#include <string>
using namespace std;

int main()
{

	//Reading Source Code from file
	ifstream MYFILE("sourceCode.txt");
	string s_Code="";

	//below function used for reading file content and storing it in string variable s_Code
	s_Code.assign( istreambuf_iterator<char>(MYFILE) , istreambuf_iterator<char>());


	Tokenizer object;

	object.setSourceCode(s_Code);

    object.display();
	object.separateWords();

	return 0;
}


