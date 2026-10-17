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

