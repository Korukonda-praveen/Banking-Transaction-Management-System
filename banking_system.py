#=============================================================
# Project : Banking Transaction Management System 
# file:banking_system.py
#Description :This program handles customer registration, 
#              bank accounts, deposits, withdrawals, fund 
#              transfers, and saves records into a text file.
# =============================================================


import streamlit as st  # used to create web user interface
import random # used to generate random otp for secure transaction

if 'customers' not in st.session_state: # Check whether the customers dictionary exists in the session state
    st.session_state.customers={}     # Create an empty dictionary to store customer details

if 'next_customer_id' not in st.session_state: # Check whether the next customer ID exists in the session state
    st.session_state.next_customer_id= 101   # Set the starting customer ID to 101

if "registered_customer_id" not in st.session_state: # Check whether the registered customer ID variable exists
    st.session_state.registered_customer_id = None  # Set it to None because no customer has been registered yet

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
    "Minimum Balance Validation",
    "Transaction History",
    "Account Closure"
]
if "module_menu" not in st.session_state:
# Check whether the current module menu exists
    st.session_state.module_menu = "Home"  # Set Home as the default module when the application starts

if "next_module" not in st.session_state:  # Check whether the next module variable exists
    st.session_state.next_module='Home'    # Set Home as the default next module

if st.session_state.next_module is not None: # Check whether a next module has been selected
    st.session_state.module_menu = st.session_state.next_module    # Change the current module to the selected next module
    st.session_state.next_module = None 
    # Reset the next module to None to avoid repeating the navigation

choice = st.sidebar.selectbox(
    "Select Module",
    menu,
    key="module_menu"
)


# Home Page
if choice == 'Home':
    st.subheader('Welcome to the Banking Transaction Management System.')
    st.write(
        "This application helps users manage basic banking \n "
        "operations through a simple and user-friendly interface.\n\n"
        "Select a banking module from the sidebar to get started."
    )

# 1.Customer Registration
elif choice =="Customer Registration":
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
            # Generate a customer ID
            customer_id = st.session_state.next_customer_id

            # Save customer details
            st.session_state.customers[customer_id] = {
                "name": name.strip(),
                "phone": phone,
                "email": email.strip()
            }

            # Save the registered customer ID
            st.session_state.registered_customer_id = customer_id

            # Prepare the next customer ID
            st.session_state.next_customer_id += 1

            st.success("Customer registered successfully!")

    # Display details after registration
    if st.session_state.registered_customer_id is not None: #check wheather a customer has been registered
        customer_id = st.session_state.registered_customer_id # get recently registered customer's ID
        customer = st.session_state.customers[customer_id]  #get the customer's details from the dictionary

        st.write("### Customer Details")
        st.write("Customer ID:", customer_id)
        st.write("Name:", customer["name"])
        st.write("Phone:", customer["phone"])
        st.write("Email:", customer["email"])

        # Proceed to Account Creation
        if st.button("Proceed to Account Creation"):
            st.session_state.next_module = "Account Creation" #request for the next process
            st.rerun() #Run the script again from the top


# 2. Account Creation
elif choice == "Account Creation":
    st.subheader("Account Creation")

    # Get all registered customer IDs
    customer_ids = st.session_state.customers.keys()

    # Check whether a customer is registered
    if not customer_ids:
        st.error("Please register a customer first.")

    else:
        # Select a registered customer ID
        customer_id = st.selectbox(
            "Select Customer ID:",
            customer_ids
        )

        # Get the selected customer's details
        customer = st.session_state.customers[customer_id]

        # Select account type
        account_type = st.selectbox(
            "Select Account Type:",
            ["Savings Account", "Current Account"]
        )

        # Get the initial deposit amount
        initial_deposit = st.number_input(
            "Enter Initial Deposit Amount (₹):",
            min_value=0.0,
            step=500.0
        )

        # Create the bank account
        if st.button("Create Account"):
            
            if initial_deposit < 1000:
                st.error("Initial deposit must be at least ₹1,000.")

            else:
                st.success("Account created successfully!")

                st.write("### Account Details")
                st.write("Customer ID:", customer_id)
                st.write("Account Type:", account_type)
                st.write("Initial Deposit:",f"₹{initial_deposit:,.2f}")
               

# 3 Deposit
elif choice=='Deposit':
    st.subheader('Deposit')

    #get customer id
    customer_id=st.number_input(
        "Enter Customer ID:",
        min_value=101,
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
    min_value=101,
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
            st.write('Withdrawal Amount:',f'₹{withdrawal_amount:,.2f}')

# 5 Fund Transfer
elif choice =='Fund Transfer':
    st.header('Fund Transfer')
    errors=[]

    #get sender customer id
    sender_id=st.number_input(
        'Enter Sender Customer ID:',
        min_value=101,
        step=1
    )
    # Get receiver customer ID
    receiver_id = st.number_input(
        "Enter Receiver Customer ID:",
        min_value=101,
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

        errors=[]

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
    min_value=101,
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


# 7 Minimum Balance Validation
elif choice =='Minimum Balance Validation':
    st.subheader("Minimum Balance Validation")

    # get customer id
    customer_id = st.number_input(
        'Enter Customer ID:',
        min_value=101,
        step=1
    )

    # Check minimum balance
    if st.button('Check Minimum Balance'):

        st.success('Minimum balance validation request submitted')


        st.write('### Account Details')
        st.write("Customer ID:", int(customer_id))


# 8 Transaction History
elif choice == 'Transaction History':
    st.subheader('Transaction History')

    # get customer id
    customer_id = st.number_input(
        'Enter Customer ID:',
        min_value=101,
        step=1
    ) 

    # get the Transaction History
    if st.button('Transaction History'):
        st.success('Transaction history request submitted successfully!')

        st.write('### Transaction Details')
        st.write('Customer ID:',int(customer_id))
    
# 9 Account Closure
elif choice == 'Account Closure':
    st.subheader('Account Closure')

    # get customer id
    customer_id =st.number_input(
        'Enter Customer ID:',
        min_value=101,
        step=1
    )

    # confirm account closure
    confirm_closure=st.checkbox(
        'I confirm that i want to close this account.'
    )

    # Close account
    if st.button('Close Account'):

        # check wheather the user confirmed
        if not confirm_closure:
            st.error('Please confirm before closing the account.')
        else:
            st.success('Account closure request submitted successfully!')

            st.write('### Account Closure Details')
            st.write('Customer ID:',int(customer_id))
