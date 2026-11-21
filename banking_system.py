
# =============================================================
# Project : Banking Transaction Management System
# File    : banking_system.py
# Description: Streamlit user interface for the educational
#              banking system.
# =============================================================

import streamlit as st
from bank import Bank


# =============================================================
# 1. INITIALIZE SESSION STATE
# =============================================================

# Store the recently registered customer ID.
if "registered_customer_id" not in st.session_state:
    st.session_state.registered_customer_id = None

# Store the currently selected module.
if "module_menu" not in st.session_state:
    st.session_state.module_menu = "Home"

# Store the next module to navigate to.
if "next_module" not in st.session_state:
    st.session_state.next_module = None


# =============================================================
# 2. MODULE NAVIGATION FUNCTIONS
# =============================================================

# Navigate to Account Creation after successful registration.
def go_to_account_creation():
    st.session_state.next_module = "Account Creation"


# Apply pending navigation.
if st.session_state.next_module is not None:
    st.session_state.module_menu = st.session_state.next_module
    st.session_state.next_module = None


# =============================================================
# 3. INITIALIZE BANK OBJECT
# =============================================================

# Load the banking data when the application starts.
try:
    if "bank" not in st.session_state:
        st.session_state.bank = Bank()

    bank = st.session_state.bank

except (ValueError, OSError, UnicodeError, RuntimeError) as err:
    st.error(f"Cannot load banking data: {err}")
    st.stop()


# =============================================================
# 4. APPLICATION TITLE AND SIDEBAR
# =============================================================

st.title("🏦 Banking Transaction Management System")

