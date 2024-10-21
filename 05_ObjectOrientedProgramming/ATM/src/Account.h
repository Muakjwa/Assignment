#pragma once
#include <iostream>
#include <string>
#include "User.h"
#include "Bank.h"

class Bank;
class User;

using namespace std;

class Account{
private:
	User *user;
	Bank *bank;
	long long int accountNum;
	long long int cardNum;
	long long int balance = 0;
	int password;
	string accountHistory;

public:
	Account();
	Account(Bank* bank, User* user, long long int accountNum, long long int cardNum, int password);
	void deposit(int cash);
	long long int getBalance();
	void withdrawal(int cash);
	long long int getCardNum();
	long long int getAccountNum();
	string getUserName();
	string snapShot();
	int getPassword();
};