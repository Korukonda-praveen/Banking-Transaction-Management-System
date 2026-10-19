# 🏦 Banking Transaction Management System

## 📌 About the Project

This is a simple banking application built using Python and Streamlit.

It helps users perform basic banking operations like creating accounts, depositing money, withdrawing money, transferring money, and checking account balances.

The project uses TXT files to save customer details, account details, and transaction history.

## ✨ Features

- **Customer Registration** – Register a new customer.
- **Account Creation** – Create a savings or current account.
- **Deposit** – Add money to an account.
- **Withdrawal** – Withdraw money from an account.
- **Fund Transfer** – Transfer money from one account to another.
- **Balance Enquiry** – Check the current account balance.
- **Minimum Balance Validation** – Check whether the account has the required minimum balance.
- **Transaction History** – View account transactions.
- **Account Closure** – Close an existing account.
- **TXT File Storage** – Save customer, account, and transaction details in text files.

## 🛠️ Technologies Used

- Python
- Streamlit
- TXT File Handling

## 📂 Project Structure

```text
Banking-Transaction-Management-System/
│
├── banking_system.py
├── bank.py
├── README.md
├── customers.txt
├── accounts.txt
├── transactions.txt
└── closed_accounts.txt
```

**Note:** The TXT files are created automatically when the application runs, so they do not need to be uploaded to GitHub.

## ⚙️ How to Run the Project

### Step 1: Clone the repository

```bash
git clone https://github.com/Korukonda-praveen/Banking-Transaction-Management-System.git
```

### Step 2: Open the project folder

```bash
cd Banking-Transaction-Management-System
```

### Step 3: Install Streamlit

```bash
python -m pip install streamlit
```

### Step 4: Run the application

```bash
python -m streamlit run banking_system.py
```

The application will open in your web browser.

## 🧠 Python Concepts Used

- Functions
- Dictionaries
- Classes and Objects
- Constructors
- Encapsulation
- Inheritance
- Exception Handling
- Modules
- TXT File Handling

## 💾 Data Storage

The project uses four TXT files to save data:

- `customers.txt` – Stores customer details.
- `accounts.txt` – Stores active account details.
- `transactions.txt` – Stores transaction history.
- `closed_accounts.txt` – Stores closed account details.

## 🎯 What I Learned

By building this project, I learned how to use Python to create a simple banking application, work with classes and objects, handle errors, validate transactions, build a user interface with Streamlit, and save data in text files.

## 👨‍💻 Author

**Korukonda Praveen**

GitHub: [Korukonda-praveen](https://github.com/Korukonda-praveen)

---

⭐ This project was created for learning and practising Python programming.
