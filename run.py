import gspread
from google.oauth2.service_account import Credentials
import os
from tabulate import tabulate
from datetime import datetime
import time
import pandas as pd

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
    If it's a new trip run a while loop until the name of the trip is new.
    """
    print("What would you like to do?")
    print(tabulate([[1, "Create new trip"], [2, "See existing trips"]]))

    while True:
        trips = [trip.title for trip in WORKSHEETS]
        user_choice = input("Please, select your prefered option (1 or 2):\n")
        validated_choice = validate_user_choice(user_choice, range(1, 3))
        validated_choice_bool, validated_choice_num = validated_choice
        if validated_choice_bool:
            os.system("clear")
            if validated_choice_num == 1:
                while True:
                    trip_name = input("Enter the name of the trip\n")
                    if trip_name in trips:
                        os.system("clear")
                        print(f"The trip {trip_name} already exists")
                        print("Please select a different name.\n")
                    else:
                        print("Creating new trip...")
                        create_new_trip(trip_name)
                        break
            elif validated_choice_num == 2:
                load_trips()
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
        print(f"Invalid choice: {e}")
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
    print(f"{name} successfully created!")
    time.sleep(1.5)

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
                os.system("clear")
                welcome_menu()
            elif add_expense.lower() == "y":
                create_expense(name)


def create_expense(trip_name):
    """
    Call all functions to get expense data from user.
    Create an instance from expense class and call write_new_expense
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

    check_expense(write_new_expense, worksheet, expense, row_edit=0)


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
    Get input from the user for the name of the person.
    Give the possibility to cancel the process.
    If the data entered is invalid ask again.
    """
    while True:
        try:
            print("Enter a name for the expense")
            name = input("Example: 'John' or press 'C' to cancel:\n").title()
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


def check_expense(update_worksheet ,trip_name, expense, row_edit):
    """
    Loop asking if the data entered is correct. The user has the possibility
    to change any field. When the user is happy with the data entered, will call
    the update_worksheet paramete will call the appropiate function so that the
    entry will be either added or edited.
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
            update_worksheet(trip_name, expense, row_edit)
            break
        else:
            os.system("clear")
            print("The value entered is not valid. Please try again.\n")


def write_new_expense(worksheet, expense, row_edit):
    """
    Appends a new the expense to the trip spreadhseet.
    """
    worksheet = SHEET.worksheet(worksheet)
    expense_arr = [value for attr, value in expense.__dict__.items()]
    worksheet.append_row(expense_arr)


def load_trips():
    """
    Print existing trips or load the welcome menu if there aren't any.
    The user can select one of the trips.
    The function returns the name of the selected trip.
    """
    trips = {x + 1: worksheet.title for x, worksheet in enumerate(WORKSHEETS[1:])}
    options_arr = [key for key, value in trips.items()]
    options = ", ".join([str(key) for key, value in trips.items()])
    selected_trip = ""
    if not trips:
        print("There are currently no trips\n")
        welcome_menu()
    else:
        os.system("clear")
        print("These are the existing trips:")
        print(tabulate([(str(trip_num), trip) for trip_num, trip in trips.items()]))
        print(f"Select your prefered option: {options} or 'C' to go back.")
        while True:
            user_choice = input(f"Enter your selection:\n")
            if user_choice.lower() == "c":
                os.system("clear")
                welcome_menu()
            validated_choice = validate_user_choice(user_choice, options_arr)
            validated_choice_bool, validated_choice_num = validated_choice
            if validated_choice_bool:
                selected_trip = trips[validated_choice_num]
                select_trip(selected_trip)
                break


def select_trip(trip_name):
    """
    Select the worksheet containing the chosen trip.
    The user is presented with the options to:
        1. See the summary of the trip.
        2. Edit the trip.
        3. Delete the trip.
    A loop runs until the option chosen is valid.
    """
    worksheet = SHEET.worksheet(trip_name)
    data = worksheet.get_all_values()
    header = data[0]
    rows = data[1:]
    df = pd.DataFrame(rows, columns=header)
    os.system("clear")
    print(f"You've selected the {trip_name} trip.")
    print(f"There are {df.shape[0]} entries.\n")
    print("What would you like to do?")
    print(tabulate([[1, "See summary"], [2, "Edit trip"], [3, "Delete trip"]]))
    while True:
        user_choice = input("Please, select your prefered option:\n")
        validated_choice = validate_user_choice(user_choice, range(1, 5))
        validated_choice_bool, validated_choice_num = validated_choice
        if validated_choice_bool:
            os.system("clear")
            if validated_choice_num == 1:
                see_trip_summary(df)
                break
            elif validated_choice_num == 2:
                edit_trip(trip_name, df)
                break
            elif validated_choice_num == 3:
                delete_trip(trip_name, df)
                break


