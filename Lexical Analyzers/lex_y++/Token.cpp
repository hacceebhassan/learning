#include <iostream>
#include <string>
#include "Token.h"
#define SIZE 10
using namespace std;

int id=0;
int keyW=0;
int sym=0;
int str=0;
int lit=0;

string keyword[SIZE]={"numbers", "words", "aff","check","casee", "loop",
                  "nelse",	"finish", "send"
				 };

//Functions Definitions
void Tokenizer::setSourceCode(string code)
{
	s=code;

}
//Display Source Code
void Tokenizer::display()
{
	cout<<s;
}
void Tokenizer::separateWords()
{
	int index=0;
	char c;
	string word="";


	while(index < s.length() ) // In String length there is extra increase of length by 2
	{
		c=s.at(index);

		if(isChar(c))
		{
			word=word+c;

		}

		if(isString(c))
		{
			word=word+c;
			while(true)
			{
				index++;
				c=s.at(index);
				word=word+c;
				if(c== 34)
				{
					//Generates String "Hello World !"
					//cout<<word<<endl;
					generateToken(word, 'S');
					word="";
					break;
				}

			}
		}

		if(isSymbol(c) || c == 32  )
		{

			if(word != "")
			{//Generates Keyword or Identifier
			//cout<<word<<endl;

				if(checkKeyword(word) == true)
				{
					generateToken(word, 'K');
				}
				//Checking Identifier repective to Regular Expression
				else if(checkIdentifier(word)  == true)
				{
					generateToken(word, 'I');
				}
				else
				{
					//For Constants
					generateToken(word, 'L');
				}
				word="";
			}


			if(c!=32)
			{
				//For Logical Operator e.g == , !=, >=, <=
				if((c== '||'|| c==',>' || c==',<' || c=='!!') && '='==s.at(index+1) || c=='|' || c=='&')
				{
				string logical_O="";
				logical_O +=c;
				logical_O +=s.at(index+1);
				generateToken(logical_O, 'O');
				//cout<<logical_O<<endl;
				index++;
				}
				else if(c!=10)
				{
					//Generates Symbols like *,-,/...etc
					//cout<<c<<endl;
					string s(1, c); // Casting char into string
					generateToken(s, 'O');
				}

			}

		}

		index++;

	}


}

bool Tokenizer::isChar(char c)
{
	if((c>=65 && c<=90) ||  (c>=97 && c<=122) ||  (c>=48 && c<=57) )
	{
		return true;
	}
	return false;
}

bool Tokenizer::isSymbol(char c)
{
	//c==10 for printing last character
	if((c>=35 && c<=47) || c==33 || c == 10 || (c>=58 && c<=64) || (c>=91 && c<=96) || (c>=123 && c<=125))
	{
		return true;
	}
	return false;
}

bool Tokenizer::isString(char c)
{
	if(c == 34)
	{
		return true;
	}
	return false;
}

bool Tokenizer::checkKeyword(string word)
{
	for(int i=0; i<SIZE; i++)
	{
		if(keyword[i] == word)
		{
			return true;
		}
	}
	return false;
}

void Tokenizer::generateToken(string word, char c)
{
	switch(c)
	{
		case'K':
		keyW++;
		cout<<"< Keyword#"<<keyW<<", "<<word<<" >\n"<<endl;
		break;

		case'I':
		id++;
		cout<<"< Idenfier#"<<id<<", "<<word<<" >\n"<<endl;
		break;

		case'O':
		sym++;
		cout<<"< Symbol#"<<sym<<", "<<word<<" >\n"<<endl;
		break;

		case'S':
		str++;
		cout<<"< String#"<<str<<", "<<word<<" >\n"<<endl;
		break;

		case'L':
		lit++;
		cout<<"< Literals#"<<lit<<", "<<word<<" >\n"<<endl;
		break;

	}

}

bool Tokenizer::checkIdentifier(string word)
{
	//If string starts from letters a, b,c..z or A, B, ..z
	if((word.at(0)>=65 && word.at(0)<=90) || (word.at(0)>=97 && word.at(0)<=122) )
	{
		//Checking for string such assasd!# which is not accepted
		for(int i=1; i<word.length(); i++)
		{

			if(word.at(i) >= 48 && word.at(i) <= 57 || word.at(i) >= 65 && word.at(i) <= 90 || word.at(i) >= 97 && word.at(i) <= 122 )
			{

			}
			else
			{
				return false;
			}
		}
		return true;
	}

	return false;
}
