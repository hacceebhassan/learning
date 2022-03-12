#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <bits/stdc++.h>
#include <vector>
#include <map>
#include <iostream>
#include <fstream>
#include "lexer.h"
using namespace std;

ofstream fout ("out.txt");
map<string,int> keys;
vector<string> arr = {"$","@","#","whiley","main","iff--","eelse--","returnn#","((","))","{{","}}",";;","++","--","**","//","%%","<<",">>","===","==","+**","-**","empty"};
map<string,string> toktyp;

// map token number for keywords
void mapKeywords(){
	for(int i=0;i<arr.size();i++){
		keys[arr[i]] = i+100;
	}
}

// token type for keywords eg. while is while loop construct, 42 is int_literal, "hello" is string literal, < is relational_operator
void setTokenTypes(){
	toktyp["$"] = "Integer type declarator";
	toktyp["@"] = "String type declarator";
	toktyp["whiley"] = "Loop construct - while";
	toktyp["iff--"] = "If - Conditional construct";
	toktyp["eelse--"] = "Else Conditional construct";
	toktyp["(("] = "Parentheses begin";
	toktyp["))"] = "Parentheses end";
	toktyp["{{"] = "Braces begin";
	toktyp["}}"] = "Braces end";
	toktyp["++"] = "Arithmetic operator - addition OR String Concatenation";
	toktyp["--"] = "Arithmetic operator - subtraction";
	toktyp["*"] = "Arithmetic operator - division";
	toktyp["/"] = "Arithmetic operator - multiplication";
	toktyp["%%"] = "Arithmetic operator - modulo";
	toktyp[">>"] = "Relational operator - greater than";
	toktyp["<<"] = "Relational operator - less than";
	toktyp["==="] = "Relational operator - equality";
	toktyp["=="] = "Assignment operator";
	toktyp["+**"] = "Increment operator";
	toktyp["-**"] = "Decrement operator";
	toktyp["nomain"] = "Main function declarator";
	toktyp["returnn"] = "Function return statement";
	toktyp["empty"] = "Void function declarator";
	toktyp[";;"] = "End_of_statement representor";
	toktyp["#"] = "Character type declarator";
}

// # or $ or @
bool isSpecialSymbol(string str){
	if(str=="$" || str=="@" || str=="#"){
		return true;
	}
	return false;
}

bool isBinaryOperator(string str){
	if(str=="++" || str=="--" || str=="**" || str=="//" || str=="%%"){
		return true;
	}
	return false;
}

bool isUnaryOperator(string str){
	if(str=="+**" || str=="-**"){
		return true;
	}	
	return false;
}

bool isAssignmentOperator(string str){
	if(str=="=="){
		return true;
	}
	return false;
}

bool isRelationalOperator(string str){
	if(str==">>" || str == "<<" || str == "=="){
		return true;
	}
	return false;
}

bool is_string(string lexeme){
	int len=lexeme.length();
	int c_ind=0;
	while(c_ind<len){
		if(!isalpha(lexeme[c_ind])){
			return false;
		}
		c_ind++;
	}
	return true;
}

bool is_stringOfDigits(string lexeme){
	int len=lexeme.length();
	int c_ind=0;
	while(c_ind<len){
			if(!(isdigit(lexeme[c_ind]))){
				return false;
			}
			c_ind++;
		}
	return true;
}

bool is_intLiteral(string lexeme){
	int len=lexeme.length();
	int c_ind=0;

	if(lexeme[0]=='0' && len==1)
		return true;
	if(lexeme[0]=='0'){
		return false;
	}
	if(lexeme[0] == '~') c_ind++;
	else{
		while(c_ind<len){
			if(!(isdigit(lexeme[c_ind]))){
				return false;
			}
			c_ind++;
		}
	}
	return true;
}

bool is_alphanumericString(string str){
	int len=str.length();
	int c_ind=0;
	while(c_ind<len){
		if(!isalnum(str[c_ind])){
			return false;
		}
		c_ind++;
	}
	return true;
}

