import ctypes

# Load the DLL
bank = ctypes.CDLL('./BankSystem.dll')

# Define the argument and return types of the C++ functions you plan to use
# For example, if you have:
# int create_account(const char* name, const char* address, char acc_type, const char* balance);

bank.create_account.argtypes = [ctypes.c_char_p, ctypes.c_char_p, ctypes.c_char, ctypes.c_char_p]
bank.create_account.restype = ctypes.c_int

bank.deposit_money.argtypes = [ctypes.c_int, ctypes.c_char_p]
bank.deposit_money.restype = ctypes.c_bool

bank.withdraw_money.argtypes = [ctypes.c_int, ctypes.c_char_p]
bank.withdraw_money.restype = ctypes.c_bool

bank.get_account_info.argtypes = [ctypes.c_int]
bank.get_account_info.restype = ctypes.c_char_p

# Test the integration
acct_num = bank.create_account(b"John Doe", b"123 Main St", b's', b"1000.00")
print("✅ Account created:", acct_num)

success = bank.deposit_money(acct_num, b"200.00")
print("Deposit success:", success)

success = bank.withdraw_money(acct_num, b"50.00")
print("Withdraw success:", success)

info = bank.get_account_info(acct_num).decode('utf-8')
print("Account info:\n", info)
