
# =============================================================
# Project Name : Banking Transaction Management System
# File Name    : bank.py
# Purpose      : Handle the backend logic of the banking system
#
# Storage:
# Complete banking data is stored in one TXT snapshot.
# A backup file is maintained for recovery.
#
# Account Rules:
# Minimum opening balance : Rs. 1,000.00
# Minimum running balance : Rs. 1,000.00
# Supported account types : Savings and Current
# =============================================================


# =============================================================
# 1. IMPORT REQUIRED MODULES
# =============================================================

from datetime import datetime, timezone
from decimal import Decimal, InvalidOperation
from pathlib import Path
import os
import re
import tempfile
import uuid


# =============================================================
# 2. CONSTANTS
# =============================================================

MINIMUM_BALANCE = Decimal("1000.00")
TWO_DECIMALS = Decimal("0.01")
MAX_MONEY = Decimal("999999999999.99")

ACCOUNT_TYPES = (
    "Savings Account",
    "Current Account"
)


# =============================================================
# 3. MONEY VALIDATION
# =============================================================

def money(value, allow_zero=False):

    if isinstance(value, bool) or not isinstance(
        value, (int, float, str, Decimal)
    ):
        raise ValueError("Enter a valid numerical amount.")

    try:
        amount = Decimal(str(value))

        if not amount.is_finite():
            raise ValueError("Amount cannot be NaN or infinity.")

        if abs(amount) > MAX_MONEY:
            raise ValueError("Amount exceeds the supported limit.")

        if amount < 0:
            raise ValueError("Amount cannot be negative.")

        if amount == 0 and not allow_zero:
            raise ValueError("Amount must be greater than zero.")

        if amount.as_tuple().exponent < -2:
            raise ValueError("Use at most two decimal places.")

        return amount.quantize(TWO_DECIMALS)

    except InvalidOperation:
        raise ValueError(
            "Invalid or excessively large amount."
        ) from None


# =============================================================
# 4. CUSTOMER CLASS
# =============================================================

class Customer:

    def __init__(self, customer_id, name, phone, email):

        self.customer_id = customer_id
        self.name = name
        self._phone = phone
        self.__email = email

    @property
    def phone(self):
        return self._phone

    @property
    def email(self):
        return self.__email

    def get_phone(self):
        return self._phone

    def get_email(self):
        return self.__email

    def get_details(self):

        return {
            "Customer ID": self.customer_id,
            "Name": self.name,
            "Phone": self._phone,
            "Email": self.__email
        }

    def to_record(self):

        return (
            f"C|{self.customer_id}|{self.name}|"
            f"{self._phone}|{self.__email}"
        )


# =============================================================
# 5. ACCOUNT CLASS
# =============================================================

