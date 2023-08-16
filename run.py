import gspread
from google.oauth2.service_account import Credentials
import os
from tabulate import tabulate
from datetime import datetime

# Every Google account has as an IAM (Identity and Access Management)
# configuration which specifies what the user has access to.
# The SCOPE lists the APIs that the program should access in order to run.

SCOPE = [
    "https://www.googleapis.com/auth/spreadsheets",
    "https://www.googleapis.com/auth/drive.file",
    "https://www.googleapis.com/auth/drive"
    ]

CREDS = Credentials.from_service_account_file("creds.json")
SCOPED_CREDS = CREDS.with_scopes(SCOPE)
GSPREAD_CLIENT = gspread.authorize(SCOPED_CREDS)
SHEET = GSPREAD_CLIENT.open("trip_split")

WORKSHEETS = SHEET.worksheets()


def welcome_menu():
    """
    Print welcome message and ask to choose between create trip and see list.
    Check the option chosen in valid and call the corresponding function.
    Run a while loop asking for input until it's a valid option.
    """
    print("Welcome to Trip Split\n")
    print("What would you like to do?")
    print(tabulate([[1, "Create new trip"], [2, "See existing trips"]]))

    while True:
        user_choice = input("Please, select your prefered option (1 or 2):\n")
        validated_choice = validate_user_choice(user_choice, range(1, 3))
        validated_choice_bool, validated_choice_num = validated_choice
        if validated_choice_bool:
            if validated_choice_num == 1:
                os.system('clear')
                trip_name = input("Enter the name of the trip\n")
                print("Creating new trip...")
                create_new_trip(trip_name)
                print(f"{trip_name} successfully created!")
                break
            elif validated_choice_num == 2:
                print(f"You chose {user_choice}")
                break


def validate_user_choice(data, choices):
    """
    Check that the data provided is a number within
    the possible options to choose from.
    Returns a tuple with:
        - A boolean indicating if the data provided is a number.
        - The value provided converted to an integer.
    """
    try:
        new_number = int(data)
        choices_str = [str(num) for num in choices]
        choices_str_list = ", ".join(choices_str)
        if new_number not in choices:
            raise ValueError(
                f"You selected {new_number}.\nSelect one of the following options: {choices_str_list}"
            )
    except ValueError as e:
        print(f"Invalid data: {e}")
        return (False, 0)

    return (True, new_number)


def create_new_trip(name):
    """
    Create a new worksheet for the trip with the name provided by the user.
    The worksheet is populated with the column headers.
    A loop asks the user to provide expenses, calling the appropiate function.
    """
    SHEET.add_worksheet(title=name, rows=100, cols=20)
    worksheet = SHEET.worksheet(name)
    header = ["Date", "Name", "Concept", "Cost", "Currency"]
    worksheet.append_row(header)

    while True:
        add_expense = input("Do you want to add an expense? (Y / N):\n")
        try:
            if add_expense.lower() not in ["y", "n"]:
                raise ValueError(f"You selected {add_expense}. Please select Y or N")
        except ValueError as e:
            print(f"Invalid option: {e}")
        else:
            if add_expense.lower() == "n":
                break
            elif add_expense.lower() == "y":
                create_expense()


class Expense:
    def __init__(self, date, name, concept, cost, currency):
        self.date = date
        self.name = name
        self.concept = concept
        self.cost = cost
        self.currency = currency


def create_expense():
    """
    Creates an expense
    """
    # concepts = {
    #     1: "Travel",
    #     2: "Food",
    #     3: "Other"
    # }

    # currencies = {
    #     1: "EUR",
    #     2: "GBP",
    #     3: "USD"
    # }

    date = get_date()
    name = get_name()
    # concept
    # cost
    # currency

    # expense = Expense(date, name, concept, cost, currency)

    # write_expense(expense)


def get_date():
    """
    Get date input from the user and format it to date.
    Give the possibility to cancel the process.
    If the data entered is invalid ask again.
    """
    date_format = '%d/%m/%Y'

    while True:
        try:
            print("Enter date in the following format dd/mm/yyyy")
            date = input("Example: 31/06/2023 or press 'C' to cancel:\n")
            if date.lower() == "c":
                os.system('clear')
                welcome_menu()
            else:
                date_obj = datetime.strptime(date, date_format)
                break
        except ValueError:
            print("The date entered is not valid, please try again")

    return date_obj


def get_name():
    """
    Get input from the user for the name of the expense
    Give the possibility to cancel the process.
    If the data entered is invalid ask again.
    """
    while True:
        try:
            print("Enter a name for the expense")
            name = input("Example: 'Cinema tickets' or press 'C' to cancel:\n")
            if name.lower() == "c":
                os.system('clear')
                welcome_menu()
            break
        except ValueError:
            print("The name entered is not valid, please try again")

    return name


def write_expense(expense):
    pass


welcome_menu()
