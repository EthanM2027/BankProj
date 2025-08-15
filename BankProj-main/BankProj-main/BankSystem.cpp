#include <stdio.h>
#include <iostream>
#include <string>
#include <cstring>
#include <iomanip>
#include <sstream>  // for ostringstream
#include <limits>   // for numeric_limits
#include <vector>
#include <fstream>

// This is the branch file for the Bank System project

using namespace std;

class bank
{
    string name, address, balance;
    char acc_type;
    int account_number;

    public:
        static int account_count; // Static variable to keep track of the number of accounts

        //Sets all of the variables for the account
        bank(const string& n, const string& addr, char type, const string& bal)
        {
            name = n;
            address = addr;
            acc_type = type;
            balance = bal;
            account_number = account_count++;
        }

        //Specific to the users account number
        int get_account_num() const { return account_number; }
        
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

        //Outputs the user info in a format that can be read back in
        string out_user() const 
        {
            ostringstream out;
            out << account_number << "," << name << "," << address << "," << acc_type << "," << balance << "\n";
            return out.str();
        }
        
        //Deposit money into account
        bool deposit(const string& amount)
        {
            if(!isValidAmount(amount)) return false;
            float current = stof(balance);
            current += stof(amount);
            balance = toFixed(current);
            return true;
        }

        //Withdraw money from account
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
        // Validate that the amount is a valid number (non-negative, numeric, at most one decimal point)
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
        // Convert float to string with 2 decimal places
        static string toFixed(float value) 
        {
            ostringstream stream;
            stream << fixed << setprecision(2) << value;
            return stream.str();
        }
};

// Initialize static member
int bank::account_count = 1000;
static vector<bank> accounts;

extern "C" 
{
    // Create account and returns the  account number
    __declspec(dllexport) int create_account(const char* name, const char* address, char type, const char* balance) 
    {
        accounts.emplace_back(name, address, type, balance);
        return accounts.back().get_account_num();
    }

    // Deposit money into account
    __declspec(dllexport) bool deposit_money(int account_number, const char* amount) 
    {
        for (auto& acc : accounts) 
        {
            if (acc.get_account_num() == account_number)
            {
                return acc.deposit(amount);
            }
        }
        return false;
    }

    // Withdraw money from account
    __declspec(dllexport) bool withdraw_money(int account_number, const char* amount) 
    {
        for (auto& acc : accounts)
        {
            if (acc.get_account_num() == account_number)
            {
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
        for (auto& acc : accounts) 
        {
            if (acc.get_account_num() == account_number) 
            {
                static string info;
                info = acc.get_user_info();
                return info.c_str();
            }
        }
        return "Account not found.";
    }

    __declspec(dllexport) void save_all_accounts() 
    {
        ofstream outfile("accounts.csv");
        if (!outfile.is_open()) return;

        for (const auto& acc : accounts)
        {
            outfile << acc.out_user();
        }

        outfile.close();
    }

    __declspec(dllexport) void load_all_accounts() 
    {
        ifstream infile("accounts.csv");
        if (!infile.is_open()) return;

        accounts.clear();
        string line;
        while (getline(infile, line)) 
        {
            if (line.empty()) continue;

            stringstream ss(line);
            string acc_num_str, name, address, type_str, balance;

            getline(ss, acc_num_str, ',');
            getline(ss, name, ',');
            getline(ss, address, ',');
            getline(ss, type_str, ',');
            getline(ss, balance, ',');

            char acc_type = type_str.empty() ? 's' : type_str[0];
            accounts.emplace_back(name, address, acc_type, balance);

            // Update account count correctly
            int acc_num = stoi(acc_num_str);
            if (acc_num >= bank::account_count) 
            {
                bank::account_count = acc_num + 1;
            }
        }
        infile.close();
    }


    __declspec(dllexport) bool account_exists(int account_number) 
    {
        for (auto& acc : accounts) {
            if (acc.get_account_num() == account_number) 
            {
                return true;
            }
        }
        return false;
    }

}