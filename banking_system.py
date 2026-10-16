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
    "Home",
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

# Home Page
if choice == 'Home':
    st.subheader('Welcome to the Banking Transaction Management System.')
    st.write(
        "This application helps users manage basic banking \n "
        "operations through a simple and user-friendly interface.\n\n"
        "Select a banking module from the sidebar to get started."
    )

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

 # 2.Account Creation
elif choice == "Account Creation":
    st.subheader('Account Creation')

    #get customer id
    customer_id=st.number_input(
        "Enter Customer ID:",
        min_value=1, #set the minimum vlaue to 1
        step=1 # + or - by 1
    )

    #select account type
    account_type=st.selectbox(
        "Select Account Type:",
        ["Savings Account","Current Account"] #provide account options
    )

    #get initial deposit amount
    initial_deposit=st.number_input(
        "Enter Initial Deposit Amount(₹):",
        min_value=0.0, #allow zero as the minimum deposit
        step=500.0 # + or - by 500
    )

    #create bank account
    if st.button('Create Account'):

        if initial_deposit <1000:
            st.error('Initial deposit must be at least ₹1,000.')
        else:
            st.success('Account created successflly!')

            st.write('### Account Details')
            st.write('Customer ID:',int(customer_id))
            st.write('Account Type:',account_type)
            st.write('Initial Deposit:',f'₹{initial_deposit:,.2f}')
# 3 Deposit
elif choice=='Deposit':
    st.subheader('Deposit')

    #get customer id
    customer_id=st.number_input(
        "Enter Customer ID:",
        min_value=1,
        step=1
    )

    # get deposit amount
    deposit_amount=st.number_input(
        "Enter Deposit Amount (₹):",
        min_value=0.0,
        step=500.0   
    )

    # Deposit money
    if st.button("Deposit Money"):

        if deposit_amount <=0:
            st.error("Deposit amount must be greater than ₹0.")
        else:
            st.success("Deposit details submitted successfully!")

            st.write('### Deposit Details')
            st.write('Customer ID:',int(customer_id))
            st.write('Deposit Amount:',f'₹{deposit_amount:,.2f}')
# 4 Withdrawal
elif choice == "Withdrawal":
    st.header('Withdrawal')

    # get customer id
    customer_id=st.number_input(
    "Enter Customer ID:",
    min_value=1,
    step=1
    )

    # Get withdrawal amount
    withdrawal_amount = st.number_input(
        "Enter Withdrawal Amount (₹):",
        min_value=0.0,
        step=500.0
    )

    # Withdrawal money
    if st.button('Withdraw Money'):

        if withdrawal_amount<=0:
            st.error('Withdrawal amount must be greater than ₹0.')
        else:
            st.success('Withdrawal details submitted successfully!')

            st.write('### Withdrawal Details')
            st.write('Customer ID:',int(customer_id))
            st.write('Withdrawal Amount:'f'₹{withdrawal_amount:,.2f}')

# 5 Fund Transfer
elif choice =='Fund Transfer':
    st.header('Fund Transfer')
    errors=[]

    #get sender customer id
    sender_id=st.number_input(
        'Enter Sender Customer ID:',
        min_value=1,
        step=1
    )
    # Get receiver customer ID
    receiver_id = st.number_input(
        "Enter Receiver Customer ID:",
        min_value=1,
        step=1
    )
    # get transfer amount
    transfer_amount=st.number_input(
        'Enter Transfer Amount (₹):',
        min_value=0.0,
        step=500.0
    )

    # transfer money
    if st.button('Transfer Money'):

        if sender_id == receiver_id:
            errors.append('Sender and receiver Ids must be different.')

        if transfer_amount<=0:
            errors.append('Transfer amount must be greater then ₹0.')

        if errors:
            for error in errors:
                st.error(error)
        
        else:
            st.success('Transfer details submitted successfully!')


            st.write('### Transfer Details')
            st.write('Sender Customer ID:',int(sender_id))
            st.write('Receiver Customer ID:',int(receiver_id))
            st.write('Transfer Amount:',f'₹{transfer_amount:,.2f}')

# 6 Balance Enquiry
elif choice== 'Balance Enquiry':
    st.subheader('Balance Enquiry')

    # get customer id
    customer_id = st.number_input(
    "Enter Customer ID:",
    min_value=1,
    step=1
)

    # Check account balance
    if st.button('Check Balance'):

        st.success('Balance enquiry submitted successfully!')

        st.write('### Account Details')
        st.write('Customer ID:',int(customer_id))

        st.info(
        "The actual account balance will be displayed "
        "when we connect the banking logic."
        )



   
