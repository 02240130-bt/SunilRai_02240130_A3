"""
Banking Application - CSF101 Assignment 3

This file is my attempt at a simple banking system. It lets you do basic stuff like
create accounts, deposit and withdraw money, transfer between accounts, delete accounts,
and even top up a phone number (like a SIM recharge). There's also a basic Tkinter GUI
if you don't want to use the console.

I tried to keep the code readable and added comments to explain what I was thinking , Its my first time trying to create a Banking Application,
it isn't my best work so I hope I did a decent job at it.

"""

import tkinter as tk

class InputError(Exception):
    """Raised when the user enters something that doesn't make sense (like a negative deposit)."""
    pass

class TransferError(Exception):
    """Raised when a transfer or withdrawal can't be completed (like insufficient funds)."""
    pass

class Account:
    """
    Represents a single bank account.
    Stores account number, owner's name, and balance.
    """
    def __init__(self, account_number, name, balance=0.0):
        self.account_number = account_number
        self.name = name
        self.balance = balance

    def deposit(self, amount):
        """ Only allow positive deposits """
        if amount <= 0:
            raise InputError("Deposit amount must be positive.")
        self.balance += amount

    def withdraw(self, amount):
        """ Only allow positive withdrawals and not more than available"""
        if amount <= 0:
            raise InputError("Withdraw amount must be positive.")
        if amount > self.balance:
            raise TransferError("Not enough funds for this withdrawal.")
        self.balance -= amount

class Bank:
    """
    This is the main bank system. It keeps track of accounts and phone top-ups.
    """
    def __init__(self):
        self.accounts = {}         
        self.phone_balances = {}   

    def create_account(self, account_number, name):
        """ Don't allow duplicate accounts """
        if account_number in self.accounts:
            raise InputError("Account already exists.")
        self.accounts[account_number] = Account(account_number, name)

    def delete_account(self, account_number):
        """ Remove account if it exists """
        if account_number not in self.accounts:
            raise InputError("Account does not exist.")
        del self.accounts[account_number]

    def transfer(self, from_acc, to_acc, amount):
        """ Check both accounts exist and amount is valid """
        if from_acc not in self.accounts or to_acc not in self.accounts:
            raise InputError("One or both accounts do not exist.")
        if amount <= 0:
            raise InputError("Transfer amount must be positive.")
        self.accounts[from_acc].withdraw(amount)
        self.accounts[to_acc].deposit(amount)

    def top_up_phone(self, phone_number, amount):
        """ Add to phone balance (create if not exists)"""
        if amount <= 0:
            raise InputError("Top-up amount must be positive.")
        if phone_number not in self.phone_balances:
            self.phone_balances[phone_number] = 0.0
        self.phone_balances[phone_number] += amount

def process_user_input(bank, choice):
    """
    Handles the user's menu choice and calls the correct bank method.
    Returns False if the user wants to exit, True otherwise.
    """
    try:
        if choice == '1':
            acc = input("Enter new account number: ")
            name = input("Enter account holder's name: ")
            bank.create_account(acc, name)
            print("Account created.")
        elif choice == '2':
            acc = input("Enter account number: ")
            amt = float(input("Enter deposit amount: "))
            bank.accounts[acc].deposit(amt)
            print("Deposited. New balance:", bank.accounts[acc].balance)
        elif choice == '3':
            acc = input("Enter account number: ")
            amt = float(input("Enter withdraw amount: "))
            bank.accounts[acc].withdraw(amt)
            print("Withdrawn. New balance:", bank.accounts[acc].balance)
        elif choice == '4':
            from_acc = input("From account: ")
            to_acc = input("To account: ")
            amt = float(input("Amount to transfer: "))
            bank.transfer(from_acc, to_acc, amt)
            print("Transferred. New balance:", bank.accounts[from_acc].balance)
        elif choice == '5':
            phone = input("Phone number: ")
            amt = float(input("Top-up amount: "))
            bank.top_up_phone(phone, amt)
            print("Phone top-up finished. New phone balance:", bank.phone_balances[phone])
        elif choice == '6':
            acc = input("Please enter account number to delete: ")
            bank.delete_account(acc)
            print("Account deleted.")
        elif choice == '0':
            print("Thank you for using the bank! Please come vist us again.")
            return False
        else:
            print("Nahh! That's not a valid option. Please try again.")
    except Exception as e:
        print("Error:", e)
    return True

