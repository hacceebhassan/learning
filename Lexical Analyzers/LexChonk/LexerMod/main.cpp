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