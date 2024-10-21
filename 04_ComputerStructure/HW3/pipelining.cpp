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

class state_register
{
public:
    int Instr = 0;                  // 어떤 instruction인지 저장
    unsigned int NPC = 0;           // 다음으로 실행될 instruction의 PC 저장
    int rs = 0;                     // 해당 instruction의 rs
    int rt = 0;                     // 해당 instruction의 rt
    int IMM = 0;                    // 해당 instruction의 IMM
    int rd = 0;                     // 해당 instruction의 rd
    int ALU_OUT = 0;                // 해당 instruction의 ALU 연산의 결과
    unsigned int BR_TARGET = 0;     // BEQ, BNE에서 Branch할 주소
    int shamt = 0;                  // SLL, SRL에서 shift할 개수 (shamt)
    unsigned int cur_PC = 0;        // 현재 PC
    unsigned int ex_PC = 0;         // 이전 instruction의 PC
    int ALUcntrl = 0;               // ALU에서 어떤 연산을 할지에 대한 state(덧셈 or 뺄셈 or 그 외)
    int RegWrite = 0;               // Register에 Write을 할지에 대한 state
    int Branch = 0;                 // BEQ, BNE일 경우
    int BranchN = 0;                // BNE의 경우
    int MemWrite = 0;               // Memory에 Write할지에 대한 state
    int MemRead = 0;                // Memory를 Read할지에 대한 state
    int MemtoReg = 0;               // Memory -> Register에 대한 state
    int funct = 0;                  // ALU에서 어떤 연산을 할지에 대한 state(구체적)
    int RegWriteAddr = 0;           // register에 값을 저장해야할 때, register 주소
    int MemAddr = 0;                // LW, LB에서 접근할 메모리의 주소
    int RegData = 0;                // SW, SB에서 저장할 register의 값
    int MemData = 0;                // LW, LB하는 메모리의 값
    int rs_F = 0;                   // rs에 data forwarding할 value
    int rt_F = 0;                   // rt에 data forwarding할 value
    int forwardA = 0;               // data forwarding을 할지에 대한 state(rs)
    int forwardB = 0;               // data forwarding을 할지에 대한 state(rt)
    int Jump = 0;                   // Jump 여부에 대한 state
    int Store = 0;                  // data를 memory에 store할지의 state
    int Byte = 0;                   // 단위가 Byte단위일 경우 (LB, SB)
};

state_register Noop;
int endPC;
int PC = 0x400000;

int cycle(state_register& IF_ID, state_register& ID_EX, state_register& EX_MEM, state_register& MEM_WB, int& PC, vector<int>& reg, map<unsigned int, string>& memoryMap, bool taken);
void printPipePC(state_register& IF_ID, state_register& ID_EX, state_register& EX_MEM, state_register& MEM_WB, int& cycle_count, int final);
void stateInit(state_register& state, int& PC, vector<int>& reg, map<unsigned int, string>& memoryMap);
void stateTransfer(state_register& src_state, state_register& dst_state);