class Account:

    def __init__(
        self,
        account_number,
        customer_id,
        account_type,
        balance
    ):

        self.account_number = int(account_number)
        self.customer_id = customer_id
        self.account_type = account_type

        self.__balance = money(balance, allow_zero=True)
        self.transaction_history = []

    def get_balance(self):
        return self.__balance

    def get_details(self):

        return {
            "Account Number": self.account_number,
            "Customer ID": self.customer_id,
            "Account Type": self.account_type,
            "Balance": self.__balance
        }

    # ---------------------------------------------------------
    # DEPOSIT
    # ---------------------------------------------------------

    def deposit(self, amount):

        amt = money(amount)

        new_balance = money(
            self.__balance + amt,
            allow_zero=True
        )

        self.__balance = new_balance

        self.transaction_history.append(
            f"Deposited: Rs.{amt:.2f} | "
            f"Balance: Rs.{new_balance:.2f}"
        )

        return self.__balance

    # ---------------------------------------------------------
    # WITHDRAWAL
    # ---------------------------------------------------------

    def withdraw(self, amount):

        amt = money(amount)

        new_balance = money(
            self.__balance - amt,
            allow_zero=True
        )

        if new_balance < MINIMUM_BALANCE:
            raise ValueError(
                "Minimum balance of Rs.1,000.00 must be maintained."
            )

        self.__balance = new_balance

        self.transaction_history.append(
            f"Withdrawn: Rs.{amt:.2f} | "
            f"Balance: Rs.{new_balance:.2f}"
        )

        return self.__balance

    # ---------------------------------------------------------
    # CALCULATE TRANSFER BALANCES
    # ---------------------------------------------------------

    def calculate_transfer_out(self, amount):

        amt = money(amount)

        new_balance = money(
            self.__balance - amt,
            allow_zero=True
        )

        if new_balance < MINIMUM_BALANCE:
            raise ValueError(
                "Minimum balance of Rs.1,000.00 must be maintained."
            )

        return new_balance

    def calculate_transfer_in(self, amount):

        amt = money(amount)

        return money(
            self.__balance + amt,
            allow_zero=True
        )

    # ---------------------------------------------------------
    # RECORD TRANSFER
    # ---------------------------------------------------------

    def _record_transfer(
        self,
        new_balance,
        amount,
        counterparty,
        reference,
        timestamp,
        direction
    ):

        if direction not in ("OUT", "IN"):
            raise ValueError("Invalid transfer direction.")

        amt = money(amount)
        balance = money(new_balance, allow_zero=True)

        if balance > MAX_MONEY:
            raise ValueError("Balance exceeds the supported limit.")

        if direction == "OUT":

            message = (
                f"[{timestamp}] [{reference}] "
                f"Transfer to {counterparty}: "
                f"-Rs.{amt:.2f} | Balance: Rs.{balance:.2f}"
            )

        else:

            message = (
                f"[{timestamp}] [{reference}] "
                f"Transfer from {counterparty}: "
                f"+Rs.{amt:.2f} | Balance: Rs.{balance:.2f}"
            )

        self.__balance = balance
        self.transaction_history.append(message)

    # ---------------------------------------------------------
    # ACCOUNT CLOSURE SETTLEMENT
    # ---------------------------------------------------------

    def settle_for_closure(self):

        settled = self.__balance

        self.__balance = Decimal("0.00")

        self.transaction_history.append(
            f"Simulated settlement payout: Rs.{settled:.2f}"
        )

        return settled

    # ---------------------------------------------------------
    # SERIALIZATION
    # ---------------------------------------------------------

    def to_record(self, status="A"):

        return (
            f"{status}|{self.account_number}|"
            f"{self.customer_id}|{self.account_type}|"
            f"{self.__balance:.2f}"
        )


# =============================================================
# 6. SAVINGS ACCOUNT CLASS
# =============================================================

class SavingsAccount(Account):

    def __init__(self, account_number, customer_id, balance):

        super().__init__(
            account_number,
            customer_id,
            "Savings Account",
            balance
        )


# =============================================================
# 7. CURRENT ACCOUNT CLASS
# =============================================================

class CurrentAccount(Account):

    def __init__(self, account_number, customer_id, balance):

        super().__init__(
            account_number,
            customer_id,
            "Current Account",
            balance
        )


# =============================================================
# 8. BANK CLASS
# =============================================================

