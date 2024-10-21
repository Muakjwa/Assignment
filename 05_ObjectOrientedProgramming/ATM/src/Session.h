#pragma once
#include <iostream>
#include <string>
#include <vector>
#include "Bank.h"
#include "ATM.h"

using namespace std;

class Session {
private:
	static int transNum;
	string sessionTransaction;
	string tempSessionTransaction;
	vector<string> transHistory;
public:
	Session();

	void addTransaction(string cardNum, int amount, Account* target_account, string cash_or_check);
	void addTransaction(string cardNum, int amount, Account* source_account);
	void addTransaction(string cardNum, int amount, Account* target_account, int fee);
	void addTransaction(string cardNum, int amount, Account* source_account, Account* target_account, int fee);
	string printTransaction();

	void sessionKorean(ATM* ChosenATM, Account* userAccount, string cardNum, bool isSub);
	int sessionDepositKorean(ATM* ChosenATM, Account* userAccount, string cardNum, bool isSub);
	int sessionWithDrawalKorean(ATM* ChosenATM, Account* userAccount, string cardNum, bool isSub, int& withdrawalNum);
	int sessionTransferKorean(ATM* ChosenATM, Account* userAccount, string cardNum, bool isSub);

	void sessionEnglish(ATM* ChosenATM, Account* userAccount, string cardNum, bool isSub);
	int sessionDepositEnglish(ATM* ChosenATM, Account* userAccount, string cardNum, bool isSub);
	int sessionWithDrawalEnglish(ATM* ChosenATM, Account* userAccount, string cardNum, bool isSub, int& withdrawalNum);
	int sessionTransferEnglish(ATM* ChosenATM, Account* userAccount, string cardNum, bool isSub);
};