int main(int argc, char** argv)
{	
    // register & PC address initialization
    vector<int> reg(32);
    // int PC = 0x400000;

    string object_file = "";
    string addr1 = "";
    string addr2 = "";
    int exe_instruction = -1;
    bool printEveryTime = false;
    bool Always_taken = false;
    bool printPipeline = false;

    // Parsing Command
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
        else if (emulator_instruction == "-atp"){
            Always_taken = true;
        }
        else if (emulator_instruction == "-antp"){
            Always_taken = false;
        }
        else if (emulator_instruction == "-p"){
            printPipeline = true;
        }
        else{
            object_file = argv[i];
        }
    }

    // Input File Parsing
    vector<int> load_data;
    parser(object_file, load_data);

    // Memomry Mapping
    map<unsigned int, string> memoryMap;
    toMemory(load_data, memoryMap);

    int exe_num = 0;
    int cycle_count = 0;
    // int temp_PC = 0;
    endPC = 0x400000 + load_data[0];
    
    state_register IF_ID; state_register ID_EX; state_register EX_MEM; state_register MEM_WB;

    while(1){
        if (exe_instruction != 0){
            cycle_count += 1;
            exe_num += cycle(IF_ID, ID_EX, EX_MEM, MEM_WB, PC, reg, memoryMap, Always_taken);
        }
        
        if (printPipeline == true){
            printPipePC(IF_ID, ID_EX, EX_MEM, MEM_WB, cycle_count, 0);
        }

        if (printEveryTime == true){
            printReg(PC, reg);
            if (addr1 != ""){
                printMem(addr1, addr2, load_data, memoryMap);
            }
        }

        if (exe_num == exe_instruction || (IF_ID.cur_PC == 0 && ID_EX.cur_PC == 0 && EX_MEM.cur_PC == 0 && MEM_WB.cur_PC == 0 && MEM_WB.ex_PC == 0)){
            // print PipeStage
            state_register IF_ID_n; state_register ID_EX_n; state_register EX_MEM_n; state_register MEM_WB_n;
            stateTransfer(IF_ID, IF_ID_n); stateTransfer(ID_EX, ID_EX_n); stateTransfer(EX_MEM, EX_MEM_n); stateTransfer(MEM_WB, MEM_WB_n);
            vector<int> reg_n(32);
            int PC_n = PC;
            for (int i = 0; i < 32; i++){
                reg_n[i] = reg[i];
            }
            map<unsigned int, string> memoryMap_n;
            for (const auto& pair : memoryMap) {
                memoryMap_n[pair.first] = pair.second;
            }
            
            while (!(IF_ID.cur_PC == 0 && ID_EX.cur_PC == 0 && EX_MEM.cur_PC == 0 && MEM_WB.cur_PC == 0 && MEM_WB.ex_PC == 0)){
                cycle_count += 1;
                cycle(IF_ID, ID_EX, EX_MEM, MEM_WB, PC, reg, memoryMap, Always_taken);
            }
            printPipePC(IF_ID_n, ID_EX_n, EX_MEM_n, MEM_WB_n, cycle_count, 1);
        
            // print Register val & Memory
            printReg(PC_n, reg_n);
            if (addr1 != ""){
                printMem(addr1, addr2, load_data, memoryMap_n);
            }
            break;
        }
    }
	return 0;
}

