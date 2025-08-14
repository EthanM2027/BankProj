import ctypes
import sys
import os
import tkinter as tk
from tkinter import ttk, messagebox, simpledialog
from tkinter.font import Font

class BankSystemGUI:
    def __init__(self):
        """Initialize the bank system GUI with proper error handling"""
        self.bank = None
        self.root = None
        self.setup_gui()
        self.load_dll()
        self.setup_function_signatures()
        self.load_existing_accounts()
    
    def setup_gui(self):
        """Setup the main GUI window"""
        self.root = tk.Tk()
        self.root.title("🏦 Python Bank System")
        self.root.geometry("800x600")
        self.root.configure(bg='#2c3e50')
        
        # Set window icon and make it non-resizable initially
        try:
            self.root.iconbitmap('bank_icon.ico')  # Optional: add your own icon
        except:
            pass  # Icon file not found, continue without it
        
        self.root.minsize(700, 500)
        
        # Create main style
        self.style = ttk.Style()
        self.style.theme_use('clam')
        
        # Configure custom styles
        self.style.configure('Title.TLabel', 
                           font=('Arial', 20, 'bold'),
                           background='#2c3e50',
                           foreground='#ecf0f1')
        
        self.style.configure('Header.TLabel',
                           font=('Arial', 14, 'bold'),
                           background='#34495e',
                           foreground='#ecf0f1')
        
        self.style.configure('Custom.TButton',
                           font=('Arial', 11, 'bold'),
                           padding=10)
        
        # Setup the main interface
        self.setup_main_interface()
    
    def load_dll(self):
        """Load the bank.dll with error handling"""
        try:
            self.bank = ctypes.CDLL(r'C:\Users\ethan\OneDrive\CProjects\Git\BankProj\bank.dll')
            messagebox.showinfo("Success", "✅ Bank DLL loaded successfully!")
        except OSError as e:
            messagebox.showerror("Error", f"❌ Error loading bank.dll: {e}\nMake sure bank.dll is accessible.")
            self.root.destroy()
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
                messagebox.showinfo("Info", "✅ Existing accounts loaded from accounts.csv")
            else:
                messagebox.showinfo("Info", "ℹ️ No existing accounts found. Starting fresh.")
        except Exception as e:
            messagebox.showwarning("Warning", f"⚠️ Could not load accounts: {e}")
    
    def setup_main_interface(self):
        """Setup the main interface"""
        # Clear the window
        for widget in self.root.winfo_children():
            widget.destroy()
        
        # Main frame
        main_frame = tk.Frame(self.root, bg='#2c3e50')
        main_frame.pack(fill='both', expand=True, padx=20, pady=20)
        
        # Title
        title_label = tk.Label(main_frame, 
                             text="🏦 PYTHON BANK SYSTEM 🏦",
                             font=('Arial', 24, 'bold'),
                             bg='#2c3e50',
                             fg='#ecf0f1')
        title_label.pack(pady=(0, 10))
        
        subtitle_label = tk.Label(main_frame,
                                text="(Powered by C++ Backend)",
                                font=('Arial', 12),
                                bg='#2c3e50',
                                fg='#bdc3c7')
        subtitle_label.pack(pady=(0, 30))
        
        # Button frame
        button_frame = tk.Frame(main_frame, bg='#2c3e50')
        button_frame.pack(expand=True)
        
        # Buttons
        buttons = [
            ("📝 Create New Account", self.create_account_window, '#27ae60'),
            ("🔐 Access Existing Account", self.access_account_window, '#3498db'),
            ("📊 View Account Information", self.view_account_window, '#f39c12'),
            ("💾 Save All Accounts", self.save_accounts, '#9b59b6'),
            ("🚪 Exit", self.exit_application, '#e74c3c')
        ]
        
        for i, (text, command, color) in enumerate(buttons):
            btn = tk.Button(button_frame,
                          text=text,
                          command=command,
                          font=('Arial', 12, 'bold'),
                          bg=color,
                          fg='white',
                          relief='flat',
                          padx=20,
                          pady=15,
                          width=30,
                          cursor='hand2')
            btn.pack(pady=10)
            
            # Hover effects
            btn.bind("<Enter>", lambda e, b=btn, c=color: self.on_hover(b, self.lighten_color(c)))
            btn.bind("<Leave>", lambda e, b=btn, c=color: self.on_leave(b, c))
    
    def lighten_color(self, color):
        """Lighten a hex color for hover effect"""
        color_map = {
            '#27ae60': '#2ecc71',
            '#3498db': '#5dade2',
            '#f39c12': '#f4d03f',
            '#9b59b6': '#bb8fce',
            '#e74c3c': '#ec7063'
        }
        return color_map.get(color, color)
    
    def on_hover(self, button, color):
        """Handle button hover"""
        button.configure(bg=color)
    
    def on_leave(self, button, color):
        """Handle button leave"""
        button.configure(bg=color)
    
    def is_valid_amount(self, amt):
        """Validate if a string represents a valid monetary amount (Python version)"""
        decimal_count = 0
        
        # Check if string is empty
        if not amt:
            return False
        
        for ch in amt:
            # Check for alphabetic characters
            if ch.isalpha():
                return False
            
            # Count decimal points
            if ch == '.':
                decimal_count += 1
                if decimal_count > 1:
                    return False
            
            # Check for invalid characters (not digit and not decimal point)
            elif not ch.isdigit() and ch != '.':
                return False
        
        return True
    
    def validate_amount(self, amount_str):
        """Validate amount input using the new validation function"""
        if not amount_str.strip():
            return False, "Amount cannot be empty."
        
        # Use the C++ equivalent validation
        if not self.is_valid_amount(amount_str.strip()):
            return False, "Please enter a valid monetary amount (digits and at most one decimal point)."
        
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
    
    def create_account_window(self):
        """Create the account creation window"""
        account_window = tk.Toplevel(self.root)
        account_window.title("📝 Create New Account")
        account_window.geometry("500x600")
        account_window.configure(bg='#34495e')
        account_window.resizable(False, False)
        
        # Center the window
        account_window.transient(self.root)
        account_window.grab_set()
        
        # Main frame
        main_frame = tk.Frame(account_window, bg='#34495e')
        main_frame.pack(fill='both', expand=True, padx=30, pady=30)
        
        # Title
        title_label = tk.Label(main_frame,
                             text="📝 CREATE NEW ACCOUNT",
                             font=('Arial', 18, 'bold'),
                             bg='#34495e',
                             fg='#ecf0f1')
        title_label.pack(pady=(0, 30))
        
        # Entry fields
        fields = [
            ("Full Name:", "name"),
            ("Address:", "address"),
            ("Initial Deposit ($):", "balance")
        ]
        
        entries = {}
        
        for label_text, field_name in fields:
            # Label
            label = tk.Label(main_frame,
                           text=label_text,
                           font=('Arial', 12, 'bold'),
                           bg='#34495e',
                           fg='#ecf0f1')
            label.pack(anchor='w', pady=(10, 5))
            
            # Entry
            if field_name == "address":
                entry = tk.Text(main_frame,
                              height=3,
                              font=('Arial', 11),
                              relief='solid',
                              borderwidth=1)
            else:
                entry = tk.Entry(main_frame,
                               font=('Arial', 11),
                               relief='solid',
                               borderwidth=1,
                               width=40)
            
            entry.pack(fill='x', pady=(0, 5))
            entries[field_name] = entry
        
        # Account type frame
        type_frame = tk.Frame(main_frame, bg='#34495e')
        type_frame.pack(fill='x', pady=(10, 20))
        
        type_label = tk.Label(type_frame,
                            text="Account Type:",
                            font=('Arial', 12, 'bold'),
                            bg='#34495e',
                            fg='#ecf0f1')
        type_label.pack(anchor='w', pady=(0, 10))
        
        account_type = tk.StringVar(value='s')
        
        savings_radio = tk.Radiobutton(type_frame,
                                     text="💰 Savings Account",
                                     variable=account_type,
                                     value='s',
                                     font=('Arial', 11),
                                     bg='#34495e',
                                     fg='#ecf0f1',
                                     selectcolor='#2c3e50',
                                     activebackground='#34495e')
        savings_radio.pack(anchor='w', pady=2)
        
        checking_radio = tk.Radiobutton(type_frame,
                                      text="💳 Checking Account",
                                      variable=account_type,
                                      value='c',
                                      font=('Arial', 11),
                                      bg='#34495e',
                                      fg='#ecf0f1',
                                      selectcolor='#2c3e50',
                                      activebackground='#34495e')
        checking_radio.pack(anchor='w', pady=2)
        
        # Button frame
        button_frame = tk.Frame(main_frame, bg='#34495e')
        button_frame.pack(fill='x', pady=(20, 0))
        
        def create_account():
            # Get values
            name = entries['name'].get().strip()
            balance = entries['balance'].get().strip()
            
            if isinstance(entries['address'], tk.Text):
                address = entries['address'].get('1.0', tk.END).strip()
            else:
                address = entries['address'].get().strip()
            
            acc_type = account_type.get()
            
            # Validate inputs
            name_valid, name_error = self.validate_name(name)
            if not name_valid:
                messagebox.showerror("Error", name_error)
                return
            
            address_valid, address_error = self.validate_address(address)
            if not address_valid:
                messagebox.showerror("Error", address_error)
                return
            
            balance_valid, balance_error = self.validate_amount(balance)
            if not balance_valid:
                messagebox.showerror("Error", balance_error)
                return
            
            # Confirm creation
            acc_type_name = "Savings" if acc_type == 's' else "Checking"
            confirm_msg = f"Create account with:\n\nName: {name}\nAddress: {address}\nType: {acc_type_name}\nInitial Balance: ${float(balance):.2f}"
            
            if messagebox.askyesno("Confirm", confirm_msg):
                try:
                    account_number = self.bank.create_account(
                        name.encode('utf-8'),
                        address.encode('utf-8'),
                        ord(acc_type),
                        f"{float(balance):.2f}".encode('utf-8')
                    )
                    
                    success_msg = f"🎉 Account created successfully!\n\nAccount Number: {account_number}\nInitial Balance: ${float(balance):.2f}\nAccount Type: {acc_type_name}"
                    messagebox.showinfo("Success", success_msg)
                    account_window.destroy()
                    
                except Exception as e:
                    messagebox.showerror("Error", f"Failed to create account: {e}")
        
        # Buttons
        create_btn = tk.Button(button_frame,
                             text="✅ Create Account",
                             command=create_account,
                             font=('Arial', 12, 'bold'),
                             bg='#27ae60',
                             fg='white',
                             relief='flat',
                             padx=20,
                             pady=10,
                             cursor='hand2')
        create_btn.pack(side='left', padx=(0, 10))
        
        cancel_btn = tk.Button(button_frame,
                             text="❌ Cancel",
                             command=account_window.destroy,
                             font=('Arial', 12, 'bold'),
                             bg='#e74c3c',
                             fg='white',
                             relief='flat',
                             padx=20,
                             pady=10,
                             cursor='hand2')
        cancel_btn.pack(side='right')
    
    def access_account_window(self):
        """Create the account access window"""
        # First, get account number
        account_num = simpledialog.askinteger("Account Access", 
                                            "Enter your account number:",
                                            minvalue=1000,
                                            maxvalue=999999999)
        
        if not account_num:
            return
        
        # Check if account exists
        if not self.bank.account_exists(account_num):
            messagebox.showerror("Error", f"Account {account_num} not found.")
            return
        
        # Create account operations window
        operations_window = tk.Toplevel(self.root)
        operations_window.title(f"🔐 Account {account_num} Operations")
        operations_window.geometry("400x500")
        operations_window.configure(bg='#34495e')
        operations_window.resizable(False, False)
        
        # Center the window
        operations_window.transient(self.root)
        operations_window.grab_set()
        
        # Main frame
        main_frame = tk.Frame(operations_window, bg='#34495e')
        main_frame.pack(fill='both', expand=True, padx=30, pady=30)
        
        # Title
        title_label = tk.Label(main_frame,
                             text=f"Account {account_num}",
                             font=('Arial', 18, 'bold'),
                             bg='#34495e',
                             fg='#ecf0f1')
        title_label.pack(pady=(0, 30))
        
        # Operation buttons
        operations = [
            ("💰 Deposit Money", lambda: self.deposit_money_dialog(account_num), '#27ae60'),
            ("💸 Withdraw Money", lambda: self.withdraw_money_dialog(account_num), '#e67e22'),
            ("📊 View Account Details", lambda: self.display_account_info_dialog(account_num), '#3498db'),
            ("🔙 Close", operations_window.destroy, '#95a5a6')
        ]
        
        for text, command, color in operations:
            btn = tk.Button(main_frame,
                          text=text,
                          command=command,
                          font=('Arial', 12, 'bold'),
                          bg=color,
                          fg='white',
                          relief='flat',
                          padx=20,
                          pady=15,
                          width=25,
                          cursor='hand2')
            btn.pack(pady=10)
    
    def deposit_money_dialog(self, account_number):
        """Handle money deposit dialog"""
        amount = simpledialog.askstring("Deposit Money",
                                       f"Enter deposit amount for account {account_number}:")
        
        if not amount:
            return
        
        is_valid, error_msg = self.validate_amount(amount)
        if not is_valid:
            messagebox.showerror("Error", error_msg)
            return
        
        try:
            success = self.bank.deposit_money(account_number, amount.encode('utf-8'))
            if success:
                messagebox.showinfo("Success", f"✅ Successfully deposited ${amount} to account {account_number}!")
            else:
                messagebox.showerror("Error", "❌ Deposit failed. Please check the amount format.")
        except Exception as e:
            messagebox.showerror("Error", f"❌ Error during deposit: {e}")
    
    def withdraw_money_dialog(self, account_number):
        """Handle money withdrawal dialog"""
        amount = simpledialog.askstring("Withdraw Money",
                                       f"Enter withdrawal amount for account {account_number}:")
        
        if not amount:
            return
        
        is_valid, error_msg = self.validate_amount(amount)
        if not is_valid:
            messagebox.showerror("Error", error_msg)
            return
        
        try:
            success = self.bank.withdraw_money(account_number, amount.encode('utf-8'))
            if success:
                messagebox.showinfo("Success", f"✅ Successfully withdrew ${amount} from account {account_number}!")
            else:
                messagebox.showerror("Error", "❌ Withdrawal failed. Check amount or insufficient funds.")
        except Exception as e:
            messagebox.showerror("Error", f"❌ Error during withdrawal: {e}")
    
    def view_account_window(self):
        """Handle viewing account information window"""
        account_num = simpledialog.askinteger("View Account", 
                                            "Enter account number to view:",
                                            minvalue=1000,
                                            maxvalue=999999999)
        
        if account_num:
            self.display_account_info_dialog(account_num)
    
    def display_account_info_dialog(self, account_number):
        """Display account information in a dialog"""
        try:
            if not self.bank.account_exists(account_number):
                messagebox.showerror("Error", f"Account {account_number} not found.")
                return
            
            info = self.bank.get_account_info(account_number)
            if info:
                decoded_info = info.decode('utf-8')
                
                # Create info window
                info_window = tk.Toplevel(self.root)
                info_window.title(f"📋 Account {account_number} Information")
                info_window.geometry("500x400")
                info_window.configure(bg='#34495e')
                
                # Main frame
                main_frame = tk.Frame(info_window, bg='#34495e')
                main_frame.pack(fill='both', expand=True, padx=20, pady=20)
                
                # Title
                title_label = tk.Label(main_frame,
                                     text=f"📋 ACCOUNT {account_number} INFORMATION",
                                     font=('Arial', 16, 'bold'),
                                     bg='#34495e',
                                     fg='#ecf0f1')
                title_label.pack(pady=(0, 20))
                
                # Info text
                info_text = tk.Text(main_frame,
                                  font=('Consolas', 11),
                                  bg='#2c3e50',
                                  fg='#ecf0f1',
                                  relief='solid',
                                  borderwidth=1,
                                  state='normal')
                info_text.pack(fill='both', expand=True)
                
                info_text.insert('1.0', decoded_info)
                info_text.config(state='disabled')
                
                # Close button
                close_btn = tk.Button(main_frame,
                                    text="🔙 Close",
                                    command=info_window.destroy,
                                    font=('Arial', 12, 'bold'),
                                    bg='#95a5a6',
                                    fg='white',
                                    relief='flat',
                                    padx=20,
                                    pady=10,
                                    cursor='hand2')
                close_btn.pack(pady=(10, 0))
                
            else:
                messagebox.showerror("Error", f"Could not retrieve information for account {account_number}")
                
        except Exception as e:
            messagebox.showerror("Error", f"Error retrieving account info: {e}")
    
    def save_accounts(self):
        """Save all accounts to file"""
        try:
            self.bank.save_all_accounts()
            messagebox.showinfo("Success", "✅ All accounts saved to accounts.csv")
        except Exception as e:
            messagebox.showerror("Error", f"❌ Error saving accounts: {e}")
    
    def exit_application(self):
        """Handle application exit"""
        if messagebox.askyesno("Exit", "Save all accounts before exiting?"):
            try:
                self.save_accounts()
            except Exception as e:
                messagebox.showerror("Error", f"Could not save accounts: {e}")
        
        self.root.quit()
        self.root.destroy()
    
    def run(self):
        """Run the GUI application"""
        try:
            self.root.protocol("WM_DELETE_WINDOW", self.exit_application)
            self.root.mainloop()
        except KeyboardInterrupt:
            print("\n⚡ Program interrupted by user.")
            self.exit_application()
        except Exception as e:
            messagebox.showerror("Error", f"Unexpected error: {e}")

def main():
    """Main function"""
    try:
        bank_gui = BankSystemGUI()
        bank_gui.run()
    except Exception as e:
        if 'bank_gui' in locals():
            messagebox.showerror("Error", f"Unexpected error: {e}")
        else:
            print(f"Error initializing application: {e}")

if __name__ == "__main__":
    main()