def main():
    """
    This is the main loop for the console version of the banking app.
    """
    bank = Bank()
    while True:
        print("\n1. Create Account\n2. Deposit\n3. Withdraw\n4. Transfer\n5. Phone Top-up\n6. Delete Account\n0. Exit")
        choice = input("Enter your choice: ")
        if not process_user_input(bank, choice):
            break

class BankGUI:
    """
    Basic Tkinter GUI for the banking app that I created. It lets you do all main operations with buttons and entry fields.
    """
    def __init__(self, bank):
        self.bank = bank
        self.window = tk.Tk()
        self.window.title("Simple Bank")
        self.result = tk.StringVar()
        self.setup_ui()

    def setup_ui(self):
        tk.Label(self.window, text="Account Number:").grid(row=0, column=0)
        self.acc_entry = tk.Entry(self.window)
        self.acc_entry.grid(row=0, column=1)

        tk.Label(self.window, text="Name/Phone/To Acc:").grid(row=1, column=0)
        self.name_entry = tk.Entry(self.window)
        self.name_entry.grid(row=1, column=1)

        tk.Label(self.window, text="Amount:").grid(row=2, column=0)
        self.amt_entry = tk.Entry(self.window)
        self.amt_entry.grid(row=2, column=1)

        tk.Button(self.window, text="Create", command=self.create_account).grid(row=3, column=0)
        tk.Button(self.window, text="Deposit", command=self.deposit).grid(row=3, column=1)
        tk.Button(self.window, text="Withdraw", command=self.withdraw).grid(row=4, column=0)
        tk.Button(self.window, text="Transfer", command=self.transfer).grid(row=4, column=1)
        tk.Button(self.window, text="Top-up", command=self.topup).grid(row=5, column=0)
        tk.Button(self.window, text="Delete", command=self.delete_account).grid(row=5, column=1)
        tk.Label(self.window, textvariable=self.result).grid(row=6, columnspan=2)

    def create_account(self):
        acc = self.acc_entry.get()
        name = self.name_entry.get()
        try:
            self.bank.create_account(acc, name)
            self.result.set("Account created.")
        except Exception as e:
            self.result.set(str(e))

    def deposit(self):
        acc = self.acc_entry.get()
        try:
            amt = float(self.amt_entry.get())
            self.bank.accounts[acc].deposit(amt)
            self.result.set(f"Deposited. Balance: {self.bank.accounts[acc].balance}")
        except Exception as e:
            self.result.set(str(e))

    def withdraw(self):
        acc = self.acc_entry.get()
        try:
            amt = float(self.amt_entry.get())
            self.bank.accounts[acc].withdraw(amt)
            self.result.set(f"Withdrawn. Balance: {self.bank.accounts[acc].balance}")
        except Exception as e:
            self.result.set(str(e))

    def transfer(self):
        from_acc = self.acc_entry.get()
        to_acc = self.name_entry.get()
        try:
            amt = float(self.amt_entry.get())
            self.bank.transfer(from_acc, to_acc, amt)
            self.result.set(f"Transferred. Balance: {self.bank.accounts[from_acc].balance}")
        except Exception as e:
            self.result.set(str(e))

    def topup(self):
        phone = self.name_entry.get()
        try:
            amt = float(self.amt_entry.get())
            self.bank.top_up_phone(phone, amt)
            self.result.set(f"Phone top-up. Balance: {self.bank.phone_balances[phone]}")
        except Exception as e:
            self.result.set(str(e))

    def delete_account(self):
        acc = self.acc_entry.get()
        try:
            self.bank.delete_account(acc)
            self.result.set("Account deleted.")
        except Exception as e:
            self.result.set(str(e))

if __name__ == "__main__":
    #main()  
    """ To use the GUI, comment out the line above and uncomment below """
    BankGUI(Bank()).window.mainloop()
    



