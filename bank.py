# ==================================================
# Project Name: Banking Transaction Management System
# File Name: bank.py
# Purpose: Handle the backend logic of the banking system

# This file contains the classes and methods used
# to manage customers, bank accounts, and transactions.

# It handles customer details, account creation,
# deposits, withdrawals, and fund transfers.

# It also helps validate banking operations and
# manage account balances.

# Later, this file will be connected to banking_system.py
# to make the Streamlit application work with real data.
# ==================================================

import os #check wheather TXT files exist 

# # Class 1: Store customer details

class Customer:

    # Initialize the customer object with the given details
    def __init__(self,customer_id,name,phone,email):
        self.customer_id=customer_id  #public variable
        self.name=name #public variable
        self._phone=phone  #protected variable
        self.__email = email #private variable

    # Create a method to display customer details
    def display_details(self):

        # Display the public customer ID
        print('Customer ID:',self.customer_id)

        # Display the public customer name
        print('Customer name:',self.name)

        # Display the protected phone number
        print("Phone Number:", self._phone)

        # Display the private email address
        print("Email:", self.__email)


# Class 2: Manage an individual bank account

class Account:

    # Initialize the account object with the given details
    def __init__(self,account_number,customer_id,account_type,balance):
        self.account_number=account_number #public
        self.customer_id=customer_id #public
        self.account_type=account_type #public
        self.__balance=balance #private
        self.transaction_history=[]
        self.transaction_history.append(f"Account created with initial deposit: ₹{balance:.2f}")         # Record the initial account creation and deposit

    # Create a method to display the details
    def display_details(self):

        #Display the account number
        print('Account Number:',self.account_number)

        #Display the Customer ID
        print('Customer ID:',self.customer_id)

        # Display the account type
        print('Account Type:',self.account_type)

        #Display the account balance
        print(f'Account Balance: ₹{self.__balance:.2f}')

    # Create a method to check the balance
    def get_balance(self):
        return self.__balance #return the private balance

    # Create a method to deposit money
    def deposit(self,amount):
 
        if amount<=0: # it check the deposut amount is positive or not
            raise ValueError('Deposit amount must be greater than zero.')
        self.__balance += amount #it the deposit amount to the current balance
         # Record the successful deposit in transaction history
        self.transaction_history.append(
            f"Deposited: ₹{amount:.2f} | Balance: ₹{self.__balance:.2f}"
        )
        return self.__balance #it updated the balance

    # Create a method to withdraw money
    def withdraw(self,amount):

        # Check wheather the withdrawal amount is positive
        if amount <=0:
            raise ValueError('Withdrawal amount must be greater than zero.')

        # Check wheather enought balance is available
        if amount>self.__balance:
            raise ValueError('Insufficient account balance.')
         # Check whether the minimum balance of ₹1,000 is maintained
        if self.__balance - amount < 1000:
            raise ValueError('Minimum balance of ₹1,000 must be maintained.')

        self.__balance -=amount #subtract the amount from the balance
        
        # Record the successful withdrawal in transaction history
        self.transaction_history.append(
            f"Withdrawn: ₹{amount:.2f} | Balance: ₹{self.__balance:.2f}"
        )


        return self.__balance # it updated the balance
    
    def settle_for_closure(self):
        # Store the remaining balance
        remaining_balance = self.__balance

        # Empty the account balance
        self.__balance = 0

        # Record the final settlement
        self.transaction_history.append(
            f"Final settlement paid: ₹{remaining_balance:.2f}"
        )

        # Return the settled amount
        return remaining_balance


# child class 1 savings account
class SavingsAccount(Account):

 def __init__(self, account_number, customer_id,balance):
     super().__init__(account_number, customer_id, "Savings Account", balance)

# child class 2 current account
class CurrentAccount(Account):
    def __init__(self, account_number, customer_id, balance):
        super().__init__(account_number, customer_id,'Current Account', balance)


# Class 3: Manage the entire bank

