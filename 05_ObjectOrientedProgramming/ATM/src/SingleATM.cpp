#include <iostream>
#include <string>
#include "SingleATM.h"

using namespace std;

class Bank;
class ATM;

SingleATM::SingleATM(){
}

SingleATM::SingleATM(string SerialNum, Bank* primaryBank, bool bilingual){
	setBilingual(bilingual);
	setSerialNum(SerialNum);
	setPrimaryBank(primaryBank);
}