#pragma once
#include <iostream>
#include <string>
#include "Account.h"

using namespace std;

class Account;

#ifndef USER_H
#define USER_H
class User {
private:
	int accountCnt = 0;
	string name;

public:
	User();
	User(string UserName);
	string getUserName();
	void setAccountArr(Account account);
};
#endif