class Bank:

    "Initialize the bank"
    def __init__(self):
        
        
        # Set the names of the TXT files used to store bank records
        
        self.customers_file = "customers.txt"
        
        self.accounts_file = "accounts.txt"
        
        self.transactions_file = "transactions.txt"
        
        self.closed_accounts_file = "closed_accounts.txt"

        # Create TXT files if they do not exist
        for file_name in [
            self.customers_file,
            self.accounts_file,
            self.transactions_file,
            self.closed_accounts_file
        ]:
            # Check whether the file already exists
            if not os.path.exists(file_name):

                # Create an empty TXT file
                with open(file_name, "w") as file:
                    pass


        # To store all the registerd customers
        self.customers={}

        # To store all created bank accounts
        self.accounts={}

        # Store closed accounts and their transaction histories
        self.closed_accounts = {}

        # set the starting customer ID
        self.next_customer_id=1

        # Set the starting account number
        self.next_account_number=1001


        # Load saved customer details
        self.load_customers()

        # Load saved active accounts
        self.load_accounts()

        # Load saved closed accounts
        self.load_closed_accounts()

        # Load transaction histories
        self.load_transactions()


     # 1. Customer Registration
    def register_customer(self,name,phone,email):

        # Generate a customer ID such as CUST001
        customer_id=f'Cust{self.next_customer_id:03d}'

        # create a customer object
        customer=Customer(customer_id,name,phone,email)

        # store the customer using their customer id
        self.customers[customer_id]=customer

        # Increase the customer ID counter by 1
        self.next_customer_id+=1

        # Save customer details in the TXT file
        self.save_customers()

        # return the generated customer ID
        return customer_id

    
    # 2. Account Creation
    def create_account(self,customer_id,account_type,initial_deposit):

        if customer_id not in self.customers: #it will check the customer is registered or not
            raise ValueError('Customer Id does not exist.')
 
        if account_type not in ['Savings Account','Current Account']: #it check account type valid or not
            raise ValueError('Invalid account type.')

        if initial_deposit <1000: #it check the deposit 1000 or less than 1000
            raise ValueError('Initial deposit must be at least ₹1,000')

        # Generate the next account number
        account_number=self.next_account_number
        # Create the correct account type
        
        if account_type == "Savings Account":
            account = SavingsAccount(
                account_number, customer_id, initial_deposit)
        elif account_type == "Current Account":
            account = CurrentAccount(
                account_number, customer_id, initial_deposit)


        self.accounts[account_number]=account #stores the account in the bank's account dictionary

        self.next_account_number+=1 #increase the account to for the next customer

        # Save account details in the TXT file
        self.save_accounts()

        self.save_transactions() # Save the initial transaction history

        
        return account_number #it generates account number

    # 3. Deposit
    def deposit(self,account_number,amount):

        if account_number not in self.accounts: # it will check whether is exists or not
            raise ValueError('Account does not exist')

        account=self.accounts[account_number] #get the account object from the dicitionary

        updated_balance=account.deposit(amount) # it use the account class method and update the balance

        self.save_accounts() # Save the updated account balance

        self.save_transactions()  # Save the transaction history

        return updated_balance  # Return the account balance after depositing the money

    # 4. Withdraw
    def withdraw(self,account_number,amount):

        if account_number not in self.accounts:# Check whether the given account number exists in the bank
            raise ValueError('Account does not exist.')

        # Get the account object using the account number
        account=self.accounts[account_number]

        # Call the withdraw method from the Account class
        # This checks the amount and available balance, then deducts the money     
        updated_balance=account.withdraw(amount)
        
        self.save_accounts() # Save the updated account balance

        self.save_transactions()  # Save the transaction history
        
        return updated_balance   # Return the account balance after withdrawing the money

    # 5. Fund Transfer
    def transfer_funds(self,sender_account, receiver_account,amount):

        # Check whether the sender's account exists
        if sender_account not in self.accounts:
            raise ValueError('Sender Account does not exist')

        # Check whether the receiver's account exists
        if  receiver_account not in self.accounts:
            raise ValueError('Receiver Account does not exist')
        
        # Prevent transferring money to the same account
        if sender_account==receiver_account:
            raise ValueError('Cannot transfer money to the same account.')

          # Check whether the transfer amount is positive
        if amount <= 0:
         raise ValueError("Transfer amount must be greater than zero.")

        # Get the sender's account object
        sender=self.accounts[sender_account]
        # Get the receiver's account object
        receiver=self.accounts[receiver_account]

        # Check whether the sender has enough money
        if amount > sender.get_balance():
            raise ValueError("Insufficient account balance.")

        #withdraw money from the sender account
        sender.withdraw(amount)

        # deposit the same money in the receiver account
        receiver.deposit(amount)
      
        self.save_accounts() # Save the updated account balance

        self.save_transactions()  # Save the transaction history

        return "Fund transfer successful" # a success message after the transfer

    # 6. Balance Enquiry
    def check_balance(self,account_number):

        if account_number not in self.accounts: # Check whether the given account number exists in the bank
            raise ValueError('Account does not exist')

        # Get the account object using the account number
        account=self.accounts[account_number]

        # Get the balance using the account class method
        balance=account.get_balance()

        return balance
        
    # 7. Transaction History
    def get_transaction_history(self,account_number):

        if account_number not in self.accounts:# Check whether the account number exists in the bank
            raise ValueError('Account does not exist.')

        account=self.accounts[account_number]    # Get the account object using the account number

        return account.transaction_history     # Return the transaction history stored in the account

    # 8. Account Closure
    def close_account(self,account_number):

        if account_number not in self.accounts:
            raise ValueError('Account does not exist.')

        account=self.accounts[account_number]

        # Settle the remaining balance and make it zero
        settlement_amount = account.settle_for_closure()
        
        # Record the account closure in its transaction history
        account.transaction_history.append('Account closed successfully.')

        # Save the closed account and its transaction history
        self.closed_accounts[account_number] = account

        del self.accounts[account_number] # Remove the account from the bank's account dictionary
 
        self.save_closed_accounts()# Save closed account details in the TXT file
        self.save_accounts()   # Save the updated active account records
        self.save_transactions()  # Save the transaction history
        return settlement_amount

    
    # Save customer details in a TXT file
    def save_customers(self):

        # Open the file to save customer details
        with open(self.customers_file, "w") as file:

            # Get each registered customer
            for customer in self.customers.values():

                # Write customer details into the file
                file.write(
                    f"{customer.customer_id}|"
                    f"{customer.name}|"
                    f"{customer._phone}|"
                    f"{customer._Customer__email}\n"
                )

    # Save account details in a TXT file
    def save_accounts(self):

        # Open the file to save account details
        with open(self.accounts_file, "w",encoding="utf-8") as file:

            # Get each active bank account
            for account in self.accounts.values():

                # Write account details into the file
                file.write(
                    f"{account.account_number}|"
                    f"{account.customer_id}|"
                    f"{account.account_type}|"
                    f"{account.get_balance()}\n"
                )


    # Save transaction histories in a TXT file
    def save_transactions(self):

        # Open the file to save transaction details
        with open(self.transactions_file, "w",encoding="utf-8") as file:

            # Combine active and closed accounts
            all_accounts = {
                **self.accounts,
                **self.closed_accounts
            }

            # Get each account
            for account in all_accounts.values():

                # Get each transaction from the account history
                for transaction in account.transaction_history:

                    # Write the account number and transaction details
                    file.write(
                        f"{account.account_number}|"
                        f"{transaction}\n"
                    )

      # Save closed account details in a TXT file
    def save_closed_accounts(self):

        # Open the file to save closed account details
        with open(self.closed_accounts_file, "w",encoding="utf-8") as file:

            # Get each closed account
            for account in self.closed_accounts.values():

                # Write the closed account details
                file.write(
                    f"{account.account_number}|"
                    f"{account.customer_id}|"
                    f"{account.account_type}|"
                    f"{account.get_balance()}\n"
                )


    # Load customer details from the TXT file
    def load_customers(self):

        # Open the customer file
        with open(self.customers_file, "r",encoding="utf-8") as file:

            # Read each line from the file
            for line in file:

                # Split customer details
                customer_id, name, phone, email = line.strip().split("|", 3)

                # Create a customer object
                customer = Customer(customer_id, name, phone, email)

                # Store the customer details
                self.customers[customer_id] = customer

         # Check whether any customers are registered
        if self.customers:

            # Get the highest customer ID, such as Cust003
            last_customer_id = max(self.customers)

            # Extract the number and set the next customer ID
            self.next_customer_id = int(last_customer_id[4:]) + 1


    
    # Load account details from the TXT file
    def load_accounts(self):

        # Open the account file
        with open(self.accounts_file, "r",encoding="utf-8") as file:

            # Read each account record
            for line in file:

                # Split account details
                account_number, customer_id, account_type, balance = line.strip().split("|", 3)

                # Convert account number and balance to numbers
                account_number = int(account_number)
                balance = float(balance)

                # Create the correct account object
                if account_type == "Savings Account":
                    account = SavingsAccount(account_number, customer_id, balance)
                else:
                    account = CurrentAccount(account_number, customer_id, balance)

                # Clear the default history before loading saved transactions
                account.transaction_history = []
                
                # Store the account in the dictionary
                self.accounts[account_number] = account
        
        
        # Set the starting account number
        self.next_account_number = 1001

        # Check active accounts
        if self.accounts:
            self.next_account_number = max(self.accounts) + 1

        # Check closed accounts
        if self.closed_accounts:
            self.next_account_number = max(
                self.next_account_number,
                max(self.closed_accounts) + 1
            )



     # Load transaction histories from the TXT file
    def load_transactions(self):

        # Open the transaction file
        with open(self.transactions_file, "r",encoding="utf-8") as file:

            # Read each transaction record
            for line in file:

                # Split the account number and transaction details
                account_number, transaction = line.strip().split("|", 1)

                # Convert account number into an integer
                account_number = int(account_number)

                # Find the account in active or closed accounts
                account = self.accounts.get(account_number)

                if account is None:
                    account = self.closed_accounts.get(account_number)

                # Add the transaction to the account history
                if account is not None:
                    account.transaction_history.append(transaction)

    
    # Load closed accounts from the TXT file
    def load_closed_accounts(self):

        # Open the closed accounts file
        with open(self.closed_accounts_file, "r",encoding="utf-8") as file:

            # Read each closed account record
            for line in file:

                # Split the account details
                account_number, customer_id, account_type, balance = line.strip().split("|", 3)

                # Convert values into numbers
                account_number = int(account_number)
                balance = float(balance)

                # Create the correct account object
                if account_type == "Savings Account":
                    account = SavingsAccount(account_number, customer_id, balance)
                else:
                    account = CurrentAccount(account_number, customer_id, balance)

                # Store the closed account
                self.closed_accounts[account_number] = account

                # Clear the default history before loading saved transactions
                account.transaction_history = []

