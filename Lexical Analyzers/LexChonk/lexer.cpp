#include <stdio.h>
#include <stdlib.h>
#include <string.h>
//#include <bits/stdc++.h>
#include <vector>
#include <map>
#include <iostream>
#include <fstream>
using namespace std;

ofstream fout ("out.txt");
map<string,int> keys;
vector<string> arr = {"$","@","#","while","main","if","else","return","(",")","{","}",";","+","-","*","/","%","<",">","==","=","++","--","void"};
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
	toktyp["while"] = "Loop construct - while";
	toktyp["if"] = "If - Conditional construct";
	toktyp["else"] = "Else Conditional construct";
	toktyp["("] = "Parentheses begin";
	toktyp[")"] = "Parentheses end";
	toktyp["{"] = "Braces begin";
	toktyp["}"] = "Braces end";
	toktyp["+"] = "Arithmetic operator - addition";
	toktyp["-"] = "Arithmetic operator - subtraction";
	toktyp["/"] = "Arithmetic operator - division";
	toktyp["*"] = "Arithmetic operator - multiplication";
	toktyp["%"] = "Arithmetic operator - modulo";
	toktyp[">"] = "Relational operator - greater than";
	toktyp["<"] = "Relational operator - less than";
	toktyp["=="] = "Relational operator - equality";
	toktyp["="] = "Assignment operator";
	toktyp["++"] = "Increment operator";
	toktyp["--"] = "Decrement operator";
	toktyp["main"] = "Main function declarator";
	toktyp["return"] = "Function return statement";
	toktyp["void"] = "Void function declarator";
	toktyp[";"] = "End_of_statement representor";
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
	if(str=="+" || str=="-" || str=="*" || str=="/" || str=="%"){
		return true;
	}
	return false;
}

bool isUnaryOperator(string str){
	if(str=="++" || str=="--"){
		return true;
	}	
	return false;
}

bool isAssignmentOperator(string str){
	if(str=="="){
		return true;
	}
	return false;
}

bool isRelationalOperator(string str){
	if(str==">" || str == "<" || str == "=="){
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
string get_name(string line, int len, int &ind){
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
string get_num(string line, int len, int &ind){
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
	if(line[ind]==' ' || line[ind]==';' || line[ind]==')' || line[ind]=='\n' || line[ind]=='}' || isBinaryOperator(""+line[ind]) || isRelationalOperator(""+line[ind]) || ind>=len){
		--ind;
		return buf;
	}
	return "";
}

// as name suggests
void remove_back_slash(string &s){
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
string get_const_str(string line, int len, int &ind){
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
	remove_back_slash(buf);
	buf+="\"";
	--ind;
	return buf;
}

string get_operator(string line,int line_len,int &i){
	int op_type = -1;
	switch(line[i]) {
	case '+':
		if( i < line_len - 1 ) {
			if( line[i+1] == '+' ) {
				++i;
				return "++";
			}
		}
		return "+";
	case '-':
		if( i < line_len - 1 ) {
			if( line[i+1] == '-' ) {
				++i;
				return "--";
			}
		}
		return "-";
	case '*':
		return "*";
	case '/':
		return "/";
	case '%':
		return "%";
	case '&':
		return "&";
	case '|':
		return "|";
	case '~':
		return "~";
	case '=':
		if(i<line_len - 1) {
				if( line[i+1] == '=' ) {
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
			string str = get_name(line, line.length(), ind);
			return str;
		}

		// numbers
		else if(isdigit(line[ind]) || line[ind]== '~'){
			string num = get_num(line,line.length(),ind);
			if(num.empty()){
				return "error_Digit";
			}
			return num;
		}

		// const strings
		else if(line[ind] == '\"' || line[ind] == '\'' ) {
			string res = get_const_str(line, line.length(),ind);
			if(res.empty()){
				return "error_Const_String";
			}
			return res;
		}

		// operators
		string op = get_operator(line,line.length(),ind);
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

int main(){
	string testfile_name;
	cout<<"Enter the name of the testfile (e.g. inp.txt): \n";
	cin>>testfile_name;
	ios::sync_with_stdio(0);
    cin.tie(0);
    cout.tie(0);
    mapKeywords();
    setTokenTypes();
    string linbuff = "";
	ifstream fin(testfile_name);
	ofstream fout("out.txt");
	int c,n=0;
	if (fin.is_open()){
		if(fout.is_open()){
		    while (getline(fin,linbuff)){
		    	cout << '\n';
		    	linbuff+="\n";
		    	n++;
		    	//parse line by line
		    	lexerLine(linbuff,n);
	       		linbuff = "";
		    }
		    fin.close();
		    fout.close();
		}
		else{
    		cout << "Error opening output file. Please try again. \n";
    	}
	}
	else{
		cout << "Error opening input file. Please try again. \n";
	}
	return 0;
}