int cycle(state_register& IF_ID, state_register& ID_EX, state_register& EX_MEM, state_register& MEM_WB, int& PC, vector<int>& reg, map<unsigned int, string>& memoryMap, bool taken)
{
    int instruction_exe = 0;
    if (MEM_WB.cur_PC != 0){
        instruction_exe = 1;
        EX_MEM.ex_PC = MEM_WB.cur_PC; // EX_MEM의 state register를 propagation하기 때문
    }

    // Data Hazard Forwarding
    if (EX_MEM.RegWrite == 1 && EX_MEM.RegWriteAddr != 0 && EX_MEM.RegWriteAddr == ID_EX.rs){
        ID_EX.forwardA = 1;
        ID_EX.rs_F = EX_MEM.ALU_OUT;
        // cout << "1. " << ID_EX.rs_F << endl;
    }
    if (EX_MEM.RegWrite == 1 && EX_MEM.RegWriteAddr != 0 && EX_MEM.RegWriteAddr == ID_EX.rt){
        ID_EX.forwardB = 1;
        ID_EX.rt_F = EX_MEM.ALU_OUT;
        // cout << "2. " << ID_EX.rt_F << endl;
    }
    if (MEM_WB.RegWrite == 1 && MEM_WB.RegWriteAddr != 0 && EX_MEM.RegWriteAddr != ID_EX.rs && MEM_WB.RegWriteAddr == ID_EX.rs){
        ID_EX.forwardA = 1;
        ID_EX.rs_F = MEM_WB.ALU_OUT;
        // cout << "3. " << ID_EX.rs_F << endl;
    }
    if (MEM_WB.RegWrite == 1 && MEM_WB.RegWriteAddr != 0 && EX_MEM.RegWriteAddr != ID_EX.rt && MEM_WB.RegWriteAddr == ID_EX.rt){
        ID_EX.forwardB = 1;
        ID_EX.rt_F = MEM_WB.ALU_OUT;
        // cout << "4. " << ID_EX.rt_F << endl;
    }
    if (MEM_WB.MemRead == 1 && MEM_WB.RegWrite == 1 && MEM_WB.RegWriteAddr != 0 && MEM_WB.RegWriteAddr == ID_EX.rs){
        ID_EX.forwardA = 1;
        ID_EX.rs_F = MEM_WB.MemData;
        // cout << "5. " << ID_EX.rs_F << endl;
    }
    if (MEM_WB.MemRead == 1 && MEM_WB.RegWrite == 1 && MEM_WB.RegWriteAddr != 0 && MEM_WB.RegWriteAddr == ID_EX.rt){
        ID_EX.forwardB = 1;
        ID_EX.rt_F = MEM_WB.MemData;
        // cout << "6. " << ID_EX.rt_F << endl;
    }
    if (MEM_WB.RegWrite == 1 && MEM_WB.RegWriteAddr != 0 && MEM_WB.MemRead == 1 && EX_MEM.MemWrite == 1 && MEM_WB.RegWriteAddr == EX_MEM.rt){
        EX_MEM.RegData = reg[MEM_WB.RegWriteAddr];
        if (MEM_WB.Byte == 1){
            EX_MEM.RegData = MEM_WB.MemData;
        }
    }

    // WB stage implementation
    if (MEM_WB.RegWrite == 1){
        if (MEM_WB.MemtoReg == 0){ // R format 연산한 값을 register에 저장
            reg[MEM_WB.RegWriteAddr] = MEM_WB.ALU_OUT;
        }
        else if (MEM_WB.MemtoReg == 1){
            reg[MEM_WB.RegWriteAddr] = MEM_WB.MemData;
        }
    }

    // Branch Hazard (Check prediction is right?)
    int temp = 0;
    if (MEM_WB.Branch == 1){
        if ((MEM_WB.NPC != EX_MEM.cur_PC) && !taken){
            PC = MEM_WB.NPC;
            temp = MEM_WB.cur_PC;
            stateTransfer(Noop, EX_MEM);
            stateTransfer(Noop, ID_EX);
            stateTransfer(Noop, IF_ID);
            // return instruction_exe;
        }
        if ((MEM_WB.NPC != ID_EX.cur_PC) && taken){
            PC = MEM_WB.NPC;
            temp = MEM_WB.cur_PC;
            stateTransfer(Noop, EX_MEM);
            stateTransfer(Noop, ID_EX);
            stateTransfer(Noop, IF_ID);
            // return instruction_exe;
        }
    }

    // MEM stage implementation (EX_MEM -> MEM_WB)
    if (EX_MEM.MemRead == 1){
        if (EX_MEM.Byte == 0){
            EX_MEM.MemData = fromHexToDeci(loadWord(EX_MEM.MemAddr, memoryMap));
        }
        else if (EX_MEM.Byte == 1){
            string s = loadWord(EX_MEM.MemAddr, memoryMap).substr(0,2);
            EX_MEM.MemData = fromBinToDeci(fromHexToDeci(s), 8, 1);
        }
    }
    else if (EX_MEM.MemWrite == 1){  // sw와 같은 instruction
        if (EX_MEM.Byte == 0){
            saveWord(EX_MEM.MemAddr, EX_MEM.RegData, memoryMap);
        }
        else if (EX_MEM.Byte == 1){
            string s = "";
            stringstream ss;
            string Hex_val;
            ss << hex << fromBinToDeci(EX_MEM.RegData, 8, false);
            s.append((2 - strlen(ss.str().c_str())), '0');
            s += ss.str();
            memoryMap[EX_MEM.MemAddr] = s;
        }
    }
    stateTransfer(EX_MEM, MEM_WB);

    // // Branch Hazard (Check prediction is right?)
    // if (EX_MEM.Branch == 1){
    //     if ((EX_MEM.NPC != ID_EX.cur_PC) && !taken){
    //         PC = EX_MEM.NPC;
    //         stateTransfer(Noop, EX_MEM);
    //         stateTransfer(Noop, ID_EX);
    //         stateTransfer(Noop, IF_ID);
    //         return instruction_exe;
    //     }
    //     if ((EX_MEM.NPC != IF_ID.cur_PC) && taken){
    //         PC = EX_MEM.NPC;
    //         stateTransfer(Noop, EX_MEM);
    //         stateTransfer(Noop, ID_EX);
    //         stateTransfer(Noop, IF_ID);
    //         return instruction_exe;
    //     }
    // }


    // LW Data Hazard
    if (EX_MEM.MemRead == 1 && (EX_MEM.RegWriteAddr == ID_EX.rs || EX_MEM.RegWriteAddr == ID_EX.rt) && ID_EX.Store == 0){
        stateTransfer(Noop, EX_MEM);
        return instruction_exe;
    }

    // EX stage implementation (ID_EX -> EX_MEM)
    int rs_val = reg[ID_EX.rs];
    int rt_val = reg[ID_EX.rt];
    if (ID_EX.forwardA == 1){
        rs_val = ID_EX.rs_F;
    }
    if (ID_EX.forwardB == 1){
        rt_val = ID_EX.rt_F;
    }
    if (ID_EX.ALUcntrl == 0){
        // LW & LB
        ID_EX.MemAddr = rs_val + ID_EX.IMM;
        // SW & SB
        if (ID_EX.Store == 1){
            ID_EX.RegData = rt_val;
        }
    }
    else if (ID_EX.ALUcntrl == 1){
        // BEQ & BNE
        if ((rs_val == rt_val && ID_EX.Branch == 1 && ID_EX.BranchN == 0) || (rs_val != rt_val && ID_EX.BranchN == 1)){
            ID_EX.NPC = ID_EX.cur_PC + 4 + 4*ID_EX.IMM;
        }
    }
    else if (ID_EX.ALUcntrl == 2){ // R, I type
        // ADDIU
        if (ID_EX.funct == 9){
            ID_EX.ALU_OUT = rs_val + ID_EX.IMM;
        }
        // ANDI
        else if (ID_EX.funct == 0xc){
            ID_EX.ALU_OUT = rs_val & ID_EX.IMM;
        }
        // LUI
        else if (ID_EX.funct == 0xf){
            ID_EX.ALU_OUT = (ID_EX.IMM << 16);
        }
        // ORI
        else if (ID_EX.funct == 0xd){
            ID_EX.ALU_OUT = rs_val | ID_EX.IMM;
        }
        // SLTIU
        else if (ID_EX.funct == 0xb){
            if (static_cast<unsigned int>(rs_val) < static_cast<unsigned int>(ID_EX.IMM)){
                ID_EX.ALU_OUT = 1;
            }
            else {
                ID_EX.ALU_OUT = 0;
            }
        }
        // ADDU
        else if (ID_EX.funct == 0x21){
            ID_EX.ALU_OUT = rs_val + rt_val;
        }
        // AND
        else if (ID_EX.funct == 0x24){
            ID_EX.ALU_OUT = rs_val & rt_val;
        }
        // JR // 수정 필요 ****************************************
        else if (ID_EX.funct == 8){
            ID_EX.NPC = rs_val;
        }
        // NOR
        else if (ID_EX.funct == 0x27){
            ID_EX.ALU_OUT = (~rs_val) & (~rt_val);
        }
        // OR
        else if (ID_EX.funct == 0x25){
            ID_EX.ALU_OUT = rs_val | rt_val;
        }
        // SLTU
        else if (ID_EX.funct == 0x2b){
            if (static_cast<unsigned int>(rs_val) < static_cast<unsigned int>(rt_val)){
                ID_EX.ALU_OUT = 1;
            }
            else {
                ID_EX.ALU_OUT = 0;
            }
        }
        // SLL
        else if (ID_EX.funct == 0){
            ID_EX.ALU_OUT = rt_val << ID_EX.shamt;
        }
        // SRL
        else if (ID_EX.funct == 2){
            ID_EX.ALU_OUT = static_cast<unsigned int>(rt_val) >> ID_EX.shamt;
        }
        // SUBU
        else if (ID_EX.funct == 0x23){
            ID_EX.ALU_OUT = rs_val - rt_val;
        }
    }
    stateTransfer(ID_EX, EX_MEM);

    // LW Data Hazard
    // if (ID_EX.MemRead == 1 && (ID_EX.RegWriteAddr == IF_ID.rs || ID_EX.RegWriteAddr == IF_ID.rt) && IF_ID.Store == 0){
    //     stateTransfer(Noop, ID_EX);
    //     return instruction_exe;
    // }

    // ID stage implementation (IF_ID -> ID_EX)
    long long int instruction = fromHexToDeci(loadWord(IF_ID.cur_PC, memoryMap));
    int op = fromBinToDeci((instruction >> 26), 6, false);
    IF_ID.Instr = op;
    // R format
    if (op == 0){
        IF_ID.ALUcntrl = 2;
        int funct = fromBinToDeci(instruction, 6, false);       IF_ID.funct = funct;
        int rs = fromBinToDeci((instruction>>21), 5, false);    IF_ID.rs = rs;
        int rt = fromBinToDeci((instruction>>16), 5, false);    IF_ID.rt = rt;
        int rd = fromBinToDeci((instruction>>11), 5, false);    IF_ID.rd = rd;  IF_ID.RegWriteAddr = rd;
        int shamt = fromBinToDeci((instruction>>6), 5, false);  IF_ID.shamt = shamt;
        if (funct != 8){
            IF_ID.RegWrite = 1; // JR instruction 제외 모든 instruction Regwrite 한다.
        }
        else {
            IF_ID.Jump = 1;
            unsigned int target = reg[IF_ID.rs];    IF_ID.BR_TARGET = target;
            // Jump Hazard
            // PC = IF_ID.BR_TARGET;
        }
    }
    // J format
    else if (op == 2 || op == 3){
        IF_ID.Jump = 1;
        if (op == 3){
            IF_ID.RegWrite = 1;
            IF_ID.RegWriteAddr = 31;
            IF_ID.ALU_OUT = IF_ID.cur_PC + 4;
        }
        unsigned int target = fromBinToDeci(instruction, 26, false) * 4;    IF_ID.BR_TARGET = target;
        // Jump Hazard    
        // PC = IF_ID.BR_TARGET;
        // if (PC+4 < 0x400000 || PC+4 >= endPC){
        //     PC = 0;
        // }
    }
    // I format
    else {
        IF_ID.ALUcntrl = 2;
        IF_ID.funct = IF_ID.Instr;
        if (op == 9 || op == 0xc || op == 0xf || op == 0xd || op == 0xb){
            IF_ID.RegWrite = 1;
        }
        else if (op == 4){   // Branch (beq, bne)
            IF_ID.Branch = 1;
            IF_ID.ALUcntrl = 1;
            if (taken){
                IF_ID.BR_TARGET = IF_ID.cur_PC + 4 + 4*fromBinToDeci(instruction, 16, true);
            }
        }
        else if (op == 5){
            IF_ID.Branch = 1;
            IF_ID.ALUcntrl = 1;
            IF_ID.BranchN = 1;
            if (taken){
                IF_ID.BR_TARGET = IF_ID.cur_PC + 4 + 4*fromBinToDeci(instruction, 16, true);
            }
        }
        else if (op == 0x23 || op == 0x20){ // Load (lw, lb)
            IF_ID.RegWrite = 1;
            IF_ID.ALUcntrl = 0;
            IF_ID.MemRead = 1;
            IF_ID.MemtoReg = 1;
            if (op == 0x20){
                IF_ID.Byte = 1;
            }
        }
        else if (op == 0x2b || op == 0x28){ // Store (sw, sb)
            IF_ID.ALUcntrl = 0;
            IF_ID.MemWrite = 1;
            IF_ID.Store = 1;
            if (op == 0x28){
                IF_ID.Byte = 1;
            }
        }
        int imm = fromBinToDeci(instruction, 16, true);         IF_ID.IMM = imm;
        int rs = fromBinToDeci((instruction>>21), 5, false);    IF_ID.rs = rs;
        int rt = fromBinToDeci((instruction>>16), 5, false);    IF_ID.rt = rt;  IF_ID.RegWriteAddr = rt;
    }
    stateTransfer(IF_ID, ID_EX);
        
    // Jump Hazard
    // if (ID_EX.Jump == 1){
    //     stateTransfer(Noop, IF_ID);
    //     return instruction_exe;
    // }
    if (EX_MEM.Jump == 1){
        stateTransfer(Noop, ID_EX);
        PC = EX_MEM.BR_TARGET;
    }

    // Branch Hazard
    if (EX_MEM.Branch == 1 && taken == true){
        PC = EX_MEM.BR_TARGET;  // 예측 PC로 바꿔야 함
        stateTransfer(Noop, ID_EX);
        stateInit(IF_ID, PC, reg, memoryMap);
        PC += 4;        // PC + 4 원래 state init에서 하는 동작
        return instruction_exe;
    }
    // Branch Prediction Failed!!
    if (temp != 0){
        MEM_WB.ex_PC = temp;
    }

    // IF stage implementation (PC -> IF_ID)
    stateInit(IF_ID, PC, reg, memoryMap);
    PC = IF_ID.NPC;

    // End of Cycle
    return instruction_exe;
}

