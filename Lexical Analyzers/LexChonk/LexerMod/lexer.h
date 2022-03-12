#ifndef lexer_h    // To make sure you don't declare the function more than once by including the header multiple times.
#define lexer_h

#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <bits/stdc++.h>
#include <vector>
#include <map>
#include <iostream>
#include <fstream>
using namespace std;

bool isSpecialSymbol(string str);
bool isBinaryOperator(string str);
bool isUnaryOperator(string str);
bool isAssignmentOperator(string str);
bool isRelationalOperator(string str);
bool is_string(string lexeme);
bool is_stringOfDigits(string lexeme);
bool is_intLiteral(string lexeme);
bool is_alphanumericString(string str);
string stringParse(string line, int len, int &ind);
string integerParse(string line, int len, int &ind);
void backSlashString(string &s);
string stringLiteral(string line, int len, int &ind);
string specOperators(string line,int line_len,int &i);
string getNextLex(string line, int &ind);
void lexerLine(string line, int &n);
void mapKeywords();
void setTokenTypes();

#endif