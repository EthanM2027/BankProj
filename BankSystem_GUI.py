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

bank.save_all_accounts.argtypes = []
bank.save_all_accounts.restype = None

# --- Interactive Part ---
print("Welcome to Python GUI Bank System (using C++ backend)\n")

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

# 3) Menu for deposit/withdraw
while True:
    print("\nChoose an option:")
    print("1) Deposit Money")
    print("2) Withdraw Money")
    print("3) View Account Info")
    print("4) Exit")
    
    choice = input("Selection: ")
    
    if choice == '1':
        amount = input("Enter deposit amount: ").encode('utf-8')
        success = bank.deposit_money(acct_num, amount)
        print("Deposit success!" if success else "Deposit failed.")
    
    elif choice == '2':
        amount = input("Enter withdraw amount: ").encode('utf-8')
        success = bank.withdraw_money(acct_num, amount)
        print("Withdraw success!" if success else "Withdraw failed.")
    
    elif choice == '3':
        info = bank.get_account_info(acct_num).decode('utf-8')
        print("\nAccount Info:\n", info)
    
    elif choice == '4':
        print("Exiting...")
        bank.save_all_accounts()
        print("✅ All accounts saved to accounts.txt")
        break
    
    else:
        print("Invalid choice. Please try again.")
