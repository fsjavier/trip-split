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
        os.system("clear")
        add_expense = input(f"Do you want to add an expense for your {name} trip? (Y / N):\n")
        try:
            if add_expense.lower() not in ["y", "n"]:
                raise ValueError(f"You selected {add_expense}. Please select Y or N")
        except ValueError as e:
            print(f"Invalid option: {e}")
        else:
            if add_expense.lower() == "n":
                break
            elif add_expense.lower() == "y":
                create_expense(name)


def create_expense(trip_name):
    """
    Call all functions to get expense data from user.
    Create an instance from expense class and call write_expense
    function passing the expense.
    """
    worksheet = trip_name

    os.system("clear")
    date = get_date()
    name = get_name()
    concept = get_concept()
    cost = get_cost()
    currency = get_currency()

    expense = Expense(date, name, concept, cost, currency)

    check_expense(worksheet, expense)


def get_date():
    """
    Get date input from the user and format it to date and return it as str.
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

    os.system("clear")
    return date_obj.strftime('%d/%m/%Y')


def get_name():
    """
    Get input from the user for the name of the expense.
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
            os.system("clear")
            return name
        except ValueError:
            print("The name entered is not valid, please try again")


def get_concept():
    """
    Get concept input from the user from the list of options.
    Give the possibility to cancel the process.
    If the data entered is invalid ask again.
    """
    concepts = {
        1: "Travel",
        2: "Meals",
        3: "Accomodation",
        4: "Supermarket",
        5: "Shopping",
        6: "Other"
    }
    concepts_headers = ["Code", "Concept"]

    print("Select one of the following code options (1 to 6)")
    print(tabulate([(str(code), concept) for code, concept in concepts.items()], headers=concepts_headers, tablefmt="mixed_grid"))

    while True:
        user_choice = input("Example: '1' or press 'C' to cancel:\n")
        validated_choice = validate_user_choice(user_choice, range(1, 7))
        validated_choice_bool, validated_choice_num = validated_choice
        if user_choice.lower() == "c":
            os.system('clear')
            welcome_menu()
        elif validated_choice_bool:
            os.system("clear")
            return concepts[validated_choice_num]


def get_cost():
    """
    Get input from the user for the cost.
    Give the possibility to cancel the process.
    If the data entered is invalid ask again.
    """
    print("Enter a cost for the expense")
    while True:
        try:
            cost = input("Example: '19.95' or press 'C' to cancel:\n")
            if cost.lower() == "c":
                os.system('clear')
                welcome_menu()
            cost_float = float(cost)
            os.system("clear")
            return cost_float
        except ValueError:
            print("The cost entered is not valid, please try again")


def get_currency():
    """
    Get currency input from the user from the list of options.
    Give the possibility to cancel the process.
    If the data entered is invalid ask again.
    """
    currencies = {
        1: "EUR",
        2: "GBP",
        3: "USD"
    }
    currencies_headers = ["Code", "Currency"]

    print("Select one of the following code options (1 to 3)")
    print(tabulate([(str(code), currency) for code, currency in currencies.items()], headers=currencies_headers, tablefmt="mixed_grid"))

    while True:
        user_choice = input("Example: '1' or press 'C' to cancel:\n")
        validated_choice = validate_user_choice(user_choice, range(1, 4))
        validated_choice_bool, validated_choice_num = validated_choice
        if user_choice.lower() == "c":
            os.system('clear')
            welcome_menu()
        elif validated_choice_bool:
            os.system("clear")
            return currencies[validated_choice_num]


class Expense:
    def __init__(self, date, name, concept, cost, currency):
        self.date = date
        self.name = name
        self.concept = concept
        self.cost = cost
        self.currency = currency


def check_expense(trip_name, expense):
    """
    Loop asking if the data entered is correct. The user has the possibility
    to change any field. When the user is happy with the data entered, will call
    the write_expense function and then can choose to add another expense.
    The user has the possibility to cancel at any time.
    """
    worksheet = SHEET.worksheet(trip_name)
    while True:
        print(f"You have added the following information for your {trip_name} trip:")
        print(tabulate([(attr, value) for attr, value in expense.__dict__.items()]))
        print("Press 'Y' if you want to confirm the expense")
        print("Press 'C' if you want to cancel")
        print("If you want to make a change, enter the field you want to modify")
        field = input("Example: name\n")
        if field.lower() == "date":
            new_date = get_date()
            expense.date = new_date
            os.system("clear")
        elif field.lower() == "name":
            new_name = get_name()
            expense.name = new_name
            os.system("clear")
        elif field.lower() == "concept":
            new_concept = get_concept()
            expense.concept = new_concept
            os.system("clear")
        elif field.lower() == "cost":
            new_cost = get_cost()
            expense.cost = new_cost
            os.system("clear")
        elif field.lower() == "currency":
            new_currency = get_currency()
            expense.currency = new_currency
            os.system("clear")
        elif field.lower() == "c":
            welcome_menu()
        elif field.lower() == "y":
            write_expense(worksheet, expense)
            break
        else:
            os.system("clear")
            print("The value entered is not valid. Please try again.\n")


def write_expense(worksheet, expense):
    """
    Writes the expense to the trip spreadhseet.
    """
    expense_arr = [value for attr, value in expense.__dict__.items()]
    worksheet.append_row(expense_arr)


welcome_menu()
