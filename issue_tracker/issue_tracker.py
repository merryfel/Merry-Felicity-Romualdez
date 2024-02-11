import hashlib
from datetime import datetime
import getpass
import uuid

users = {}
issues = []




class Issue:
    def __init__(self, username, title, description, status, date_added, date_solved=None, ticket_number=None):
        self.username = username
        self.title = title
        self.description = description
        self.status = status
        self.date_added = date_added
        self.date_solved = date_solved
        self.ticket_number = ticket_number


def register():
    print("=== Register ===")
    username = input("Enter your username: ")
    password = getpass.getpass("Enter your password: ")
    # Encrypting the password
    hashed_password = hashlib.sha256(password.encode()).hexdigest()
    users[username] = hashed_password
    print("Registration successful!")


def login():
    print("=== Login ===")
    username = input("Enter your username: ")
    password = getpass.getpass("Enter your password: ")
    # Encrypting the password
    hashed_password = hashlib.sha256(password.encode()).hexdigest()
    if username in users and users[username] == hashed_password:
        print("Login successful!")
        return username  # Return the username upon successful login
    else:
        print("Invalid username or password.")
        return None  # Return None if login fails

class Account:
    def __init__(self, account_number, balance=0):
        self.account_number = account_number
        self.balance = balance
        self.transaction_history = []

    def view_account(self):
        print(f"Account Number: {self.account_number}")
        print(f"Balance: {self.balance}")

    def view_transactions(self):
        print("Transaction History:")
        for transaction in self.transaction_history:
            print(transaction)

    def add_transaction(self, transaction):
        self.transaction_history.append(transaction)


class Transaction:
    def __init__(self, amount, date, description, ticket_number):
        self.amount = amount
        self.date = date
        self.description = description
        self.ticket_number = ticket_number

    def __str__(self):
        return f"Amount: {self.amount}, Date: {self.date}, Description: {self.description}, Ticket Number: {self.ticket_number}"

def generate_ticket_number():
    return str(uuid.uuid4())

def add_issue(username):
    print("=== Add Issue ===")
    title = input("Enter the title of the issue: ")
    description = input("Enter the description of the issue: ")
    date_added = datetime.now().date()
    status = "Unsolved"
    ticket_number = generate_ticket_number()  # Generate a unique ticket number
    issues.append(Issue(username, title, description, status, date_added, ticket_number))
    print("Issue added successfully!")



def edit_issue():
    print("=== Edit Issue ===")
    print("Current issues:")
    for i, issue in enumerate(issues):
        print(f"{i+1}. {issue.title} - Status: {issue.status}")

    choice = int(input("Enter the number of the issue to edit: "))
    if 1 <= choice <= len(issues):
        new_status = input("Enter the new status for the issue: ")
        while True:
            date_solved = input("Enter the date the issue is resolved (YYYY-MM-DD): ")
            try:
                date_solved = datetime.strptime(date_solved, "%Y-%m-%d").date()
                break  # Exit the loop if the date is successfully parsed
            except ValueError:
                print("Invalid date format. Please enter the date in YYYY-MM-DD format.")

        issues[choice - 1].status = new_status
        issues[choice - 1].date_solved = date_solved
        print("Issue status updated successfully!")
    else:
        print("Invalid choice. No issue found.")


def view_issues():
    print("=== View Issues ===")
    # Get the username of the logged-in user
    username = input("Enter your username: ")  # Assuming the user logs in with their username

    # Check if the user exists and has issues
    if username in users:
        user_issues = [issue for issue in issues if issue.username == username]
        if user_issues:
            for i, issue in enumerate(user_issues):
                date_solved = issue.date_solved.strftime("%Y-%m-%d") if issue.date_solved else "Not Solved Yet"
                print(f"{i+1}. Title: {issue.title} - Description: {issue.description} - Status: {issue.status} - Date Added: {issue.date_added.strftime('%Y-%m-%d')} - Date Solved: {date_solved} - Ticket Number: {issue.ticket_number}")
        else:
            print("No issues to display for this user.")
    else:
        print("Invalid username.")


        
def delete_issue():
    print("=== Delete Issue ===")
    print("Current issues:")
    for i, issue in enumerate(issues):
        print(f"{i+1}. {issue.title} - Status: {issue.status}")

    choice = int(input("Enter the number of the issue to delete: "))
    if 1 <= choice <= len(issues):
        del issues[choice - 1]
        print("Issue deleted successfully!")
    else:
        print("Invalid choice. No issue found.")


def main():
    logged_in_username = None  # Initialize variable to store the logged-in username
    while True:
        print("\n===== Issue Tracker System =====")
        print("1. Login")
        print("2. Register")
        print("3. Exit")
        choice = input("Enter your choice: ")

        if choice == "1":
            logged_in_username = login()  # Store the returned username
            if logged_in_username:
                while True:
                    print("\n===== Welcome =====")
                    print("1. Add Issue")
                    print("2. Edit Issue")
                    print("3. Delete Issues")
                    print("4. View Issues")
                    print("5. Logout")
                    user_choice = input("Enter your choice: ")
                    if user_choice == "1":
                        add_issue(logged_in_username)  # Pass the logged-in username
                    elif user_choice == "2":
                        edit_issue()
                    elif user_choice == "3":
                        delete_issue()
                    elif user_choice == "4":
                        view_issues()
                    elif user_choice == "5":
                        logged_in_username = None  # Reset the logged-in username upon logout
                        break
                    else:
                        print("Invalid choice. Please try again.")

        elif choice == "2":
            register()
        elif choice == "3":
            print("Exiting...")
            break
        else:
            print("Invalid choice. Please try again.")


if __name__ == "__main__":
    main()