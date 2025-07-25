#include <stdio.h>
#include <iostream>
#include <string>
#include <cstring>
#include <iomanip>
#include <sstream>  // for ostringstream
#include <limits> // for numeric_limits
#include <vector>
#include <fstream> // for file operations


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
        void save_to_file(ofstream& outfile) const;
        void load_from_file(ifstream& infile);
        static void load_accounts(vector<bank>& accounts);
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

void bank :: save_to_file(ofstream& outfile) const 
{
    outfile << account_number << '|'
            << name << '|'
            << address << '|'
            << acc_type << '|'
            << balance << '|';
    outfile << "###END###\n"; // End of record marker
    // Using '|' as a delimiter for fields
}

void bank :: load_from_file(ifstream& infile) 
{
    string line;
    getline(infile, line);

    if(line.empty() || line == "###END###") return; // Skip empty lines or end markers
    
    stringstream ss(line);
    string token;

    // Read account number
    getline(ss, token, '|');
    account_number = stoi(token);

    // Read name
    getline(ss, token, '|');
    strncpy(name, token.c_str(), sizeof(name));
    name[sizeof(name) - 1] = '\0'; // Ensure null termination

    // Read address
    getline(ss, token, '|');
    strncpy(address, token.c_str(), sizeof(address));
    address[sizeof(address) - 1] = '\0'; // Ensure null termination

    // Read account type
    getline(ss, token, '|');
    acc_type = token[0]; // Assuming single character for account type

    // Read balance
    getline(ss, balance, '|');

    // Consume the END marker
    getline(infile, line);
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

void bank :: load_accounts(vector<bank>& accounts) {
    ifstream infile("accounts.txt");
    int highest = 999;
    while (infile.peek() != EOF) {
        bank acc;
        acc.load_from_file(infile);
        if (acc.get_account_number() > highest)
            highest = acc.get_account_number();
        accounts.push_back(acc);
    }
    infile.close();
    bank::account_count = highest + 1;
}

int bank::account_count = 1000; // starting account number

int main()
{
    int selection;
    bank obj;
    vector<bank> accounts;

    /*Load existing accounts from file
    ifstream infile("accounts.txt");
    while (infile.peek() != EOF) {
        bank acc;
        acc.load_from_file(infile);
        accounts.push_back(acc);
    }
    infile.close();*/
    bank :: load_accounts(accounts);

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
            ofstream outfile("accounts.txt");
            for (const auto& acc : accounts) 
            {
                acc.save_to_file(outfile);
            }
            outfile.close();
        } 
        else 
        {
            cout << "Invalid selection.\n";
        }
    } while (selection != 5);
    return 0;
}