#=============================================================
# Project : Banking Transaction Management System 
# file:banking_system.py
#Description :This program handles customer registration, 
#              bank accounts, deposits, withdrawals, fund 
#              transfers, and saves records into a text file.
# =============================================================


import streamlit as st  # used to create web user interface
import random # used to generate random otp for secure transaction

# Streamlit user interface

st.title("🏦 Banking Transaction Management System") # Create a bank object if it doesn't already exist

# if 'bank' not in st.session_state:
    #  st.session_state.bank= Bank()

# bank=st.session_state.bank # Get the existing bank object

menu=[
    "Customer Registration",
    "Account Creation",
    "Deposit",
    "Withdrawal",
    "Fund Transfer",
    "Balance Enquiry",
    "Transaction History",
    "Account Closure"
]
choice= st.sidebar.selectbox('Select Module',menu)

# 1.Customer Registration
if choice =="Customer Registration":
    st.subheader('Customer Registration')  #display the heading

    # get the customer's name
    name=st.text_input('Enter Customer Name:') #collect the customer name
    phone=st.text_input('Enter Phone Number:') #collect the phone number
    email=st.text_input('Enter Email Address:') # collect the email address

    # register customer
    if st.button('Register Customer'): #display the button
        errors=[] # an empty list ot store validation errors

        if not name.strip(): # checks name is empty or contains only spaces
            errors.append('Please enter a valid name.') # display the error message
        if not phone.isdigit() or len(phone)!=10: # checks phone number is it 10 digit or not
            errors.append('Please enter a valid 10- digit phone number.')
        if "@" not in email or "." not in email: # checks the email contains @ symbol and dot
            errors.append('Please enter a valid email address.')

        if errors: # check whether any errors were found
            for error in errors:
                st.error(error) #display each error separately
        else:
            st.success('Customer registered sucessfully!') # display the succes message

            st.write('### Customer Details')
            st.write('Name:',name.strip())
            st.write('Phone:',phone)
            st.write('Email:',email.strip())