#include <stdio.h>
#include <iostream>
#include <sstream>
#include <fstream>
#include <string>
#include <string.h>
#include <cstring>
#include <vector>
#include <map>
#include <iomanip>

using namespace std;

map<string, long long int> data_list = 
{
	{"$0", 0}, {"$1", 1}, {"$2", 2}, {"$3", 3}, {"$4", 4}, {"$5", 5}, {"$6", 6}, {"$7", 7}, {"$8", 8}, 
	{"$9", 9}, {"$10", 10}, {"$11", 11}, {"$12", 12}, {"$13", 13}, {"$14", 14}, {"$15", 15}, {"$16", 16}, 
	{"$17", 17}, {"$18", 18}, {"$19", 19}, {"$20", 20}, {"$21", 21}, {"$22", 22}, {"$23", 23}, {"$24", 24}, 
	{"$25", 25}, {"$26", 26}, {"$27", 27}, {"$28", 28}, {"$29", 29}, {"$30", 30}, {"$31", 31}
};

map<string, unsigned int> instructions = 
{
	{"addiu", 0x9}, {"addu", 0x0}, {"and", 0x0}, {"andi", 0xc}, {"beq", 0x4}, {"bne", 0x5}, {"j", 0x2}, {"jal", 0x3},
	{"jr", 0x0}, {"lui", 0xf}, {"lw", 0x23}, {"lb", 0x20}, {"nor", 0x0}, {"or", 0x0}, {"ori", 0xd}, {"sltiu", 0xb},
	{"sltu", 0x0}, {"sll", 0x0}, {"srl", 0x0}, {"sw", 0x2b}, {"sb", 0x28}, {"subu", 0x0}
};

map<string, unsigned int> R_format = 
{
	{"addu", 0x21}, {"and", 0x24}, {"jr", 0x8}, {"nor", 0x27}, {"or", 0x25}, {"sltu", 0x2b}, {"sll", 0x0}, {"srl", 0x2}, {"subu", 0x23}
};

vector<string> textLabel;

void parser(char* file, vector<string>& data, vector<string>& text);
void labelChecker(vector<string>& data, vector<string>& text, vector<string>& bin);
void pseudoTrans(vector<string>& data, vector<string>& text, vector<string>& bin);
void assembler(vector<string>& bin, vector<string>& data, vector<string>& text);
void binTransformer(vector<string>& bin, vector<string>& words);
string getBinData(long long int data, long long int num);

int main(int argc, char** argv)
{	
	if (argc != 2)
	{
		fprintf(stderr, "input is wrong...\n");
		return 1;
	}
	vector<string> data;
	vector<string> text;

	parser(argv[1], data, text);

	vector<string> bin;

	// Check label and data
	labelChecker(data, text, bin);

	pseudoTrans(data, text, bin);

	// Transform data, text to binary code
	assembler(bin, data, text);
	
	string name = argv[1];
	ofstream out(name.substr(0,name.find(".")) + ".o");
	for (int i = 0; i < bin.size(); i++)
	{
		long long int decimal_val = stoll(bin[i], 0, 2);
		out << hex << "0x" << decimal_val << endl;
	}
	out.close();

	return 0;
}

void parser(char* file, vector<string>& data, vector<string>& text)
{
	string s;
	int isData = 0;
	int isText = 0;

	ifstream fp(file);

	if (!fp.is_open())
	{
		cout << stderr << "can't read file...\n" << endl;
		exit(1);
	}

	while(getline(fp, s))
	{
		if (s.find(".data") != string::npos){
			isData = 1; 
			isText = 0;
			continue;
		}
		else if (s.find(".text") != string::npos){
			isData = 0; 
			isText = 1;
			continue;
		}

		if (isData)
			data.push_back(s);
		if (isText)
			text.push_back(s);
	}
	fp.close();
}

