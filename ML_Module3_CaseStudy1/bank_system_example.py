# Design software for bank systems. There should be options like cash withdrawal,
# cash credit, and a change password. According to user input, the software should
# provide the required output.
# Hint: Use if else statements and functions.

# Simple Bank System

# Initial account details
balance = 10000  # starting balance
password = "1234"  # default password

def cash_withdrawal():
    global balance
    amount = float(input("Enter amount to withdraw: "))
    if amount > balance:
        print(" Insufficient balance!")
    else:
        balance -= amount
        print(f" Withdrawal successful! Remaining balance: ₹{balance}")

def cash_credit():
    global balance
    amount = float(input("Enter amount to deposit: "))
    balance += amount
    print(f" Deposit successful! Updated balance: ₹{balance}")

def change_password():
    global password
    old_pass = input("Enter old password: ")
    if old_pass == password:
        new_pass = input("Enter new password: ")
        password = new_pass
        print(" Password changed successfully!")
    else:
        print(" Incorrect old password!")

def main():
    global password
    print("----- Welcome to HDFC Bank System -----")
    entered_pass = input("Enter your password: ")
    if entered_pass != password:
        print(" Wrong password. Access denied!")
        return

    while True:
        print("\nChoose an option:")
        print("1. Cash Withdrawal")
        print("2. Cash Credit (Deposit)")
        print("3. Change Password")
        print("4. Exit")

        choice = input("Enter your choice: ")

        if choice == "1":
            cash_withdrawal()
        elif choice == "2":
            cash_credit()
        elif choice == "3":
            change_password()
        elif choice == "4":
            print("Thank you for using HDFC Bank System!")
            break
        else:
            print(" Invalid choice, please try again.")

# Run the program
main()

# Example input:
# Enter your password: 1234
# Choose an option:
# 1. Cash Withdrawal
# 2. Cash Credit (Deposit)
# 3. Change Password
# 4. Exit
# Enter your choice: 1
# Enter amount to withdraw: 500
# Withdrawal successful! Remaining balance: ₹9500.0
# Enter your choice: 2
# Enter amount to deposit: 2000
# Deposit successful! Updated balance: ₹11500.0
# Enter your choice: 3
# Enter old password: 1234
# Enter new password: 5678
# Password changed successfully!
# Enter your choice: 4
# Thank you for using HDFC Bank System!
# Example input:
# Enter your password: 1234
# Choose an option:
# 1. Cash Withdrawal
# 2. Cash Credit (Deposit)
# 3. Change Password
# 4. Exit
# Enter your choice: 1
# Enter amount to withdraw: 12000
# Insufficient balance!
# Enter your choice: 2
# Enter amount to deposit: 5000
# Deposit successful! Updated balance: ₹15000.0
# Enter your choice: 3
# Enter old password: 5678
# Enter new password: 1234
# Password changed successfully!
# Enter your choice: 4
# Thank you for using HDFC Bank System!
# Example input:
# Enter your password: 1234
# Choose an option:
# 1. Cash Withdrawal
# 2. Cash Credit (Deposit)
# 3. Change Password
# 4. Exit
# Enter your choice: 3
# Enter old password: 1234
# Enter new password: 4321
# Password changed successfully!
# Enter your choice: 4
# Thank you for using HDFC Bank System!
# Example input:
# Enter your password: 1234
# Choose an option:
# 1. Cash Withdrawal
# 2. Cash Credit (Deposit)
# 3. Change Password
# 4. Exit
# Enter your choice: 5
# Invalid choice, please try again.
# Enter your choice: 1
# Enter amount to withdraw: 2000
# Withdrawal successful! Remaining balance: ₹8000.0
# Enter your choice: 2
# Enter amount to deposit: 3000
# Deposit successful! Updated balance: ₹11000.0

