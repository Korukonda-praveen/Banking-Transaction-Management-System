#=============================================================
# Project : Banking Transaction Management System 
# file:banking_system.py
#Description :This program handles customer registration, 
#              bank accounts, deposits, withdrawals, fund 
#              transfers, and saves records into a text file.
# =============================================================


import streamlit as st  # used to create web user interface
from bank import Bank  # Import the backend Bank class

if "registered_customer_id" not in st.session_state: # Check whether the registered customer ID variable exists
    st.session_state.registered_customer_id = None  # Set it to None because no customer has been registered yet

# Function to navigate to Customer Registration
def go_to_customer_registration():
    st.session_state.module_menu = "Customer Registration"

# Navigate to the Account Creation module
def go_to_account_creation():
    st.session_state.module_menu = "Account Creation"

if 'bank' not in st.session_state: # Initialize the Bank in session state so it doesn't reset on every click
      st.session_state.bank= Bank()

bank=st.session_state.bank # Use st.session_state.bank instead of just 'bank' throughout your code

# Streamlit user interface
st.title("🏦 Banking Transaction Management System") # Create a bank object if it doesn't already exist
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
    st.session_state.next_module=None    # Set Home as the default next module


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
    st.title('🏦 Welcome to Digital Banking') #Display the welcome heading
    # Display a short instroduction
    st.write(
        'Welcome to the Banking Transaction Management System!'
        'Manage customers,accounts and transactions in one place'
    )
    st.divider()

    # Dispaly project information
    st.subheader('📌 About Our Project')

    st.write(
        'This project is developed using Python and Streamlit.'
        'It demonstrates object-oriented programming,Validation,'
        'Exception handling and banking operations'
    )

    st.divider()

    # Display available banking services
    st.subheader('💳 Our Banking Services')

    # create two columns to display the services
    col1,col2=st.columns(2)

    # Display the first three serives in the first column
    with col1:
        st.info('👤 Customer Registration')
        st.info('🏦 Account Creation')
        st.info('💰 Deposit and Withdrawal')

    # Display the remaining services in the second column
    with col2:
        st.info('🔁 Fund Transfer')
        st.info('📊 Balance Enquiry')
        st.info('📜 Transaction History')
        st.info('🚪 Account Closure')

    st.divider()

    # Display a remider message
    st.success(
        'Ready to mange your banking operations..?'
        'Click the button below to get started'
    )

    # Create the get started button
    if st.button('🚀 Get Started',type='primary',on_click=go_to_customer_registration):

        st.rerun() # Refresh the page to open Customer Registration
     # Display the project technologies
    
    st.caption(
        "Developed using Python | Streamlit | Object-Oriented Programming"
    )


# 1.Customer Registration
elif choice =="Customer Registration":
    st.subheader('Customer Registration')  #display the heading

    # get the customer's details
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

            try:
                # Register the customer using the backend
                customer_id = bank.register_customer(
                    name.strip(),
                    phone,
                    email.strip())

                # Save the registered customer ID
                st.session_state.registered_customer_id = customer_id

                st.success("Customer registered successfully!")

            except(ValueError,TypeError,KeyError) as error:   # Catch unexpected errors during registration
                st.error(f'Registration failed:{error}')

        # Display the latest registered customer's details
        customer_id=st.session_state.registered_customer_id

        if customer_id is not None and customer_id in bank.customers:
            customer=bank.customers[customer_id]
        
        st.write("### Customer Details")
        st.write("Customer ID:", customer_id)
        st.write("Name:", customer.name)
        st.write("Phone:", customer._phone)
        st.write("Email:", customer._Customer__email)

        # Create the Proceed to Account Creation button
        st.button("➡️ Proceed to Account Creation",type="primary",on_click=go_to_account_creation)





# 2. Account Creation
elif choice == "Account Creation":
    st.subheader("Account Creation")

    # Check whether a customer is registered
    if not bank.customers:
        st.warning("Please register a customer first.")

    else:
          # Select a registered customer
        customer_id = st.selectbox(
            "Select Customer ID:",
            list(bank.customers.keys()),
            key="account_creation_customer_id") # Give this input box a unique name

        # Check whether the customer ID exists in the bank's customer dictionary
        if customer_id in bank.customers:

         # Get the selected customer's details
            customer = bank.customers[customer_id]
        
        
         # Display customer details
            st.write("Name:", customer.name)
            st.write("Phone:", customer._phone)
            st.write("Email:", customer._Customer__email)

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

                try:
                    account_number = bank.create_account(
                    customer_id,
                    account_type,
                    initial_deposit)

                    
                    st.success("Account created successfully!")

                    st.write("### Account Details")
                    st.write("Customer ID:", customer_id)
                    st.write("Account Type:", account_type)
                    st.write("Initial Deposit:",f"₹{initial_deposit:,.2f}")
                except ValueError as error:
                    st.error(str(error))  





# 3 Deposit
elif choice=='Deposit':
    st.subheader('Deposit')

    # Check whether bank accounts exist
    if not bank.accounts:
        st.warning("Please create a bank account first.")
    
    else:  
       # Select the account number
        account_number = st.selectbox(
            "Select Account Number:",
            list(bank.accounts.keys()),key="deposit_account") # Give this input box a unique name

    # get deposit amount
    deposit_amount=st.number_input(
        "Enter Deposit Amount (₹):",
        min_value=0.0,
        step=500.0   
    )

    # Deposit money
    if st.button("Deposit Money"):

       # Try to validate the customer ID and deposit amount
        try:
             # Deposit money using the backend
            updated_balance = bank.deposit(
                    account_number, deposit_amount)


            # Display a success message when both validations pass
            st.success("Deposit details submitted successfully!")

            # Display the deposit details
            st.write("Account Number:", account_number)
            st.write("Deposited Amount:", f"₹{deposit_amount:,.2f}")
            st.write("Updated Balance:", f"₹{updated_balance:,.2f}")


            # Catch the validation error and display its message
        except ValueError as error:
            st.error(str(error))




