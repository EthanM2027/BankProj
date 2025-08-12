import ctypes
import sys
import os

class BankSystemGUI:
    def __init__(self):
        """Initialize the bank system GUI with proper error handling"""
        self.bank = None
        self.load_dll()
        self.setup_function_signatures()
        self.load_existing_accounts()
    
    def load_dll(self):
        """Load the bank.dll with error handling"""
        try:
            self.bank = ctypes.CDLL('./bank.dll')
            print("✅ Bank DLL loaded successfully!")
        except OSError as e:
            print(f"❌ Error loading bank.dll: {e}")
            print("Make sure bank.dll is in the same directory as this script.")
            input("Press Enter to exit...")
            sys.exit(1)
    
    def setup_function_signatures(self):
        """Define all function signatures for type safety"""
        # Create account
        self.bank.create_account.argtypes = [ctypes.c_char_p, ctypes.c_char_p, ctypes.c_char, ctypes.c_char_p]
        self.bank.create_account.restype = ctypes.c_int
        
        # Deposit money
        self.bank.deposit_money.argtypes = [ctypes.c_int, ctypes.c_char_p]
        self.bank.deposit_money.restype = ctypes.c_bool
        
        # Withdraw money
        self.bank.withdraw_money.argtypes = [ctypes.c_int, ctypes.c_char_p]
        self.bank.withdraw_money.restype = ctypes.c_bool
        
        # Get account info
        self.bank.get_account_info.argtypes = [ctypes.c_int]
        self.bank.get_account_info.restype = ctypes.c_char_p
        
        # Load accounts
        self.bank.load_all_accounts.argtypes = []
        self.bank.load_all_accounts.restype = None
        
        # Save accounts
        self.bank.save_all_accounts.argtypes = []
        self.bank.save_all_accounts.restype = None
        
        # Check if account exists
        self.bank.account_exists.argtypes = [ctypes.c_int]
        self.bank.account_exists.restype = ctypes.c_bool
    
    def load_existing_accounts(self):
        """Load existing accounts from file"""
        try:
            self.bank.load_all_accounts()
            if os.path.exists('accounts.csv'):
                print("✅ Existing accounts loaded from accounts.csv")
            else:
                print("ℹ️  No existing accounts found. Starting fresh.")
        except Exception as e:
            print(f"⚠️  Warning: Could not load accounts: {e}")
    
    def clear_screen(self):
        """Clear the console screen"""
        os.system('cls' if os.name == 'nt' else 'clear')
    
    def display_header(self):
        """Display the main header"""
        print("=" * 60)
        print("           🏦 PYTHON BANK SYSTEM 🏦")
        print("         (Powered by C++ Backend)")
        print("=" * 60)
    
    def validate_amount(self, amount_str):
        """Validate amount input"""
        if not amount_str.strip():
            return False, "Amount cannot be empty."
        
        try:
            amount = float(amount_str)
            if amount <= 0:
                return False, "Amount must be positive."
            if amount > 999999999:
                return False, "Amount is too large."
            return True, ""
        except ValueError:
            return False, "Please enter a valid number."
    
    def validate_name(self, name):
        """Validate name input"""
        if not name.strip():
            return False, "Name cannot be empty."
        if len(name.strip()) < 2:
            return False, "Name must be at least 2 characters long."
        if len(name.strip()) > 50:
            return False, "Name must be less than 50 characters."
        return True, ""
    
    def validate_address(self, address):
        """Validate address input"""
        if not address.strip():
            return False, "Address cannot be empty."
        if len(address.strip()) < 5:
            return False, "Address must be at least 5 characters long."
        if len(address.strip()) > 100:
            return False, "Address must be less than 100 characters."
        return True, ""
    
    def get_account_number_input(self):
        """Get and validate account number input"""
        while True:
            try:
                acc_input = input("Enter account number: ").strip()
                if not acc_input:
                    print("❌ Account number cannot be empty.")
                    continue
                
                acc_num = int(acc_input)
                if acc_num < 1000:
                    print("❌ Account number must be 1000 or greater.")
                    continue
                
                return acc_num
            except ValueError:
                print("❌ Please enter a valid account number (numbers only).")
    
    def create_account_menu(self):
        """Handle account creation with full validation"""
        print("\n" + "-" * 40)
        print("         📝 CREATE NEW ACCOUNT")
        print("-" * 40)
        
        # Get and validate name
        while True:
            name = input("Enter your full name: ").strip()
            is_valid, error_msg = self.validate_name(name)
            if is_valid:
                break
            print(f"❌ {error_msg}")
        
        # Get and validate address
        while True:
            address = input("Enter your address: ").strip()
            is_valid, error_msg = self.validate_address(address)
            if is_valid:
                break
            print(f"❌ {error_msg}")
        
        # Get account type
        while True:
            print("\nAccount Types:")
            print("  s - Savings Account")
            print("  c - Checking Account")
            acc_type = input("Enter account type (s/c): ").strip().lower()
            
            if acc_type in ['s', 'c']:
                acc_type_char = ord(acc_type)
                acc_type_name = "Savings" if acc_type == 's' else "Checking"
                break
            else:
                print("❌ Invalid choice. Please enter 's' for Savings or 'c' for Checking.")
        
        # Get and validate initial balance
        while True:
            balance_input = input("Enter initial deposit amount ($): ").strip()
            is_valid, error_msg = self.validate_amount(balance_input)
            if is_valid:
                balance = f"{float(balance_input):.2f}"
                break
            print(f"❌ {error_msg}")
        
        # Confirm account creation
        print(f"\n📋 Account Summary:")
        print(f"   Name: {name}")
        print(f"   Address: {address}")
        print(f"   Type: {acc_type_name}")
        print(f"   Initial Balance: ${balance}")
        
        confirm = input("\nCreate this account? (y/n): ").strip().lower()
        if confirm != 'y':
            print("❌ Account creation cancelled.")
            return
        
        # Create account
        try:
            account_number = self.bank.create_account(
                name.encode('utf-8'),
                address.encode('utf-8'),
                acc_type_char,
                balance.encode('utf-8')
            )
            
            print(f"\n🎉 SUCCESS! Account created!")
            print(f"📝 Your account number is: {account_number}")
            print(f"💰 Initial balance: ${balance}")
            print(f"📋 Account type: {acc_type_name}")
            
        except Exception as e:
            print(f"❌ Error creating account: {e}")
        
        input("\nPress Enter to continue...")
    
    def access_account_menu(self):
        """Handle accessing existing accounts"""
        print("\n" + "-" * 40)
        print("         🔐 ACCESS EXISTING ACCOUNT")
        print("-" * 40)
        
        acc_num = self.get_account_number_input()
        
        # Check if account exists
        if not self.bank.account_exists(acc_num):
            print(f"❌ Account {acc_num} not found.")
            input("Press Enter to continue...")
            return
        
        print(f"✅ Account {acc_num} found!")
        
        # Account operations menu
        while True:
            print(f"\n--- Account {acc_num} Operations ---")
            print("1. 💰 Deposit Money")
            print("2. 💸 Withdraw Money")
            print("3. 📊 View Account Details")
            print("4. 🔙 Back to Main Menu")
            
            action = input("Choose an option (1-4): ").strip()
            
            if action == '1':
                self.deposit_money(acc_num)
            elif action == '2':
                self.withdraw_money(acc_num)
            elif action == '3':
                self.display_account_info(acc_num)
            elif action == '4':
                print("🔙 Returning to main menu...")
                break
            else:
                print("❌ Invalid choice. Please enter 1, 2, 3, or 4.")
    
    def deposit_money(self, account_number):
        """Handle money deposit"""
        print(f"\n💰 Deposit Money to Account {account_number}")
        print("-" * 30)
        
        while True:
            amount_input = input("Enter deposit amount ($): ").strip()
            is_valid, error_msg = self.validate_amount(amount_input)
            if is_valid:
                break
            print(f"❌ {error_msg}")
        
        # Perform deposit
        try:
            success = self.bank.deposit_money(account_number, amount_input.encode('utf-8'))
            if success:
                print(f"✅ Successfully deposited ${amount_input} to account {account_number}!")
            else:
                print("❌ Deposit failed. Please check the amount format.")
        except Exception as e:
            print(f"❌ Error during deposit: {e}")
        
        input("Press Enter to continue...")
    
    def withdraw_money(self, account_number):
        """Handle money withdrawal"""
        print(f"\n💸 Withdraw Money from Account {account_number}")
        print("-" * 35)
        
        while True:
            amount_input = input("Enter withdrawal amount ($): ").strip()
            is_valid, error_msg = self.validate_amount(amount_input)
            if is_valid:
                break
            print(f"❌ {error_msg}")
        
        # Perform withdrawal
        try:
            success = self.bank.withdraw_money(account_number, amount_input.encode('utf-8'))
            if success:
                print(f"✅ Successfully withdrew ${amount_input} from account {account_number}!")
            else:
                print("❌ Withdrawal failed. Check amount or insufficient funds.")
        except Exception as e:
            print(f"❌ Error during withdrawal: {e}")
        
        input("Press Enter to continue...")
    
    def view_account_info_menu(self):
        """Handle viewing account information"""
        print("\n" + "-" * 40)
        print("         📊 VIEW ACCOUNT INFO")
        print("-" * 40)
        
        acc_num = self.get_account_number_input()
        self.display_account_info(acc_num)
        input("Press Enter to continue...")
    
    def display_account_info(self, account_number):
        """Display account information in a formatted way"""
        try:
            if not self.bank.account_exists(account_number):
                print(f"❌ Account {account_number} not found.")
                return
            
            info = self.bank.get_account_info(account_number)
            if info:
                decoded_info = info.decode('utf-8')
                print("\n" + "=" * 50)
                print("             📋 ACCOUNT INFORMATION")
                print("=" * 50)
                print(decoded_info)
                print("=" * 50)
            else:
                print(f"❌ Could not retrieve information for account {account_number}")
                
        except Exception as e:
            print(f"❌ Error retrieving account info: {e}")
    
    def save_accounts(self):
        """Save all accounts to file"""
        try:
            self.bank.save_all_accounts()
            print("✅ All accounts saved to accounts.csv")
        except Exception as e:
            print(f"❌ Error saving accounts: {e}")
    
    def main_menu(self):
        """Display and handle the main menu"""
        while True:
            self.clear_screen()
            self.display_header()
            print("\n📋 Main Menu:")
            print("1. 📝 Create New Account")
            print("2. 🔐 Access Existing Account")
            print("3. 📊 View Account Information")
            print("4. 💾 Save All Accounts")
            print("5. 🚪 Exit")
            print("\n" + "=" * 60)
            
            choice = input("Choose an option (1-5): ").strip()
            
            if choice == '1':
                self.create_account_menu()
            elif choice == '2':
                self.access_account_menu()
            elif choice == '3':
                self.view_account_info_menu()
            elif choice == '4':
                self.save_accounts()
                input("Press Enter to continue...")
            elif choice == '5':
                self.exit_application()
                break
            else:
                print("❌ Invalid choice. Please enter a number between 1 and 5.")
                input("Press Enter to continue...")
    
    def exit_application(self):
        """Handle application exit"""
        print("\n🚪 Exiting Bank System...")
        print("💾 Auto-saving all accounts...")
        self.save_accounts()
        print("👋 Thank you for using the Python Bank System!")
        print("💖 Have a great day!")

def main():
    """Main function"""
    try:
        bank_gui = BankSystemGUI()
        bank_gui.main_menu()
    except KeyboardInterrupt:
        print("\n\n⚡ Program interrupted by user.")
        print("💾 Attempting to save accounts...")
        try:
            bank_gui.save_accounts()
        except:
            print("⚠️  Could not save accounts.")
        print("👋 Goodbye!")
    except Exception as e:
        print(f"\n❌ Unexpected error: {e}")
        input("Press Enter to exit...")

if __name__ == "__main__":
    main()