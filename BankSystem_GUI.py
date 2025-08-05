import ctypes

# Load the DLL
bank = ctypes.CDLL('./BankSystem.dll')

# Define function signatures
bank.create_account.argtypes = [ctypes.c_char_p, ctypes.c_char_p, ctypes.c_char, ctypes.c_char_p]
bank.create_account.restype = ctypes.c_int

bank.deposit_money.argtypes = [ctypes.c_int, ctypes.c_char_p]
bank.deposit_money.restype = ctypes.c_bool

bank.withdraw_money.argtypes = [ctypes.c_int, ctypes.c_char_p]
bank.withdraw_money.restype = ctypes.c_bool

bank.get_account_info.argtypes = [ctypes.c_int]
bank.get_account_info.restype = ctypes.c_char_p

bank.load_all_accounts.argtypes = []
bank.load_all_accounts.restype = None

bank.save_all_accounts.argtypes = []
bank.save_all_accounts.restype = None

bank.account_exists.argtypes = [ctypes.c_int]
bank.account_exists.restype = ctypes.c_bool


# --- Interactive Part ---
print("Welcome to Python GUI Bank System (using C++ backend)\n")

# Load existing accounts from file
bank.load_all_accounts()
print("✅ Accounts loaded from accounts.txt")



# 3) Menu for deposit/withdraw
while True:
    print("\nChoose an option:")
    print("1) Create New Account")
    print("2) Acces Existing Account")
    print("3) View Account Info")
    print("4) Exit")
    
    choice = input("Selection: ")
    
    if choice == '1':
        # 1) Ask user for account details
        name = input("Enter your full name: ").encode('utf-8')
        address = input("Enter your address: ").encode('utf-8')

        while True:
            acc_type = input("Enter account type (s for savings, c for checking): ").lower()
            if acc_type in ['s', 'c']:
                acc_type = acc_type.encode('utf-8')
                break
            else:
                print("Invalid choice. Please enter 's' or 'c'.")

        balance = input("Enter initial deposit amount: ").encode('utf-8')

        # 2) Create account using C++ DLL
        acct_num = bank.create_account(name, address, acc_type[0], balance)
        print(f"✅ Account created! Your account number is: {acct_num}\n")
        
    elif choice == '2':
        acct_num = int(input("Enter your account number: "))
        if not bank.account_exists(acct_num):
            print("❌ Account not found.")
            continue
        print(f"✅ Account {acct_num} found!")
        
        while True:
            action = input("Do you want to (d)eposit or (w)ithdraw or Exit").lower()
            if action in ['d', 'w', "Exit", "exit"]:
                if action == 'd':
                    amount = input("Enter deposit amount: ").encode('utf-8')
                    success = bank.deposit_money(acct_num, amount)
                    print("Deposit success!" if success else "Deposit failed.")
                    break
                elif action == 'w':
                    amount = input("Enter withdraw amount: ").encode('utf-8')
                    success = bank.withdraw_money(acct_num, amount)
                    print("Withdraw success!" if success else "Withdraw failed.")
                    break
                elif action.lower() == "exit":
                    print("Exiting to main menu...")
                    break
            else:
                print("Invalid choice")
        
    
    elif choice == '3':
        acct_num_search = input("Input account number to view info: ")
        info = bank.get_account_info(acct_num_search).decode('utf-8')
        print("\nAccount Info:\n", info)
    
    elif choice == '4':
        print("Exiting...")
        bank.save_all_accounts()
        print("✅ All accounts saved to accounts.txt")
        break
    
    else:
        print("Invalid choice. Please try again.")