# 4 Withdrawal
elif choice == "Withdrawal":
    st.header('Withdrawal')

    # Check whether bank accounts exist
    if not bank.accounts:
        st.warning("Please create a bank account first.")

    else:
        # Select the account number
        account_number = st.selectbox(
            "Select Account Number:",
            list(bank.accounts.keys()),
            key="withdrawal_account") # Give this input box a unique name

    # Get withdrawal amount
    withdrawal_amount = st.number_input(
        "Enter Withdrawal Amount (₹):",
        min_value=0.0,
        step=500.0
    )

    # Withdrawal money
    if st.button('Withdraw Money'):

        try:
            # Withdraw money using the backend
            updated_balance = bank.withdraw(
            account_number, withdrawal_amount)
        
            st.success("Withdrawal successful!")
            st.write("Account Number:", account_number)
            st.write("Withdrawn Amount:", f"₹{withdrawal_amount:,.2f}")
            st.write("Updated Balance:", f"₹{updated_balance:,.2f}")
        
        except ValueError as error:
                st.error(str(error)) 





# 5 Fund Transfer
elif choice =='Fund Transfer':
    st.header('Fund Transfer')

    # Check whether at least two accounts exist
    if len(bank.accounts) < 2:
        st.warning("Create at least two bank accounts before transferring money.")
    else:
        account_numbers = list(bank.accounts.keys())

        # Select the sender's account
        sender_account = st.selectbox(
            "Select Sender Account:",
            account_numbers,
            key="sender_account"
        )

        # Select the receiver's account
        receiver_options = [
            number for number in account_numbers
            if number != sender_account
        ]

        receiver_account = st.selectbox(
            "Select Receiver Account:",
            receiver_options,
            key="receiver_account"
        )
      
    # get transfer amount
    transfer_amount=st.number_input(
        'Enter Transfer Amount (₹):',
        min_value=0.0,
        step=500.0
    )

    # transfer money
    if st.button('Transfer Money'):
        try:
            # Transfer money using the backend
            result = bank.transfer_funds(
                    sender_account,
                    receiver_account,
                    transfer_amount)

            st.success(result)
            st.write(
                    "Sender's Updated Balance:",
                    f"₹{bank.check_balance(sender_account):,.2f}"
                )
            st.write(
                    "Receiver's Updated Balance:",
                    f"₹{bank.check_balance(receiver_account):,.2f}"
                )

        except ValueError as error:
                st.error(str(error))




# 6 Balance Enquiry
elif choice== 'Balance Enquiry':
    st.subheader('Balance Enquiry') 

    if not bank.accounts:
        st.warning("Please create a bank account first.")

    else:
        # Select the account number
        account_number = st.selectbox(
            "Select Account Number:",
            list(bank.accounts.keys()),
            key="balance_account" )# Give this input box a unique name
       

    # Check account balance
    if st.button('Check Balance'):
        try:
           # Get the actual balance from the backend
            balance = bank.check_balance(account_number)

            st.success("Balance retrieved successfully!")
            st.write("Account Number:", account_number)
            st.write("Available Balance:", f"₹{balance:,.2f}")

        except ValueError as error:
            st.error(str(error))




# 7 Minimum Balance Validation
elif choice =='Minimum Balance Validation':
    st.subheader("Minimum Balance Validation")

    if not bank.accounts:
        st.warning("Please create a bank account first.")

    else:
        # Select the account number
        account_number = st.selectbox(
            "Select Account Number:",
            list(bank.accounts.keys()),
            key="minimum_balance_account") # Give this input box a unique name


        # Check minimum balance
        if st.button("Check Minimum Balance"):
            try:
                # Get the current account balance
                balance = bank.check_balance(account_number)

                st.write("Account Number:", account_number)
                st.write("Current Balance:", f"₹{balance:,.2f}")

                # Check whether the balance is at least ₹1,000
                if balance >= 1000:
                    st.success("Minimum balance requirement is satisfied.")
                else:
                    st.warning("Account balance is below ₹1,000.")

            except ValueError as error:
                st.error(str(error))





# 8 Transaction History
elif choice == 'Transaction History':
    st.subheader('Transaction History')

    if not bank.accounts:
        st.warning("Please create a bank account first.")

    else:
        # Select the account number
        account_number = st.selectbox(
            "Select Account Number:",
            list(bank.accounts.keys()),
            key="history_account" )

    # get the Transaction History
    if st.button('Transaction History'):
        try:
             # Retrieve transaction history from the backend
                account=bank.accounts[account_number]
                history = bank.get_transaction_history(account_number)
                current_balance=account.get_balance()

                st.write("### Transaction Details")
                st.write("Account Number:", account_number)

                # Display current balance nicely using a Streamlit metric card
                st.metric(label="Current Balance", value=f"₹{current_balance:.2f}")

                if history:
                   # Combines all transactions into a single numbered list and displays it
                    st.markdown("\n".join(f"1. {t}" for t in history))
                else:
                    st.info("No transactions found.")

        except ValueError as error:
            st.error(str(error))



   
        
# 9 Account Closure
elif choice == 'Account Closure':
    st.subheader('Account Closure')

    if not bank.accounts:
        st.warning("Please create a bank account first.")

    else:
        # Select the account number
        account_number = st.selectbox(
            "Select Account Number:",
            list(bank.accounts.keys()),
            key="closure_account" )


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
            try:
                result = bank.close_account(account_number)
                st.success(result)
                st.write("Closed Account Number:", account_number)

            except ValueError as error:
                st.error(str(error))