class Bank:

    def __init__(self, data_dir=None):

        base_dir = Path(__file__).resolve().parent

        self.data_dir = (
            Path(data_dir)
            if data_dir is not None
            else base_dir / "data"
        )

        self.data_dir.mkdir(parents=True, exist_ok=True)

        self.data_file = self.data_dir / "bank_data.txt"
        self.backup_file = self.data_dir / "bank_data.bak"
        self.lock_file = self.data_dir / "bank.lock"

        self.customers = {}
        self.accounts = {}
        self.closed_accounts = {}

        self.next_customer_id = 1
        self.next_account_number = 1001

        self._owns_lock = False

        self.refresh()

    # =========================================================
    # 9. FILE LOCKING
    # =========================================================

    def _acquire_lock(self):

        fd = None
        lock_created = False

        try:

            fd = os.open(
                str(self.lock_file),
                os.O_CREAT | os.O_EXCL | os.O_WRONLY
            )

            lock_created = True
            self._owns_lock = True

            lock_text = (
                f"PID={os.getpid()}\n"
                f"TIME={datetime.now(timezone.utc).isoformat()}\n"
            )

            data = lock_text.encode("utf-8")

            # Ensure the complete lock information is written.
            with os.fdopen(fd, "wb") as lock_file:

                fd = None
                lock_file.write(data)
                lock_file.flush()
                os.fsync(lock_file.fileno())

        except FileExistsError:

            raise RuntimeError(
                "Another banking operation is running, "
                "or a previous process left a lock file. "
                "Verify that no application process is active "
                "before manually removing a stale lock."
            ) from None

        except Exception:

            if fd is not None:
                os.close(fd)

            if lock_created and self._owns_lock:

                try:
                    self.lock_file.unlink(missing_ok=True)
                finally:
                    self._owns_lock = False

            raise

    def _release_lock(self):

        if self._owns_lock:

            try:
                self.lock_file.unlink(missing_ok=True)

            finally:
                self._owns_lock = False

    # =========================================================
    # 10. ATOMIC FILE WRITING
    # =========================================================

    def _atomic_write(self, target_path, content):

        temp_path = None

        try:

            with tempfile.NamedTemporaryFile(
                mode="wb",
                dir=self.data_dir,
                delete=False
            ) as temp:

                temp_path = temp.name

                temp.write(content)
                temp.flush()
                os.fsync(temp.fileno())

            os.replace(temp_path, target_path)
            temp_path = None

        finally:

            if temp_path and os.path.exists(temp_path):
                os.remove(temp_path)

    # =========================================================
    # 11. CREATE BACKUP
    # =========================================================

    def _create_backup(self):

        if self.data_file.exists():

            previous_data = self.data_file.read_bytes()

            self._atomic_write(
                self.backup_file,
                previous_data
            )

    # =========================================================
    # 12. SAVE COMPLETE SNAPSHOT
    # =========================================================

    def _save_snapshot(self):

        lines = []

        for customer in self.customers.values():
            lines.append(customer.to_record())

        for account in self.accounts.values():
            lines.append(account.to_record("A"))

        for account in self.closed_accounts.values():
            lines.append(account.to_record("X"))

        all_accounts = (
            list(self.accounts.values())
            + list(self.closed_accounts.values())
        )

        for account in all_accounts:

            for item in account.transaction_history:

                if "\n" in item or "\r" in item:
                    raise ValueError(
                        "Transaction history contains invalid line breaks."
                    )

                lines.append(
                    f"T|{account.account_number}|{item}"
                )

        content = "\n".join(lines)

        if lines:
            content += "\n"

        self._create_backup()

        self._atomic_write(
            self.data_file,
            content.encode("utf-8")
        )

    # =========================================================
    # 13. CUSTOMER VALIDATION
    # =========================================================

    def _validate_customer(self, name, phone, email):

        if not all(
            isinstance(value, str)
            for value in (name, phone, email)
        ):
            raise ValueError(
                "Name, phone and email must be text."
            )

        clean_name = " ".join(name.strip().split())
        clean_phone = phone.strip()
        clean_email = email.strip()

        for value in (clean_name, clean_phone, clean_email):

            if (
                "|" in value
                or "\n" in value
                or "\r" in value
            ):
                raise ValueError(
                    "Fields cannot contain pipe symbols or line breaks."
                )

        if not clean_name:
            raise ValueError("Customer name cannot be empty.")

        if len(clean_name) > 100:
            raise ValueError("Customer name is too long.")

        digits = (
            clean_phone[1:]
            if clean_phone.startswith("+")
            else clean_phone
        )

        if (
            not digits.isdigit()
            or not 10 <= len(digits) <= 15
        ):
            raise ValueError(
                "Enter a valid phone number with 10 to 15 digits."
            )

        email_pattern = (
            r"^[A-Za-z0-9.!#$%&'*+/=?^_`{|}~-]+"
            r"@[A-Za-z0-9]"
            r"(?:[A-Za-z0-9-]{0,61}[A-Za-z0-9])?"
            r"(?:\.[A-Za-z0-9]"
            r"(?:[A-Za-z0-9-]{0,61}[A-Za-z0-9])?)+$"
        )

        if (
            len(clean_email) > 254
            or not re.fullmatch(email_pattern, clean_email)
        ):
            raise ValueError("Enter a valid email address.")

        return clean_name, clean_phone, clean_email

    # =========================================================
    # 14. LOAD COMPLETE BANKING SNAPSHOT
    # =========================================================

    def _load_snapshot(self):

        customers = {}
        active = {}
        closed = {}

        max_customer_id = 0
        max_account_number = 1000

        try:

            with open(
                self.data_file,
                "r",
                encoding="utf-8"
            ) as file:

                for line_no, raw in enumerate(file, start=1):

                    line = raw.rstrip("\r\n")

                    if not line.strip():
                        continue

                    parts = line.split("|")
                    record_type = parts[0]

                    # -------------------------------------------------
                    # CUSTOMER RECORD
                    # -------------------------------------------------

                    if record_type == "C":

                        if len(parts) != 5:
                            raise ValueError(
                                f"{self.data_file.name}:{line_no}: "
                                "Invalid customer record."
                            )

                        _, cust_id, name, phone, email = parts

                        if (
                            not cust_id.startswith("Cust")
                            or not cust_id[4:].isdigit()
                            or int(cust_id[4:]) < 1
                        ):
                            raise ValueError(
                                f"{self.data_file.name}:{line_no}: "
                                f"Invalid customer ID '{cust_id}'."
                            )

                        if cust_id in customers:
                            raise ValueError(
                                f"{self.data_file.name}:{line_no}: "
                                f"Duplicate customer ID '{cust_id}'."
                            )

                        clean_name, clean_phone, clean_email = (
                            self._validate_customer(
                                name,
                                phone,
                                email
                            )
                        )

                        customers[cust_id] = Customer(
                            cust_id,
                            clean_name,
                            clean_phone,
                            clean_email
                        )

                        max_customer_id = max(
                            max_customer_id,
                            int(cust_id[4:])
                        )

                    # -------------------------------------------------
                    # ACTIVE AND CLOSED ACCOUNT RECORDS
                    # -------------------------------------------------

                    elif record_type in ("A", "X"):

                        if len(parts) != 5:
                            raise ValueError(
                                f"{self.data_file.name}:{line_no}: "
                                "Invalid account record."
                            )

                        _, acc_str, cust_id, acc_type, bal_str = parts

                        if not acc_str.isdigit():
                            raise ValueError(
                                f"{self.data_file.name}:{line_no}: "
                                "Invalid account number."
                            )

                        acc_no = int(acc_str)

                        if acc_no < 1001:
                            raise ValueError(
                                f"{self.data_file.name}:{line_no}: "
                                "Invalid account number."
                            )

                        if acc_no in active or acc_no in closed:
                            raise ValueError(
                                f"{self.data_file.name}:{line_no}: "
                                f"Duplicate account {acc_no}."
                            )

                        if cust_id not in customers:
                            raise ValueError(
                                f"{self.data_file.name}:{line_no}: "
                                f"Unknown customer '{cust_id}'."
                            )

                        if acc_type not in ACCOUNT_TYPES:
                            raise ValueError(
                                f"{self.data_file.name}:{line_no}: "
                                "Invalid account type."
                            )

                        bal = money(
                            bal_str,
                            allow_zero=True
                        )

                        cls = (
                            SavingsAccount
                            if acc_type == "Savings Account"
                            else CurrentAccount
                        )

                        if record_type == "A":

                            if bal < MINIMUM_BALANCE:
                                raise ValueError(
                                    f"{self.data_file.name}:{line_no}: "
                                    "Active account below minimum balance."
                                )

                            active[acc_no] = cls(
                                acc_no,
                                cust_id,
                                bal
                            )

                        else:

                            if bal != Decimal("0.00"):
                                raise ValueError(
                                    f"{self.data_file.name}:{line_no}: "
                                    "Closed account must have zero balance."
                                )

                            closed[acc_no] = cls(
                                acc_no,
                                cust_id,
                                bal
                            )

                        max_account_number = max(
                            max_account_number,
                            acc_no
                        )

                    # -------------------------------------------------
                    # TRANSACTION RECORD
                    # -------------------------------------------------

                    elif record_type == "T":

                        if len(parts) < 3:
                            raise ValueError(
                                f"{self.data_file.name}:{line_no}: "
                                "Invalid transaction record."
                            )

                        acc_str = parts[1]
                        message = "|".join(parts[2:])

                        if not acc_str.isdigit():
                            raise ValueError(
                                f"{self.data_file.name}:{line_no}: "
                                "Invalid transaction account number."
                            )

                        acc_no = int(acc_str)

                        account = (
                            active.get(acc_no)
                            or closed.get(acc_no)
                        )

                        if account is None:
                            raise ValueError(
                                f"{self.data_file.name}:{line_no}: "
                                f"Unknown account {acc_no} in history."
                            )

                        if not message:
                            raise ValueError(
                                f"{self.data_file.name}:{line_no}: "
                                "Empty transaction message."
                            )

                        account.transaction_history.append(message)

                    else:

                        raise ValueError(
                            f"{self.data_file.name}:{line_no}: "
                            f"Unknown record type '{record_type}'."
                        )

        except (ValueError, OSError, UnicodeError) as err:

            raise ValueError(
                f"Unable to trust banking data: {err}. "
                "Original snapshot and backup have been preserved. "
                "Stop transactions and correct or recover the data."
            ) from err

        # Publish only after the entire snapshot is validated.
        self.customers = customers
        self.accounts = active
        self.closed_accounts = closed

        self.next_customer_id = max_customer_id + 1
        self.next_account_number = max_account_number + 1

    # =========================================================
    # 15. REFRESH DATA
    # =========================================================

    def refresh(self):

        self._acquire_lock()

        try:

            if not self.data_file.exists():

                self._atomic_write(
                    self.data_file,
                    b""
                )

            self._load_snapshot()

        finally:
            self._release_lock()

    # =========================================================
    # 16. SAFE WRITE OPERATION HANDLER
    # =========================================================

    def _run_safe(self, action):

        self._acquire_lock()

        try:

            # Always reload the latest committed state.
            self._load_snapshot()

            # Execute the operation.
            result = action()

            # Save the complete updated snapshot.
            self._save_snapshot()

            return result

        except Exception:

            # Restore memory from the last committed snapshot.
            if self.data_file.exists():

                try:
                    self._load_snapshot()

                except Exception:
                    pass

            raise

        finally:
            self._release_lock()

    # =========================================================
    # 17. SAFE READ-ONLY OPERATION HANDLER
    # =========================================================

    def _run_read_safe(self, action):

        self._acquire_lock()

        try:

            # Load the latest data without saving it.
            self._load_snapshot()

            return action()

        finally:
            self._release_lock()

    # =========================================================
    # 18. REGISTER CUSTOMER
    # =========================================================

    def register_customer(self, name, phone, email):

        clean_name, clean_phone, clean_email = (
            self._validate_customer(
                name,
                phone,
                email
            )
        )

        def operation():

            cust_id = f"Cust{self.next_customer_id:03d}"

            customer = Customer(
                cust_id,
                clean_name,
                clean_phone,
                clean_email
            )

            self.customers[cust_id] = customer
            self.next_customer_id += 1

            return customer

        return self._run_safe(operation)

    # =========================================================
    # 19. CREATE ACCOUNT
    # =========================================================

    def create_account(
        self,
        customer_id,
        account_type,
        initial_deposit
    ):

        opening = money(initial_deposit)

        if opening < MINIMUM_BALANCE:
            raise ValueError(
                "Opening deposit must be at least Rs.1,000.00."
            )

        if account_type not in ACCOUNT_TYPES:
            raise ValueError(
                "Select Savings Account or Current Account."
            )

        def operation():

            if customer_id not in self.customers:
                raise ValueError(
                    "Selected customer does not exist."
                )

            acc_no = self.next_account_number

            cls = (
                SavingsAccount
                if account_type == "Savings Account"
                else CurrentAccount
            )

            account = cls(
                acc_no,
                customer_id,
                opening
            )

            account.transaction_history.append(
                f"Opening Deposit: Rs.{opening:.2f} | "
                f"Balance: Rs.{account.get_balance():.2f}"
            )

            self.accounts[acc_no] = account
            self.next_account_number += 1

            return account

        return self._run_safe(operation)

    # =========================================================
    # 20. DEPOSIT
    # =========================================================

    def deposit(self, account_number, amount):

        amt = money(amount)

        def operation():

            if account_number in self.closed_accounts:
                raise ValueError("Account is closed.")

            if account_number not in self.accounts:
                raise ValueError("Account not found.")

            account = self.accounts[account_number]

            return account.deposit(amt)

        return self._run_safe(operation)

    # =========================================================
    # 21. WITHDRAWAL
    # =========================================================

    def withdraw(self, account_number, amount):

        amt = money(amount)

        def operation():

            if account_number in self.closed_accounts:
                raise ValueError("Account is closed.")

            if account_number not in self.accounts:
                raise ValueError("Account not found.")

            account = self.accounts[account_number]

            return account.withdraw(amt)

        return self._run_safe(operation)

    # =========================================================
    # 22. FUND TRANSFER
    # =========================================================

    def transfer_funds(
        self,
        sender_account_no,
        receiver_account_no,
        amount
    ):

        amt = money(amount)

        if sender_account_no == receiver_account_no:
            raise ValueError(
                "Sender and receiver must be different accounts."
            )

        def operation():

            if (
                sender_account_no not in self.accounts
                or receiver_account_no not in self.accounts
            ):
                raise ValueError(
                    "Both accounts must be active."
                )

            sender = self.accounts[sender_account_no]
            receiver = self.accounts[receiver_account_no]

            # Calculate both balances before changing either.
            new_sender_balance = sender.calculate_transfer_out(amt)
            new_receiver_balance = receiver.calculate_transfer_in(amt)

            reference = f"TXN-{uuid.uuid4().hex[:8].upper()}"

            timestamp = datetime.now(
                timezone.utc
            ).strftime("%Y-%m-%d %H:%M:%S UTC")

            sender._record_transfer(
                new_sender_balance,
                amt,
                receiver_account_no,
                reference,
                timestamp,
                "OUT"
            )

            receiver._record_transfer(
                new_receiver_balance,
                amt,
                sender_account_no,
                reference,
                timestamp,
                "IN"
            )

            return reference

        return self._run_safe(operation)

    # =========================================================
    # 23. ACCOUNT CLOSURE
    # =========================================================

    def close_account(self, account_number):

        def operation():

            if account_number in self.closed_accounts:
                raise ValueError("Account is already closed.")

            if account_number not in self.accounts:
                raise ValueError("Account not found.")

            account = self.accounts.pop(account_number)

            settled = account.settle_for_closure()

            self.closed_accounts[account_number] = account

            return settled

        return self._run_safe(operation)

    # =========================================================
    # 24. TRANSACTION HISTORY
    # =========================================================

    def get_transaction_history(self, account_number):

        def operation():

            if account_number in self.accounts:

                account = self.accounts[account_number]

                return (
                    list(account.transaction_history),
                    "Active"
                )

            if account_number in self.closed_accounts:

                account = self.closed_accounts[account_number]

                return (
                    list(account.transaction_history),
                    "Closed"
                )

            raise ValueError("Account not found.")

        return self._run_read_safe(operation) 

    # =========================================================
    # 25. CUSTOMER DETAILS
    # =========================================================

    def get_customer_details(self, customer_id):

        def operation():

            if customer_id not in self.customers:
                raise ValueError("Customer not found.")

            return self.customers[customer_id].get_details()

        return self._run_read_safe(operation)

    # =========================================================
    # 26. ACCOUNT DETAILS
    # =========================================================

    def get_account_details(self, account_number):

        def operation():

            if account_number in self.accounts:

                account = self.accounts[account_number]
                status = "Active"

            elif account_number in self.closed_accounts:

                account = self.closed_accounts[account_number]
                status = "Closed"

            else:
                raise ValueError("Account not found.")

            details = account.get_details()
            details["Status"] = status

            return details

        return self._run_read_safe(operation)

    # =========================================================
    # 27. CUSTOMER AND ACCOUNT IDENTIFIERS
    # =========================================================

    def get_customer_ids(self):

        def operation():
            return list(self.customers.keys())

        return self._run_read_safe(operation)

    def get_active_account_ids(self):

        def operation():
            return list(self.accounts.keys())

        return self._run_read_safe(operation)

    def get_all_account_ids(self):

        def operation():

            return (
                list(self.accounts.keys())
                + list(self.closed_accounts.keys())
            )

        return self._run_read_safe(operation)


# =============================================================
# END OF BANKING TRANSACTION MANAGEMENT SYSTEM BACKEND
# =============================================================