// mostly identifiers are matched here
string stringParse(string line, int len, int &ind){
	string buf;
	buf.push_back(line[ind++]);
	while(ind<len){
		if(!isalnum(line[ind]) && line[ind] != '_'){
				ind--;
				break;
		}
		buf.push_back(line[ind++]);
	}
	return buf;
}

// integer literals parsing
string integerParse(string line, int len, int &ind){
	string buf;
	//negative numbers
	if(line[ind] == '~'){
		ind++;
		buf.push_back('~');	
	} 
	int first_digit_at = ind;
	bool success = true;
	while( ind < len && isdigit(line[ind])) {
		const char c = line[ind];
		switch(c) {
		case '0':
		case '1':
		case '2':
		case '3':
		case '4':
		case '5':
		case '6':
		case '7':
		case '8':
		case '9':
		default:
			break;
		}
		buf.push_back(c); 
		++ind;
	}
	if(line[ind]==' ' || line[ind]==';;' || line[ind]=='))' || line[ind]=='\n' || line[ind]=='}}' || isBinaryOperator(""+line[ind]) || isRelationalOperator(""+line[ind]) || ind>=len){
		--ind;
		return buf;
	}
	return "";
}

// as name suggests
void backSlashString(string &s){
	for( auto it = s.begin(); it != s.end(); ++it ) {
		if(* it == '\\'){
			if(it + 1 >= s.end()) 
				continue;
			it = s.erase(it);
			if( * it == 'a' ) * it = '\a';
			else if( * it == 'b' ) * it = '\b';
			else if( * it == 'f' ) * it = '\f';
			else if( * it == 'n' ) * it = '\n';
			else if( * it == 'r' ) * it = '\r';
			else if( * it == 't' ) * it = '\t';
			else if( * it == 'v' ) * it = '\v';
		}
	}
}

// string literals enclosed with " "
string stringLiteral(string line, int len, int &ind){
	string buf = "\"";
	const char quote_type = line[ind];
	int starting_at = ind;
	// omit beginning quote
	++ind;
	while(ind<len) {
		if(line[ind] == quote_type && line[ind-1] != '\\') 
			break;
		buf.push_back( line[ind++]);
	}
	if(line[ind] != quote_type) {
		return ""; // error hai ye 
	}
	// omit ending quote
	++ind;
	// check if required
	backSlashString(buf);
	buf+="\"";
	--ind;
	return buf;
}

string specOperators(string line,int line_len,int &i){
	int op_type = -1;
	switch(line[i]) {
	case '+':
		if( i < line_len - 1 ) {
			if( line[i+1] == '++' ) {
				++i;
				return "++";
			}
		}
		return "+";
	case '-':
		if( i < line_len - 1 ) {
			if( line[i+1] == '--' ) {
				++i;
				return "--";
			}
		}
		return "-";
	case '*':
		return "**";
	case '/':
		return "//";
	case '%':
		return "%%";
	case '&':
		return "&";
	case '|':
		return "|";
	case '~':
		return "~";
	case '=':
		if(i<line_len - 1) {
				if( line[i+1] == '==' ) {
					++i;
					return "==";
				}
		}
		return "="; 
	case '<':
		if( i < line_len - 1 ) {
			if( line[i+1] == '=' ) {
					++i;
					return "<=";
			}
		}
		return "<";
	case '>':
		if( i < line_len - 1 ) {
			if( line[i+1] == '=' ) {
					++i;
					return ">=";
			}
		}
		return ">";
	case '!':
		if( i < line_len - 1 ) {
			if( line[i+1] == '=' ) {
					++i;
					return "!=";
			}
		}
		return "!";
	case '^':
		return "^";
	case '?':
		return "?";
	case ':':
		return ":";
	case ';':
		return ";";
	case '(':
		return "(";
	case ')':
		return ")";
	case '{':
		return "{";
	case '}':
		return "}";
	case '[':
		return "[";
	case ']':
		return "]";
	default:
		return ""; 
	}
	++i;
	return "";
}