def see_trip_summary(df):
    """
    Print a table displaying how much each person spent.
    It also shows how much each has to pay/receive so that
    everyone pays the same amount
    """
    nr_of_persons = df["Name"].value_counts().shape[0]
    df['Cost'] = df['Cost'].str.replace(',', '.').astype(float) # Convert to float so that it can be added up
    total_cost = df['Cost'].sum() # Calculate the total cost of the trip
    avg_cost = total_cost / nr_of_persons # Calculate how much each person should pay
    sum_by_name = df.groupby("Name")["Cost"].sum() # Calculate how much each person has paid
    sum_by_name_list = [(name, value) for name, value in sum_by_name.items()] # Create list to be displayed
    header = ["Name", "Spent", "Price per person", "To pay (-) / Receive (+)"]
    cost_diff = [(name, value, round(avg_cost, 2), round(value - avg_cost, 2)) for name, value in sum_by_name_list]
    print(tabulate(cost_diff, headers=header, tablefmt="mixed_grid", numalign="center"))


def edit_trip(trip_name, df):
    """
    Show all entries for the selected trip. The user can choose between
    deleting, editing or adding an entry.
    """
    options_array = [option for option in df.index.to_numpy()]
    options_array_str = ", ".join([str(choice) for choice in options_array])
    print(f"These are all records for the {trip_name} trip:\n")
    show_trip_entries(df)
    print("Press 'e' to edit, 'd' to delete, or 'a' to add an entry")
    while True:
        user_choice = input("Select one of the above or 'c' to go back:\n")
        if user_choice not in ["e", "d", "a", "c"]:
            print("Invalid choice, please try again.")
            continue
        if user_choice == 'c':
            welcome_menu()
            break
        while True:
            if user_choice == 'e':
                print("Select the number of the entry you want to edit:")
                print(options_array_str)
                user_choice_edit_entry = input("Example '2':\n")
                validated_choice = validate_user_choice(user_choice_edit_entry, options_array)
                validated_choice_bool, validated_choice_num = validated_choice
                if validated_choice_bool:
                    print(f"You've chosen to edit {validated_choice_num}")
                    edit_trip_entry(trip_name, validated_choice_num)
                    break
            if user_choice == 'd':
                print("Select the number of the entry you want to delete:")
                print(options_array_str)
                user_choice_edit_entry = input("Example '2':\n")
                validated_choice = validate_user_choice(user_choice_edit_entry, options_array)
                validated_choice_bool, validated_choice_num = validated_choice
                if validated_choice_bool:
                    print(f"You've chosen to delete {validated_choice_num}")
                    delete_trip_entry(trip_name, validated_choice_num)
                    break
            if user_choice == "a":
                os.system("clear")
                print(f"You are creating a new entry for {trip_name}")
                create_expense(trip_name)
                print("Expense added successfully!")
                break
        break


def show_trip_entries(df):
    print(f"{df}\n")


def delete_trip_entry(trip_name, entry_ind):
    """
    The user can select an entry from the trip to delete.
    A summary of the selected entry will be displayed and the user
    must confirm that the entry should be deleted.
    """
    worksheet = SHEET.worksheet(trip_name)
    row_delete = entry_ind + 2 # +2 because the spreadsheet starts at 1 and the first line is the header
    values_list = worksheet.row_values(row_delete)
    header = ["Date", "Name", "Concept", "Cost", "Currency"]
    print("You are going to delete the following expense:")
    print(tabulate(zip(header, values_list)))
    user_choice = input("Press Y to confirm or N to discard the changes:\n")
    while True:
        if user_choice.lower() not in ["y", "n"]:
            print("That's not a valid choice, please try again.")
        elif user_choice.lower() == "y":
            worksheet.delete_rows(row_delete)
            print("Entry successfully deleted.")
            break
        else:
            welcome_menu()


def edit_trip_entry(trip_name, entry_ind):
    """
    The user can select an entry from the trip to edit.
    A summary of the selected entry will be displayed and the user
    must confirm that the entry should be edited.
    """
    worksheet = SHEET.worksheet(trip_name)
    row_edit = entry_ind + 2 # +2 because the spreadsheet starts at 1 and the first line is the header
    values_list = worksheet.row_values(row_edit)
    date = values_list[0]
    name = values_list[1]
    concept = values_list[2]
    cost = float(values_list[3].replace(',', '.')) # Convert to float from str
    currency = values_list[4]
    expense = Expense(date, name, concept, cost, currency)

    check_expense(overwrite_expense, trip_name, expense, row_edit)


def overwrite_expense(worksheet, expense, row_edit):
    """
    Overwrites the existing expense in the trip worksheet.
    """
    worksheet = SHEET.worksheet(worksheet)
    expense_arr = [value for attr, value in expense.__dict__.items()]
    row_edit_str = str(row_edit)
    worksheet.update(f"A{row_edit}:E{row_edit}" , [expense_arr])


def delete_trip(trip_name, df):
    """
    Display the trip entries and ask for the user confirmation
    before deleting it.
    """
    worksheet = SHEET.worksheet(trip_name)
    print(f"The {trip_name} contains the following entries:\n")
    print(f"{df}\n")
    print(f"Are you sure you want to delete it?\n")
    while True:
        user_choice = input("Press 'Y' to delete or 'N' to cancel:\n")
        if user_choice.lower() not in ["y", "n"]:
            print("Invalid choice, please try again")
        elif user_choice.lower() == "n":
            welcome_menu()
        elif user_choice.lower() == "y":
            SHEET.del_worksheet(worksheet)
            print(f"{trip_name} successfully deleted!")
            welcome_menu()


welcome_menu()