// Save label location & Delete label from data, text
void labelChecker(vector<string>& data, vector<string>& text, vector<string>& bin)
{
	long long int dataLoc = 0x10000000;
	long long int textLoc = 0x00400000;

	for (int i = 0; i < data.size(); i++)
	{
		istringstream ss(data[i]);
		string word;
		ss >> word;
		if (data[i].find(":")!=string::npos){
			string label = data[i].substr(0,data[i].find(":"));
			data_list.insert({label, dataLoc});
			// Case : ONLY LABEL
			if (data[i].find(":")+1 == strlen(data[i].c_str())){
				dataLoc -= 4;
				data.erase(data.begin() + i); i--;
			}
			// Case : LABEL With Instruction
			else{
				data[i] = data[i].substr(data[i].find(":")+1, strlen(data[i].c_str()));
			}
		}
		// Empty instruction Deletion
		else if (word.empty()){
			dataLoc -= 4;
			data.erase(data.begin() + i); i--;
		}
		dataLoc += 4;
	}

	for (int i = 0; i < text.size(); i++)
	{
		istringstream ss(text[i]);
		string word;
		ss >> word;
		// LABEL Exists
		if (text[i].find(":")!=string::npos){
			string label = text[i].substr(0,text[i].find(":"));
			data_list.insert({label, textLoc});
			textLabel.push_back(label);
			// Case : ONLY LABEL
			if (text[i].find(":")+1 == strlen(text[i].c_str())){
				textLoc -= 4;
			}
		}
		// Empty instruction Deletion
		else if (word.empty()){
			textLoc -= 4;
			text.erase(text.begin() + i); i--;
		}
		textLoc += 4;
	}
	bin.push_back(getBinData(textLoc - 0x00400000, 32));
	bin.push_back(getBinData(dataLoc - 0x10000000, 32));
}

void pseudoTrans(vector<string>& data, vector<string>& text, vector<string>& bin)
{
	int label_loc = 0;
	for (int i = 0; i < text.size(); i++)
	{
		// LABEL Exists
		if (text[i].find(":")!=string::npos){
			label_loc += 1;
			string label = text[i].substr(0,text[i].find(":"));
			// Case : ONLY LABEL
			if (text[i].find(":")+1 == strlen(text[i].c_str())){
				text.erase(text.begin() + i); i--;
			}
			// Case : LABEL With Instruction
			else{
				text[i] = text[i].substr(text[i].find(":")+1, strlen(text[i].c_str()));
				i--;
			}
		}
		else {
			istringstream ss(text[i]);
			string word;
			vector<string> words;
			while (ss >> word){
				if (word.find(",")!=string::npos)
					word = word.substr(0, word.find(","));
				words.push_back(word);
			}
			
			if (words[0] == "la"){
				text.erase(text.begin() + i);
				long long int temp = data_list[words[2]];

				long long int upper_part = temp >> 16;
				long long int lower_part = temp & 0xFFFF;

				text.insert(text.begin()+i, "lui " + words[1] + " " + "#" + words[2]);
				if (lower_part != 0){
					text.insert(text.begin()+i+1, "ori " + words[1] + " " + words[1] + " " + "#" + words[2]);
					for (int i = label_loc; i < textLabel.size(); i++){
						data_list[textLabel[i]] = data_list[textLabel[i]] + 4;
					}
					bin[0] = getBinData(stoi(bin[0], 0, 2) + 4, 32);
				}
			}
		}
	}
}

void assembler(vector<string>& bin, vector<string>& data, vector<string>& text)
{
	long long int textLoc = 0x00400000;
	
	for (int i = 0; i < text.size(); i++)
	{
		istringstream ss(text[i]);
		string word;
		vector<string> words;
		while (ss >> word){
			if (word.find(",")!=string::npos)
				word = word.substr(0, word.find(","));
			words.push_back(word);
		}
		
		if (words[0] == "beq" || words[0] == "bne"){
			// label과 현재 위치를 바탕으로 offset을 구해야한다.
			words.push_back(to_string(textLoc));
		}
		binTransformer(bin, words);

		textLoc += 4;
	}

	for (int i = 0; i < data.size(); i++)
	{
		istringstream ss(data[i]);
		string word;
		vector<string> words;
		while (ss >> word){
			words.push_back(word);
		}
	      	
		if (words[1].find("x") != string::npos){
			stringstream ss(words[1]);
  			long long int value;
  			ss >> hex >> value;
			
			bin.push_back(getBinData(value, 32));
		}
		else{
			bin.push_back(getBinData(stoi(words[1]), 32));
		}
	}
}

