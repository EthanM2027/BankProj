#include <stdio.h>
#include <iostream>
#include <string>
#include <iomanip>
#include <sstream>  // for ostringstream
#include <limits> // for numeric_limits
#include <vector>


// This is the branch file for the Bank System project


using namespace std;

class bank
{
    char name[100], address[100], acc_type;
    float amount, temp;
    int account_number;
    static int account_count; // Static variable to keep track of the number of accounts
    string balance; //Is currently being used to put in the starting amount
    public:
        void open_account();
        void deposit_money();
        void withdraw_money();
        void display_account();
        int get_account_number() const { return account_number; }
};



//Need to get all number values as strings and convert them to digits when needed
//This is so I can make sure they dont unput 110s2q
//Also prevents the code looping
void bank :: open_account()
{
    cout << "Enter your full name: ";
    cin.ignore();
    cin.getline(name,100);
    cout << "Enter your address: ";
    cin.getline(address,100);
    do 
    {
        acc_type = ' ';
        cout << "What type of account do you want to create? Savings(s) or Checking(c): ";
        cin >> acc_type;
        acc_type = tolower(acc_type);
    } while (acc_type != 's' && acc_type != 'c');

///////////////////////////////////////////////////////////////////////////////////////
//This is still being crabby


    int count;
    do
    {
        count = 0;
        //cin.ignore();
        cin.ignore(numeric_limits<streamsize>::max(), '\n'); // Clear leftover input
        cout << "Enter amount you would like to deposit: ";
        getline(cin, balance); 

        for(int i = 0; i < balance.size(); i++)
        {
            if(balance[i] >= 'a' && balance[i] <= 'z')
            {
                cout << "Invalid Input\n";
            }
            else
            {
                count += 1;
            }
        }
    } while (count != balance.size());
///////////////////////////////////////////////////////////////////////////////////////////////

    account_number = account_count++;
    cout << "Your account number is: " << account_number << endl;

    cout << "Your account has been created \n";

}
void bank :: deposit_money()
{
    amount = 0.0;
    cout << "Enter deposit amount: ";
    cin >> amount;
    temp = stof(balance);


    ostringstream stream;
    stream << fixed << setprecision(2) << (temp + amount);
    balance = stream.str();

    //balance =  to_string(temp + amount);
    
    cout << "New total amount: " << balance;
}
void bank :: display_account()
{
    cout << "#############################################" << endl;
    cout << "Name: \t" << name << endl;
    cout << "Address: \t" << address << endl;
    if(acc_type == 's')
    {
        cout << "Account type: \t" << "Saving" << endl;
    }
    else
    {
        cout << "Account type: \t" << "Checking" << endl;
    }
    cout << fixed << setprecision(2); // Set formatting for float
    cout << "Amount balance: \t" << balance << endl;
    cout << "#############################################" << endl;
}
void bank :: withdraw_money()
{
    amount = 0.0;
    cout << "\nWithdraw: \n";
    cout << "Enter amount to withdraw: ";
    cin >> amount;
    temp = stof(balance);
    
    cout << fixed << setprecision(2); // Set formatting for float
    balance =  to_string(temp - amount);

    cout << "Now total amount left: " << balance;
}

// Function to find an account by account number
// Returns a pointer to the account if found, otherwise returns nullptr
bank* find_account(vector<bank>& accounts, int acct_num) {
    for (auto& acc : accounts) {
        if (acc.get_account_number() == acct_num) {
            return &acc;
        }
    }
    return nullptr;
}

int bank::account_count = 1000; // starting account number

int main()
{
    //cout << "Branch Test\n";
    int selection;
    bank obj;
    vector<bank> accounts;
    
    cout << "Welcome to the Bank System\n";
    cout << "-----------------------------------\n";
    do 
    {
        cout << "\n1) Open Account\n2) Deposit\n3) Withdraw\n4) Display\n5) Exit\nSelection: ";
        cin >> selection;

        if (selection == 1) 
        {
            bank new_acc;
            new_acc.open_account();
            accounts.push_back(new_acc);
        } 
        else if (selection >= 2 && selection <= 4) 
        {
            int acct_num;
            cout << "Enter your account number: ";
            cin >> acct_num;

            bank* acc = find_account(accounts, acct_num);
            if (!acc) {
                cout << "Account not found.\n";
                continue;
            }

            switch (selection) {
                case 2: acc->deposit_money(); break;
                case 3: acc->withdraw_money(); break;
                case 4: acc->display_account(); break;
            }
        }
        else if (selection == 5) 
        {
            cout << "Goodbye\n";
        } 
        else 
        {
            cout << "Invalid selection.\n";
        }
    } while (selection != 5);
    return 0;
}