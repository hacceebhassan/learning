#ifndef  TOKEN_H
#define	 TOKEN_H	
#include <string>
using namespace std;

class Tokenizer{
	
	private:
	
	string s;	
	bool isChar(char c);
    bool isSymbol(char c);
	bool isString(char c);		
	bool checkKeyword(string word);
	void generateToken(string word, char c);
	bool checkIdentifier(string word);
	public:
	
	void setSourceCode(string code);
	void display();
	void separateWords();
	
};

#endif
