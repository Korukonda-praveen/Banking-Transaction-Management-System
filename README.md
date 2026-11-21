# Banking Transaction Management System

A simple educational banking application built with **Python** and **Streamlit**. It uses object-oriented programming (OOP) and saves records in a TXT file.

## Features

- Customer registration with input validation
- Savings and Current account creation
- Deposit and withdrawal
- Fund transfer between active accounts
- Balance enquiry and ₹1,000 minimum balance check
- Transaction history for active and closed accounts
- Account closure with simulated balance settlement
- TXT data storage and backup

## Requirements

- Python 3
- Streamlit

## How to Run

1. Keep `bank.py` and `banking_system.py` in the same folder.
2. Open a terminal in that folder and install Streamlit:

   ```bash
   python -m pip install streamlit
   ```

3. Start the application:

   ```bash
   python -m streamlit run banking_system.py
   ```

4. Select a feature from the sidebar.

## Project Workflow

1. **Start:** Run the Streamlit app and choose a module from the sidebar.
2. **Register Customer:** Enter name, phone and email to get a Customer ID.
3. **Create Account:** Select the Customer ID, choose Savings or Current, and deposit at least ₹1,000 to get an Account Number.
4. **Banking Operations:** Deposit, withdraw, transfer money, or check the balance. The ₹1,000 minimum balance is maintained.
5. **Transaction History:** View transactions for active or closed accounts.
6. **Close Account:** Confirm closure; the remaining balance is recorded as a simulated payout.
7. **Save Data:** The system saves records to `data/bank_data.txt` and keeps a backup of the previous snapshot.

**Flow:** Start → Register Customer → Create Account → Transactions / Balance Enquiry → Transaction History → Account Closure

## Project Files

- `bank.py` – Customer, account, transaction and storage logic
- `banking_system.py` – Streamlit user interface
- `data/bank_data.txt` – Saved banking records (created automatically)
- `data/bank_data.bak` – Backup of the previous saved snapshot

## Banking Rules

- Minimum opening and running balance: **₹1,000** for both account types.
- Transfers require two active accounts.
- Invalid amounts and customer details are rejected.
- Closed accounts cannot be used for further transactions.

## Python Concepts Used

Classes, objects, inheritance, encapsulation, functions, dictionaries, exception handling, `Decimal`, and TXT file handling.

## Testing and Notes

Test registration, account creation, deposit, withdrawal, transfer, transaction history, restart and closure before presenting. Add screenshots of your own tests to the repository.

**Note:** This is a learning project, not a real banking service. If stored data is damaged, stop transactions and inspect the original file and backup before restoring it.