void binTransformer(vector<string>& bin, vector<string>& words)
{
	long long  int op;
	op = instructions[words[0]];

	// R format
	if (op == 0){
		// JR instruction
		if (words.size() == 2){
			string bin_code = getBinData(op, 6);
			bin_code += getBinData(data_list[words[1]], 5);
			bin_code += "000000000000000";
			bin_code += getBinData(R_format[words[0]], 6);
			bin.push_back(bin_code);
		}
		// Shift instruction (SLL, SRL)
		else if (words[0] == "sll" || words[0] == "srl"){
			string bin_code = getBinData(op, 6);
			bin_code += "00000";
			bin_code += getBinData(data_list[words[2]], 5);
			bin_code += getBinData(data_list[words[1]], 5);
			
			if (words[3].find("x") != string::npos){
				stringstream ss(words[3]);
  				long long int value;
  				ss >> hex >> value;
			
				bin_code += getBinData(value, 5);
			}
			else{
				bin_code += getBinData(stoi(words[3]), 5);
			}
			bin_code += getBinData(R_format[words[0]], 6);
			bin.push_back(bin_code);
		}
		// Other R format
		else{
			string bin_code = getBinData(op, 6);
			bin_code += getBinData(data_list[words[2]], 5);
			bin_code += getBinData(data_list[words[3]], 5);
			bin_code += getBinData(data_list[words[1]], 5);
			bin_code += "00000";
			bin_code += getBinData(R_format[words[0]], 6);
			bin.push_back(bin_code);
		}
	}	
	// J format
	else if (op <= 3){
		string bin_code = getBinData(op, 6);
		bin_code += getBinData(data_list[words[1]]/4, 26);
		bin.push_back(bin_code);
	}
	// I format
	else {
		if (words.size() == 5){
			string bin_code = getBinData(op, 6);
			bin_code += getBinData(data_list[words[1]], 5);
			bin_code += getBinData(data_list[words[2]], 5);
			bin_code += getBinData((data_list[words[3]] - 4 - stoi(words[4]))/4, 16);
			bin.push_back(bin_code);	
		}
		else if (words.size() == 4){	
			if (words[0] == "ori" && words[3].find("#") != string::npos){
				words[3] = to_string(data_list[words[3].substr(words[3].find("#")+1, strlen(words[3].c_str()))] & 0xFFFF);
			}
			string bin_code = getBinData(op, 6);
			bin_code += getBinData(data_list[words[2]], 5);
			bin_code += getBinData(data_list[words[1]], 5);
			if (words[3].find("x") != string::npos){
				stringstream ss(words[3]);
  				long long int value;
  				ss >> hex >> value;
			
				bin_code += getBinData(value, 16);
			}
			else {
				bin_code += getBinData(stoi(words[3]), 16);
			}
			bin.push_back(bin_code);
		}
		else if (words.size() == 3){
			if (words[2].find("(")!=string::npos){
				long long int offset = stoi(words[2].substr(0, words[2].find("(")));
				string bin_code = getBinData(op, 6);
				bin_code += getBinData(data_list[words[2].substr(words[2].find("(")+1,words[2].find(")")-words[2].find("(")-1)], 5);
				bin_code += getBinData(data_list[words[1]], 5);
				bin_code += getBinData(offset, 16);
				bin.push_back(bin_code);
			}
			// LUI instruction
			else {
				if (words[2].find("#") != string::npos){
					words[2] = to_string(data_list[words[2].substr(words[2].find("#")+1, strlen(words[2].c_str()))] >> 16);
				}
				string bin_code = getBinData(op, 6);
				bin_code += "00000";
				bin_code += getBinData(data_list[words[1]], 5);
				if (words[2].find("x") != string::npos){
					stringstream ss(words[2]);
					long long int value;
					ss >> hex >> value;
				
					bin_code += getBinData(value, 16);
				}
				else {
					bin_code += getBinData(stoi(words[2]), 16);
				}
				bin.push_back(bin_code);
			}
		}
	}
}

string getBinData(long long int data, long long int num)
{
	string s = "";

	for (int i = num-1; i >= 0; i--)
	{
		long long  int k = data >> i;
		if (k & 1){
			s += "1";
		}
		else{
			s += "0";
		}
	}
	return s;
}
