#include <stdio.h>
#include <iostream>
#include <string>
#include <cstring>
#include <iomanip>
#include <sstream>  // for ostringstream
#include <limits> // for numeric_limits
#include <vector>
#include <fstream>


// This is the branch file for the Bank System project


using namespace std;

class bank
{
    string name, address, balance;
    char acc_type;
    int account_number;
    static int account_count; // Static variable to keep track of the number of accounts

    public:
        bank(const string& n, const string& addr, char type, const string& bal)
        {
            name = n;
            address = addr;
            acc_type = type;
            balance = bal;
            account_number = account_count++;
        }

        int get_account_num() const { return account_count; }
        
        //Needs to be run as a loop in py to read in any existing accounts
        string get_user_info() const
        {
            ostringstream info;
            info << "Account Number: " << account_number << "\n"
                 << "Name: " << name << "\n"
                 << "Address: " << address << "\n"
                 << "Account Type: " << (acc_type == 's' ? "Savings" : "Checking") << "\n"
                 << "Balance: " << balance;
            return info.str();
        }

        string out_user() const 
        {
            ostringstream out;
            out << account_number << "|" << name << "|" << address << "|" << acc_type << "|" << balance << "\n";
            out << "###END###\n"; // End of account marker
            return out.str();
        }
        
        bool deposit(const string& amount)
        {
            if(!isValidAmount(amount)) return false;
            float current = stof(balance);
            current += stof(amount);
            balance = toFixed(current);
            return true;
        }

        bool withdraw(const string& amount) 
        {
            if (!isValidAmount(amount)) return false;
            float current = stof(balance);
            float withdrawAmount = stof(amount);
            if (withdrawAmount > current) return false; // prevent overdraft
            current -= withdrawAmount;
            balance = toFixed(current);
            return true;
        }

        


    private:
        static bool isValidAmount(const string& amt) 
        {
            int decimal_count = 0;
            if (amt.empty()) return false;
            for (char ch : amt) 
            {
                if (isalpha(ch)) return false;
                if (ch == '.')
                {
                    decimal_count++;
                    if (decimal_count > 1) return false;
                } 
                else if (!isdigit(ch) && ch != '.')
                {
                    return false;
                }
            }
            return true;
        }
        static string toFixed(float value) 
        {
            ostringstream stream;
            stream << fixed << setprecision(2) << value;
            return stream.str();
        }
};

int bank::account_count = 1000;
static vector<bank> accounts;



extern "C" 
{

    // Create account and return account number
    __declspec(dllexport) int create_account(const char* name, const char* address, char type, const char* balance) 
    {
        accounts.emplace_back(name, address, type, balance);
        return accounts.back().get_account_num();
    }

    // Deposit money into account
    __declspec(dllexport) bool deposit_money(int account_number, const char* amount) 
    {
        for (auto& acc : accounts) {
            if (acc.get_account_num() == account_number) {
                return acc.deposit(amount);
            }
        }
        return false;
    }

    // Withdraw money from account
    __declspec(dllexport) bool withdraw_money(int account_number, const char* amount) 
    {
        for (auto& acc : accounts) {
            if (acc.get_account_num() == account_number) {
                return acc.withdraw(amount);
            }
        }
        return false;
    }

    // Get account info
    //Only gets the account info of the first account with the given account number
    //Needs to have a search function to find the account in py file
    __declspec(dllexport) const char* get_account_info(int account_number) 
    {
        for (auto& acc : accounts) {
            if (acc.get_account_num() == account_number) {
                static string info;
                info = acc.get_user_info();
                return info.c_str();
            }
        }
        return "Account not found.";
    }

    __declspec(dllexport) void save_all_accounts() 
    {
        ofstream outfile("accounts.txt");
        if (!outfile.is_open()) return;

        for (const auto& acc : accounts) {
            outfile << acc.out_user();
        }

        outfile.close();
    }


}