#include <stdio.h>
#include <iostream>
#include <sstream>
#include <fstream>
#include <string>
#include <string.h>
#include <cstring>
#include <cmath>
#include <vector>
#include <map>
#include <iomanip>

using namespace std;

void parser(string file, vector<int>& load_data);
void toMemory(vector<int>& load_data, map<unsigned int, string>& memoryMap);
void emulate(int& PC, vector<int>& reg, map<unsigned int, string>& memoryMap);
void printReg(int PC, vector<int> reg);
void printMem(string addr1, string addr2, vector<int> load_data, map<unsigned int, string> memoryMap);
int fromBinToDeci(int data, int num, bool sign);
long long int fromHexToDeci(string value);
string fromDeciToHex(int value);
string loadWord(int address, map<unsigned int, string> memoryMap);
void saveWord(int address, int value, map<unsigned int, string>& memoryMap);

int main(int argc, char** argv)
{	
    // register & PC address initialization
    vector<int> reg(32);
    int PC = 0x400000;

    string object_file = "";
    string addr1 = "";
    string addr2 = "";
    int exe_instruction = -1;
    bool printEveryTime = false;

    for (int i = 1; i < argc; i++){
        string emulator_instruction = argv[i];
        if (emulator_instruction == "-m"){
            i++;
            string argv_val = argv[i];
            addr1 = argv_val.substr(0, argv_val.find(":"));
            addr2 = argv_val.substr(argv_val.find(":")+1);
        }
        else if (emulator_instruction == "-d"){
            printEveryTime = true;
        }
        else if (emulator_instruction == "-n"){
            exe_instruction = stoi(argv[++i]);
        }
        else{
            object_file = argv[i];
        }
    }

    vector<int> load_data;
    parser(object_file, load_data);

    map<unsigned int, string> memoryMap;

    toMemory(load_data, memoryMap);

    int exe_num = 0;
    
    // PC 언제 update ??????????
    while(1){
        int temp_PC = PC;
        if (exe_num != exe_instruction){
            emulate(PC, reg, memoryMap);
            exe_num += 1;
        }
        if (temp_PC == PC && exe_instruction != 0){
            PC += 4;
        }

        // 마지막 instruction이 실행된 이후에는 무조건 출력
        if (exe_num == exe_instruction || printEveryTime == true || PC < 0x400000 || PC >= 0x400000 + load_data[0]){
            printReg(PC, reg);
            cout << endl;
            if (addr1 != ""){
                printMem(addr1, addr2, load_data, memoryMap);
            }
            if (exe_num == exe_instruction || PC < 0x400000 || PC >= 0x400000 + load_data[0]){
                break;
            }
        }
    }

	return 0;
}

void parser(string file, vector<int>& load_data)
{
	string s;

	ifstream fp(file);

	if (!fp.is_open())
	{
		cout << stderr << "can't read file...\n" << endl;
		exit(1);
	}

	while(getline(fp, s))
	{
        load_data.push_back(fromHexToDeci(s));
	}
	fp.close();
}

void toMemory(vector<int>& load_data, map<unsigned int, string>& memoryMap)
{
    unsigned int dataLoc = 0x10000000;
    for (int i = 2 + load_data[0]/4; i < 2 + load_data[0]/4 + load_data[1]/4; i++)
    {
        saveWord(dataLoc, load_data[i], memoryMap);
        dataLoc += 4;
    }
    unsigned int textLoc = 0x00400000;
    for (int i = 2; i < 2 + load_data[0]/4; i++)
    {
        saveWord(textLoc, load_data[i], memoryMap);
        textLoc += 4;
    }
}