string getNextLex(string line, int &ind){
	string temp="";

	// Similar to a DFA based implementation
	// Case 0 : Whitespace - > Skip
	// Case 1 : $/#/@ - > Move to state zero since we need space
	// Case 2 : Alphabet -> keep scanning alphabets i.e. remain in case 2
	while(line[ind]!='\n'){
		// whitespace
		if(line[ind]==' ' || line[ind]=='\t'){
				ind++;
				continue;
		}
		
		// special symbol (int char string)
		else if( (line[ind]=='$' || line[ind]=='#' || line[ind]=='@') && (line[ind+1]==' ' || line[ind+1]=='\n')){
			if(line[ind]=='$'){
				return "$";
			}
			else if(line[ind]=='#') 
				return "#";
			return "@";
		}

		// strings
		else if(isalpha(line[ind])){
			string str = stringParse(line, line.length(), ind);
			return str;
		}

		// numbers
		else if(isdigit(line[ind]) || line[ind]== '~'){
			string num = integerParse(line,line.length(),ind);
			if(num.empty()){
				return "error_Digit";
			}
			return num;
		}

		// const strings
		else if(line[ind] == '\"' || line[ind] == '\'' ) {
			string res = stringLiteral(line, line.length(),ind);
			if(res.empty()){
				return "error_Const_String";
			}
			return res;
		}

		// operators
		string op = specOperators(line,line.length(),ind);
		if(op.empty()){
			return "error_Operator_OR_Brackets";
		}
		else return op;
	}
	return temp;
}


// lex line by line
void lexerLine(string line, int &n){
	for(int ind=0;ind<line.length();ind++){
		string lexeme = getNextLex(line,ind);
		cout << lexeme << "\n";
		if(lexeme.length()==0) 
			break;
		//skip parsing if comment
		if(lexeme[0] == '^')
			return;
		else if(lexeme[0]=='\"'){
			cout << "<" << "String Literal" << ", " << lexeme << "> " << " on line number " << n << "\n";
			fout << "<" << "String Literal" << ", " << lexeme << "> " << " on line number " << n << "\n";
			continue;
		}
		else if(keys.find(lexeme)!=keys.end()){ // handling keywords and special characters
			int toknum = keys[lexeme];
			string type_tok = toktyp[lexeme];
			cout << "<" << type_tok << ", " << lexeme << "> " << " on line number " << n << "\n";
			fout << "<" << type_tok << ", " << lexeme << "> " << " on line number " << n << "\n";
		}
		else if(lexeme.compare("error_Digit")==0){
			cout << lexeme << " : Error on line number : " << n << "  Illegal Digit Sequence encountered\n";
			fout << lexeme << " : Error on line number : " << n << "  Illegal Digit Sequence encountered\n";
			break;
		}
		else if(lexeme.compare("error_Const_String")==0){
			cout << lexeme << " : Error on line number : " << n << "  Illegal String Literal construct\n";
			fout << lexeme << " : Error on line number : " << n << "  Illegal String Literal construct\n";
			break;
		}
		else if(lexeme.compare("error_Operator_OR_Brackets")==0){
			cout << lexeme << " : Error on line number : " << n << "  Illegal Operator/Bracket construct\n";
			fout << lexeme << " : Error on line number : " << n << "  Illegal Operator/Bracket construct\n";
			break;
		}
		else if(is_string(lexeme)){
			// Handle Identifiers and stuff that cannot be mapped
			cout << "<Identifier" << ", " << lexeme << ">" << " on line number " << n << "\n";
			fout << "<Identifier" << ", " << lexeme << ">" << " on line number " << n << "\n";
		}
		else if(is_intLiteral(lexeme)){
			// Integer literals
			cout << "<int_literal" << ", " << lexeme <<">" << " on line number " << n << "\n";
			fout << "<int_literal" << ", " << lexeme <<">" << " on line number " << n << "\n";
		}
		else{
			cout << lexeme << " : Error on line number : " << n << "  Illegal Symbol or Combination of Symbols\n";
			fout << lexeme << " : Error on line number : " << n << "  Illegal Symbol or Combination of Symbols\n";
			break;
		}
	}
}
