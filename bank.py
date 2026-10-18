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


# Create a class to store customoer details

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
# Create a class to store bank account details

class Account:

    # Initialize the account object with the given details
    def __init__(self,account_number,customer_id,account_type,balance):
        self.account_number=account_number #public
        self.customer_id=customer_id #public
        self.account_type=account_type #public
        self.__balance=balance #private

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
        return self.__balance #it updated the balance

    # Create a method to withdraw money
    def withdraw(self,amount):

        # Check wheather the withdrawal amount is positive
        if amount <=0:
            raise ValueError('Withdrawal amount must be greater than zero.')

        # Check wheather enought balance is available
        if amount>self.__balance:
            raise ValueError('Insufficient account balance.')

        self.__balance -=amount #subtract the amount from the balance

        return self.__balance # it updated the balance

# Create a class to mange the entire bank

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

    # Register a new customer
    def register_cutomer(self,name,phone,email):

        # Generate a customer ID with three digits
        customer_id=f'Cust{self.next_customer_id:03d}'

        # create a customer object
        customer=Customer(customer_id,name,phone,email)

        # store the customer using their customer id
        self.customers[customer_id]=customer

        # Increase the customer ID counter by 1
        self.next_customer_id+=1

        # return the generated customer ID
        return customer_id