menu = [
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

choice = st.sidebar.selectbox(
    "Select Module",
    menu,
    key="module_menu"
)


# =============================================================
# 5. HOME
# =============================================================


if choice == "Home":

    st.subheader("🏦 Welcome to Banking Transaction Management System")

    st.write(
        "Manage customers, bank accounts, transactions, "
        "and transaction history in one place."
    )

    st.info(
        "Minimum opening and running balance: "
        "₹1,000.00 for Savings and Current accounts."
    )

    st.markdown("### 📌 Available Features")

    st.write("👤 **1. Customer Registration**")
    st.write("Register new customers with name, phone number, and email.")

    st.write("🏦 **2. Account Creation**")
    st.write("Create Savings or Current accounts for registered customers.")

    st.write("💰 **3. Deposit Money**")
    st.write("Deposit money into an active bank account.")

    st.write("💸 **4. Withdraw Money**")
    st.write("Withdraw money while maintaining the minimum balance.")

    st.write("🔄 **5. Fund Transfer**")
    st.write("Transfer money securely between active bank accounts.")

    st.write("💳 **6. Balance Enquiry**")
    st.write("Check the available balance of an active account.")

    st.write("✅ **7. Minimum Balance Validation**")
    st.write("Verify that the required minimum balance is maintained.")

    st.write("📜 **8. Transaction History**")
    st.write("View transaction records of active and closed accounts.")

    st.write("🔒 **9. Account Closure**")
    st.write("Close an active account with a simulated balance settlement.")

    st.markdown("---")

    st.success(
        "✅ Select a module from the sidebar to get started!"
    )

    st.caption(
        "This application is an educational banking simulation "
        "developed using Python, OOP, Streamlit, and TXT file storage."
    )


# =============================================================
# 6. CUSTOMER REGISTRATION
# Correction 1: Fix invalid registration crash
# =============================================================

elif choice == "Customer Registration":

    st.subheader("Customer Registration")

    with st.form("reg_form"):

        name = st.text_input("Full Name")
        phone = st.text_input("Phone Number")
        email = st.text_input("Email Address")

        submitted = st.form_submit_button("Register")

    if submitted:

        # Clear the previous registration result before
        # processing a new registration.
        st.session_state.registered_customer_id = None

        try:
            # Backend validates customer information.
            cust = bank.register_customer(name, phone, email)

        except (ValueError, OSError, UnicodeError, RuntimeError) as err:

            st.error(f"Registration failed: {err}")

        else:

            # Store the customer ID only after success.
            st.session_state.registered_customer_id = cust.customer_id

            st.success("Customer registered successfully!")

            # Display customer details only after successful registration.
            st.write(f"**ID:** {cust.customer_id}")
            st.write(f"**Name:** {cust.name}")
            st.write(f"**Phone:** {cust.get_phone()}")
            st.write(f"**Email:** {cust.get_email()}")

    # Show the proceed button only for a valid registration.
    if (
        st.session_state.registered_customer_id is not None
        and st.session_state.registered_customer_id in bank.get_customer_ids()
    ):

        st.button(
            "Proceed to Account Creation",
            on_click=go_to_account_creation
        )


# =============================================================
# 7. ACCOUNT CREATION
# Correction 9: Display generated account number
# =============================================================

elif choice == "Account Creation":

    st.subheader("Account Creation")

    # Retrieve available customer IDs.
    cust_ids = bank.get_customer_ids()

    if not cust_ids:

        st.warning("No customers found. Register a customer first.")

    else:

        # Select the recently registered customer by default.
        default_idx = (
            cust_ids.index(st.session_state.registered_customer_id)
            if st.session_state.registered_customer_id in cust_ids
            else 0
        )

        cust_id = st.selectbox(
            "Customer ID",
            cust_ids,
            index=default_idx
        )

        acc_type = st.selectbox(
            "Account Type",
            ["Savings Account", "Current Account"]
        )

        # Minimum opening balance is ₹1,000.
        opening_amt = st.number_input(
            "Initial Deposit (₹)",
            min_value=1000.0,
            value=1000.0,
            step=100.0
        )

        if st.button("Create Account"):

            try:

                acc = bank.create_account(
                    cust_id,
                    acc_type,
                    opening_amt
                )

            except (ValueError, OSError, UnicodeError, RuntimeError) as err:

                st.error(f"Account creation failed: {err}")

            else:

                # Display account details only after successful creation.
                st.success("Account created successfully!")

                st.write(f"**Account Number:** {acc.account_number}")
                st.write(f"**Customer ID:** {cust_id}")
                st.write(f"**Account Type:** {acc.account_type}")
                st.write(f"**Balance:** ₹{acc.get_balance():.2f}")



# =============================================================
# 8. DEPOSIT / WITHDRAWAL / BALANCE ENQUIRY /
#    MINIMUM BALANCE VALIDATION
# =============================================================

elif choice in (
    "Deposit",
    "Withdrawal",
    "Balance Enquiry",
    "Minimum Balance Validation"
):

    st.subheader(choice)

    # Retrieve active account numbers through the backend.
    acc_ids = bank.get_active_account_ids()

    if not acc_ids:

        st.warning("No active accounts available.")

    else:

        acc_no = st.selectbox(
            "Select Active Account",
            acc_ids
        )

        if choice == "Balance Enquiry":

            # Retrieve account details using the backend method.
            details = bank.get_account_details(acc_no)
            bal = details["Balance"]

            st.info(
                f"Balance for Account {acc_no}: **₹{bal:.2f}**"
            )

        elif choice == "Minimum Balance Validation":

            # Retrieve the current balance.
            details = bank.get_account_details(acc_no)
            bal = details["Balance"]

            st.write("Required minimum balance: **₹1,000.00**")
            st.write(f"Current balance: **₹{bal:.2f}**")

            if bal >= 1000:
                st.success("Minimum balance requirement is met.")
            else:
                st.error("Balance is below ₹1,000.00.")

        else:

            # Amount input for deposit and withdrawal.
            amt = st.number_input(
                "Amount (₹)",
                min_value=0.1,
                value=100.0,
                step=50.0
            )

            btn_text = (
                "Deposit"
                if choice == "Deposit"
                else "Withdraw"
            )

            if st.button(btn_text):

                try:

                    if choice == "Deposit":
                        new_bal = bank.deposit(acc_no, amt)
                    else:
                        new_bal = bank.withdraw(acc_no, amt)

                except (ValueError, OSError, UnicodeError, RuntimeError) as err:
                    st.error(f"Action failed: {err}")

                else:
                    st.success(
                        f"Transaction completed! "
                        f"New Balance: **₹{new_bal:.2f}**"
                    )


# =============================================================
# 9. FUND TRANSFER
# =============================================================

elif choice == "Fund Transfer":

    st.subheader("Fund Transfer")

    # Retrieve only active accounts.
    acc_ids = bank.get_active_account_ids()

    if len(acc_ids) < 2:

        st.warning(
            "You need at least two active accounts "
            "to transfer funds."
        )

    else:

        sender = st.selectbox(
            "Sender Account",
            acc_ids,
            key="xfer_sender"
        )

        # Exclude the sender from receiver options.
        receivers = [
            account
            for account in acc_ids
            if account != sender
        ]

        receiver = st.selectbox(
            "Receiver Account",
            receivers,
            key="xfer_receiver"
        )

        amt = st.number_input(
            "Transfer Amount (₹)",
            min_value=0.0,
            value=100.0,
            step=50.0
        )

        if st.button("Transfer"):

            try:

                bank.transfer_funds(
                    sender,
                    receiver,
                    amt
                )

            except (ValueError, OSError, UnicodeError, RuntimeError) as err:
                st.error(f"Transfer failed: {err}")

            else:
                st.success("Transfer completed successfully!")


# =============================================================
# 10. TRANSACTION HISTORY
# =============================================================

elif choice == "Transaction History":

    st.subheader("Transaction History")

    # Retrieve active and closed account numbers.
    all_accs = bank.get_all_account_ids()

    if not all_accs:

        st.warning("No accounts available.")

    else:

        acc_no = st.selectbox(
            "Select Account (Active or Closed)",
            all_accs
        )

        try:

            # Retrieve history and account status.
            history, status = bank.get_transaction_history(acc_no)

        except (ValueError, OSError, UnicodeError, RuntimeError) as err:
            st.error(f"Could not retrieve history: {err}")

        else:

            st.write(
                f"**Account Status:** {status} (Read-only)"
            )

            if not history:

                st.info("No transactions found.")

            else:

                # Display transactions in stored order.
                for row in history:
                    st.write(f"- {row}")


# =============================================================
# 11. ACCOUNT CLOSURE
# =============================================================

elif choice == "Account Closure":

    st.subheader("Account Closure")

    # Retrieve only active accounts.
    acc_ids = bank.get_active_account_ids()

    if not acc_ids:

        st.warning("No active accounts available to close.")

    else:

        acc_no = st.selectbox(
            "Select Active Account to Close",
            acc_ids
        )

        # Require explicit confirmation.
        confirm = st.checkbox(
            "I confirm closing this account "
            "(balance will be settled as simulated payout)."
        )

        if st.button("Close Account"):

            if not confirm:

                st.warning(
                    "Please tick the confirmation box first."
                )

            else:

                try:

                    settled = bank.close_account(acc_no)

                except (ValueError, OSError, UnicodeError, RuntimeError) as err:
                    st.error(f"Could not close account: {err}")

                else:

                    st.success(
                        f"Account {acc_no} closed successfully. "
                        f"Simulated payout settled: **₹{settled:.2f}**"
                    )

                    st.info(
                        "The settlement is a simulated payout "
                        "for this educational banking project."
                    )
