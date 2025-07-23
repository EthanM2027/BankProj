#include <stdio.h>
#include <iostream>
#include <string>
#include <iomanip>
#include <sstream>  // for ostringstream
#include <limits> // for numeric_limits


using namespace std;

class bank
{
    char name[100], address[100], acc_type;
    float amount, temp;
    string balance; //Is currently being used to put in the starting amount
    public:
        void open_account();
        void deposit_money();
        void withdraw_money();
        void display_account();
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
int main()
{
    int selection;
    bank obj;

    do
    {
        cout << endl << "1) Open Account \n";
        cout << "2) Deposit Money \n";
        cout << "3) Withdraw Money \n";
        cout << "4) Display Account Balance \n";
        cout << "5) Exit \n";
        cout << "Select from the options above: ";
        cin >> selection;

        switch(selection)
        {
            case 1: cout << "\n1) Open Account \n";
            obj.open_account();
            break;
            case 2: cout << "\n2) Deposit Money \n";
            obj.deposit_money();
            break;
            case 3: cout << "\n3) Withdraw Money \n";
            obj.withdraw_money();
            break;
            case 4: cout << "\n4) Display Account Balance \n";
            obj.display_account();
            break;
            case 5: 
                cout << "\nGoodbye";
                break;
            default: cout << "Invalid Selection";
        }
    } while (selection != 5);
    return 0;
}