void emulate(int& PC, vector<int>& reg, map<unsigned int, string>& memoryMap)
{
    long long int instruction = fromHexToDeci(loadWord(PC, memoryMap));
    int op = fromBinToDeci((instruction >> 26), 6, false);
    
    // R format
    if (op == 0){
        int funct = fromBinToDeci(instruction, 6, false);
        int rs = fromBinToDeci((instruction>>21), 5, false);
        int rt = fromBinToDeci((instruction>>16), 5, false);
        int rd = fromBinToDeci((instruction>>11), 5, false);
        int shamt = fromBinToDeci((instruction>>6), 5, false);
        // ADDU
        if (funct == 0x21){
            reg[rd] = reg[rs] + reg[rt];
        }
        // AND
        else if (funct == 0x24){
            reg[rd] = reg[rs] & reg[rt];
        }
        // JR
        else if (funct == 8){
            PC = reg[rs];
        }
        // NOR
        else if (funct == 0x27){
            reg[rd] = (~reg[rs]) & (~reg[rt]);
        }
        // OR
        else if (funct == 0x25){
            reg[rd] = reg[rs] | reg[rt];
        }
        // SLTU
        else if (funct == 0x2b){
            if (static_cast<unsigned int>(reg[rs]) < static_cast<unsigned int>(reg[rt])){
                reg[rd] = 1;
            }
            else {
                reg[rd] = 0;
            }
        }
        // SLL
        else if (funct == 0){
            reg[rd] = reg[rt] << shamt;
        }
        // SRL
        else if (funct == 2){
            reg[rd] = static_cast<unsigned int>(reg[rt]) >> shamt;
        }
        // SUBU
        else if (funct == 0x23){
            reg[rd] = reg[rs] - reg[rt];
        }
    }
    // J format
    // J format에서 점프 하니까 PC를 한번더 +4 해줄 필요가 없다.
    else if (op <= 3){
        unsigned int target = fromBinToDeci(instruction, 26, false) * 4;
        // J
        if (op == 2){
            PC = target;
        }
        // JAL
        else if (op == 3){
            reg[31] = PC + 4;
            PC = target;
        }
    }
    // I format
    else{
        int imm = fromBinToDeci(instruction, 16, true);
        int rs = fromBinToDeci((instruction>>21), 5, false);
        int rt = fromBinToDeci((instruction>>16), 5, false);
        // ADDIU
        if (op == 9){
            imm = fromBinToDeci(instruction, 16, true);
            reg[rt] = reg[rs] + imm;
        }
        // ANDI
        else if (op == 0xc){
            reg[rt] = reg[rs] & imm;
        }
        // BEQ
        else if (op == 4){
            if (reg[rs] == reg[rt]){
                PC = PC + 4 + 4*imm;
            }
        }
        // BNE
        else if (op == 5){
            if (reg[rs] != reg[rt]){
                PC = PC + 4 + 4*imm;
            }
        }
        // LUI
        else if (op == 0xf){
            reg[rt] = (imm << 16);
        }
        // LW
        else if (op == 0x23){
            reg[rt] = fromHexToDeci(loadWord(reg[rs]+imm, memoryMap));
        }
        // LB
        else if (op == 0x20){
            string s = loadWord(reg[rs]+imm, memoryMap).substr(0,2);
            reg[rt] = fromBinToDeci(fromHexToDeci(s), 8, 1);
        }
        // ORI
        else if (op == 0xd){
            reg[rt] = reg[rs] | imm;
        }
        // SLTIU
        else if (op == 0xb){
            imm = fromBinToDeci(instruction, 16, true);
            if (static_cast<unsigned int>(reg[rs]) < static_cast<unsigned int>(imm)){
                reg[rt] = 1;
            }
            else {
                reg[rt] = 0;
            }
        }
        // SW
        else if (op == 0x2b){
            saveWord(reg[rs]+imm, reg[rt], memoryMap);
        }
        // SB
        else if (op == 0x28){
            string s = "";
            stringstream ss;
            string Hex_val;
            ss << hex << fromBinToDeci(reg[rt], 8, false);
            s.append((2 - strlen(ss.str().c_str())), '0');
            s += ss.str();
            memoryMap[reg[rs]+imm] = s;
        }
    }
}

void printReg(int PC, vector<int> reg)
{
    cout << "Current register values:" << endl;
    cout << "------------------------------------" << endl;
    cout << "PC: " << fromDeciToHex(PC) << endl;
    cout << "Registers:" << endl;
    for (int i = 0; i < reg.size(); i++)
    {
        cout << "R" << i << ": " << fromDeciToHex(reg[i]) << endl;
    }
}

void printMem(string addr1, string addr2, vector<int> load_data, map<unsigned int, string> memoryMap)
{
    cout << "Memory content [" << addr1 << ".." << addr2 << "]:" << endl;
    cout << "------------------------------------" << endl;
    int i = 0;
    for (i = fromHexToDeci(addr1); i+4 <= fromHexToDeci(addr2); i+=4)
    {
        string s = loadWord(i, memoryMap);
        cout << fromDeciToHex(i) << ": " << fromDeciToHex(fromHexToDeci(s)) << endl;
    }
    if (i == fromHexToDeci(addr2)){
        string s = loadWord(i, memoryMap);
        cout << fromDeciToHex(i) << ": " << fromDeciToHex(fromHexToDeci(s)) << endl;
    }
    else if (i < fromHexToDeci(addr2)){
        string s = loadWord(i, memoryMap).substr(0,2*(fromHexToDeci(addr2)-i+1));
        cout << fromDeciToHex(i) << ": " << fromDeciToHex(fromHexToDeci(s)) << endl;
    }
}

int fromBinToDeci(int data, int num, bool sign)
{
	string s = "";

	for (int i = num-1; i >= 0; i--)
	{
		int k = data >> i;
        if (i == num-1){
            if ((k & 1) && sign){
                s.append((32 - num), '1');
            }
            else{
                s.append((32 - num), '0');
            }
        }
		if (k & 1){
			s += "1";
		}
		else{
			s += "0";
		}
	}
    if (s[0] == '1'){
        s[0] = '0';
        return stoi(s, nullptr, 2) - pow(2,31);
    }
	return stoi(s, nullptr, 2);
}

long long int fromHexToDeci(string value)
{
    stringstream ss(value);
    long long int decimal_val;
    ss >> hex >> decimal_val;
    return decimal_val;
}

string fromDeciToHex(int value)
{
    stringstream ss;
    string Hex_val;
    ss << hex << value;
    Hex_val = "0x" + ss.str();
    return Hex_val;
}

string loadWord(int address, map<unsigned int, string> memoryMap)
{
    string s = "";
    for (int i = 0; i < 4; i++){
        if (memoryMap.find(address + i)!= memoryMap.end()){
            s += memoryMap[address + i];
        }
        else{
            s += "00";
        }
    }
    return s;
}

void saveWord(int address, int value, map<unsigned int, string>& memoryMap)
{
    string s = "";
    stringstream ss;
    string Hex_val;
    ss << hex << value;
    s.append((8 - strlen(ss.str().c_str())), '0');
    s += ss.str();
    for (int i = 0; i < 4; i++){
        memoryMap[address+i] = s.substr(2*i , 2);
    }
}