void stateInit(state_register& state, int& PC, vector<int>& reg, map<unsigned int, string>& memoryMap)
{
    stateTransfer(Noop, state);
    state.NPC = PC;
    // if (PC+4 < 0x400000 || PC+4 >= endPC){
    //     state.NPC = 0;
    // }
    if (PC >= 0x400000 && PC < endPC){
        state.NPC = PC+4;
        state.cur_PC = PC;
        long long int instruction = fromHexToDeci(loadWord(state.cur_PC, memoryMap));
        int op = fromBinToDeci((instruction >> 26), 6, false);
        int rs = fromBinToDeci((instruction>>21), 5, false);    state.rs = rs;
        int rt = fromBinToDeci((instruction>>16), 5, false);    state.rt = rt;
        if (op == 0x2b || op == 0x28){ // Store (sw, sb)
            state.Store = 1;
        }
    }
}

void stateTransfer(state_register& src_state, state_register& dst_state)
{
    dst_state.Instr = src_state.Instr;
    dst_state.NPC = src_state.NPC;
    dst_state.rs = src_state.rs;
    dst_state.rt = src_state.rt;
    dst_state.IMM = src_state.IMM;
    dst_state.rd = src_state.rd;
    dst_state.ALU_OUT = src_state.ALU_OUT;
    dst_state.BR_TARGET = src_state.BR_TARGET;
    dst_state.shamt = src_state.shamt;
    dst_state.cur_PC = src_state.cur_PC;
    dst_state.ex_PC = src_state.ex_PC;
    dst_state.ALUcntrl = src_state.ALUcntrl;
    dst_state.RegWrite = src_state.RegWrite;
    dst_state.Branch = src_state.Branch;
    dst_state.BranchN = src_state.BranchN;
    dst_state.MemWrite = src_state.MemWrite;
    dst_state.MemRead = src_state.MemRead;
    dst_state.MemtoReg = src_state.MemtoReg;
    dst_state.funct = src_state.funct;
    dst_state.RegWriteAddr = src_state.RegWriteAddr;
    dst_state.MemAddr = src_state.MemAddr;
    dst_state.RegData = src_state.RegData;
    dst_state.MemData = src_state.MemData;
    dst_state.rs_F = src_state.rs_F;
    dst_state.rt_F = src_state.rt_F;
    dst_state.forwardA = src_state.forwardA;
    dst_state.forwardB = src_state.forwardB;
    dst_state.Jump = src_state.Jump;
    dst_state.Store = src_state.Store;
    dst_state.Byte = src_state.Byte;
}

