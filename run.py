import gspread
from google.oauth2.service_account import Credentials
import os
from tabulate import tabulate
from pprint import pprint

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
        validated_choice = validated_number(user_choice)
        validated_choice_bool, validated_choice_num = validated_choice
        if validated_choice_bool:
            try:
                if validated_choice_num not in [1, 2]:
                    raise ValueError(
                        f"Invalid number, you selected {user_choice}. Please select 1 or 2"
                    )
            except ValueError as e:
                print(f"{e}. Please try again.\n")
            else:
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


def validated_number(data):
    """
    Check that the data provided is a number.
    Returns a tuple with:
        - A boolean indicating if the data provided is a number.
        - The value provided converted to an integer.
    """
    try:
        new_number = int(data)
    except ValueError as e:
        print(f"Invalid data: {e}. Please try again.\n")
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
    header = ["Date", "Name", "Concept", "Cost", "Currency", "Description"]
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


def create_expense():
    """
    Creates an expense
    """


welcome_menu()
