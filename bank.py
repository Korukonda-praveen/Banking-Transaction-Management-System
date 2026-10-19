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

        # To store all the registerd customers
        self.customers={}

        # To store all created bank accounts
        self.accounts={}

        # set the starting customer ID
        self.next_customer_id=1

        # Set the starting account number
        self.next_account_number=1001

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

        return account_number #it generates account number

    # 3. Deposit
    def deposit(self,account_number,amount):

        if account_number not in self.accounts: # it will check whether is exists or not
            raise ValueError('Account does not exist')

        account=self.accounts[account_number] #get the account object from the dicitionary

        updated_balance=account.deposit(amount) # it use the account class method and update the balance

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

        if account.get_balance() !=0:  # Check whether the account has a remaining balance
            raise ValueError('Withdraw the remaining balance before closing the account')

        del self.accounts[account_number]       # Remove the account from the bank's account dictionary

        return "Account closed sucessfully."