void printPipePC(state_register& IF_ID, state_register& ID_EX, state_register& EX_MEM, state_register& MEM_WB, int& cycle_count, int final)
{
    if (final == 1){
        cout << "==== Completion Cycle: " << cycle_count << " ====" << endl << endl;
    }
    else{
        cout << "==== Cycle " << cycle_count << " ====" << endl << endl;
    }
    cout << "Current pipeline PC state :" << endl;
    cout << "{";
    if (IF_ID.cur_PC && IF_ID.cur_PC != 0){
        cout << fromDeciToHex(IF_ID.cur_PC);
    }
    cout << "|";
    if (ID_EX.cur_PC && ID_EX.cur_PC != 0){
        cout << fromDeciToHex(ID_EX.cur_PC);
    }
    cout << "|";
    if (EX_MEM.cur_PC && EX_MEM.cur_PC != 0){
        cout << fromDeciToHex(EX_MEM.cur_PC);
    }
    cout << "|";
    if (MEM_WB.cur_PC && MEM_WB.cur_PC != 0){
        cout << fromDeciToHex(MEM_WB.cur_PC);
    }
    cout << "|";
    if (MEM_WB.ex_PC && MEM_WB.ex_PC != 0){
        cout << fromDeciToHex(MEM_WB.ex_PC);
    }
    cout << "}" << endl << endl;
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

void printReg(int PC, vector<int> reg)
{
    cout << "Current register values :" << endl;
    cout << "------------------------------------" << endl;
    cout << "PC: " << fromDeciToHex(PC) << endl;
    cout << "Registers:" << endl;
    for (int i = 0; i < reg.size(); i++)
    {
        cout << "R" << i << ": " << fromDeciToHex(reg[i]) << endl;
    }
    cout << endl;
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
    cout << endl;
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