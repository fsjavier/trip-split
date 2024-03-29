import gspread
from google.oauth2.service_account import Credentials
import os
from tabulate import tabulate
from datetime import datetime
import time
import pandas as pd
import colorama
import pyfiglet
from colorama import Fore
import warnings

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

colorama.init(autoreset=True)  # Initialize colorama

warnings.simplefilter("ignore")  # Avoid printing deprecation message


def clear_terminal():
    """
    Clears terminal window for better screen readability.
    Method found on StackOverflow:
    https://stackoverflow.com/questions/2084508/clear-terminal-in-python
    """
    os.system("cls" if os.name == "nt" else "clear")


def welcome_menu():
    """
    Print welcome message and ask to choose between create trip and see list.
    Check the option chosen in valid and call the corresponding function.
    Run a while loop asking for input until it's a valid option.
    If it's a new trip run a while loop until the name of the trip is new.
    """
    worksheets = SHEET.worksheets()

    welcome_message = pyfiglet.figlet_format(
        "Welcome to\n\tTrip Split"
        )
    print(welcome_message)
    print("Effortlessly track trip expenses:\n")
    print(" * Add, edit, or delete trips and their costs.")
    print(" * Gain insights into individual expenditures.\n")
    print("What would you like to do?\n")
    print(tabulate([[1, "Create new trip"], [2, "See existing trips"]]))
    print("")

    while True:
        trips = [trip.title for trip in worksheets]
        user_choice = input("Please, enter your prefered option (1 or 2):\n")
        validated_choice = validate_user_choice(user_choice, range(1, 3))
        validated_choice_bool, validated_choice_num = validated_choice
        if validated_choice_bool:
            clear_terminal()
            if validated_choice_num == 1:
                while True:
                    trip_name = input("Enter the name of the trip\n")
                    if trip_name in trips:
                        clear_terminal()
                        print(
                            Fore.RED +
                            f"The {trip_name} trip already exists.\n"
                        )
                        print("Please select a different name.\n")
                    else:
                        print("Creating new trip...\n")
                        create_new_trip(trip_name)
            elif validated_choice_num == 2:
                load_trips()


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
        if new_number not in choices:
            raise ValueError(
                f"You entered {new_number}."
            )
    except ValueError as e:
        print(Fore.RED + "\nInvalid choice: " + Fore.RESET + f"{e}\n")
        return (False, 0)

    return (True, new_number)


def create_new_trip(name):
    """
    Create a new worksheet for the trip with the name provided by the user.
    The worksheet is populated with the column headers.
    A loop asks the user to provide expenses, calling the appropiate function.
    """
    print("Please select your base currency.")
    print("All your expenses will be converted to this currency")
    print("and will be used to show the summary of your trip.\n")
    chosen_currency = get_currency(name)

    SHEET.add_worksheet(title=name, rows=100, cols=20)
    worksheet = SHEET.worksheet(name)
    header = [
        "Date",
        "Name",
        "Concept",
        "Cost",
        "Currency",
        "Cost_chosen_currency",
        "Chosen_currency"]
    worksheet.append_row(header)
    worksheet.update("J1", [[chosen_currency]])

    print(Fore.YELLOW + f"{name} successfully created!")
    time.sleep(1.5)

    while True:
        clear_terminal()
        add_expense = input(
            f"Do you want to add an expense for your {name} trip? (Y / N):\n"
        )
        try:
            if add_expense.lower() not in ["y", "n"]:
                raise ValueError(
                    f"You selected {add_expense}. Please select Y or N"
                )
        except ValueError as e:
            print(Fore.RED + "Invalid option: " + Fore.RESET + f"{e}")
            time.sleep(1.5)
        else:
            if add_expense.lower() == "n":
                clear_terminal()
                select_trip(name)
            elif add_expense.lower() == "y":
                create_expense(name)


def create_expense(trip_name):
    """
    Call all functions to get expense data from user.
    Create an instance from expense class and call write_new_expense
    function passing the expense.
    """
    worksheet = trip_name

    clear_terminal()
    date = get_date(trip_name)
    name = get_name(trip_name)
    concept = get_concept(trip_name)
    cost = get_cost(trip_name)
    currency = get_currency(trip_name)

    expense = Expense(trip_name, date, name, concept, cost, currency)

    check_expense(write_new_expense, worksheet, expense, row_edit=0)


def get_date(trip_name):
    """
    Get date input from the user and format it to date and return it as str.
    Give the possibility to cancel the process.
    If the data entered is invalid ask again.
    """
    date_format = "%d/%m/%Y"

    while True:
        try:
            print("Enter date in the following format dd/mm/yyyy")
            date = input("Example: 30/06/2023 or enter C to cancel:\n")
            if date.lower() == "c":
                clear_terminal()
                select_trip(trip_name)
            else:
                date_obj = datetime.strptime(date, date_format)
                clear_terminal()
                return date_obj.strftime("%d/%m/%Y")
        except ValueError:
            print(
                Fore.RED + "The date entered is not valid, please try again.\n"
            )


def get_name(trip_name):
    """
    Get input from the user for the name of the person.
    Give the possibility to cancel the process.
    If the data entered is invalid ask again.
    """
    while True:
        try:
            print("Enter the name of the person who paid.")
            name = input("Example: John or enter C to cancel:\n").title()
            if name.lower() == "c":
                clear_terminal()
                select_trip(trip_name)
            clear_terminal()
            return name
        except ValueError:
            print(
                Fore.RED + "The name entered is not valid, please try again.\n"
            )


def get_concept(trip_name):
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

    print(
        "Enter the code number of the concept better describing the expense.\n"
    )
    print(
        tabulate(
            [(str(code), concept) for code, concept in concepts.items()],
            headers=concepts_headers,
            tablefmt="mixed_grid"
        )
    )
    print("")

    while True:
        user_choice = input("Enter 1, 2, 3, 4, 5, 6 or C to cancel:\n")
        validated_choice = validate_user_choice(user_choice, range(1, 7))
        validated_choice_bool, validated_choice_num = validated_choice
        if user_choice.lower() == "c":
            clear_terminal()
            select_trip(trip_name)
        elif validated_choice_bool:
            clear_terminal()
            return concepts[validated_choice_num]


def get_cost(trip_name):
    """
    Get input from the user for the cost.
    Give the possibility to cancel the process.
    If the data entered is invalid ask again.
    """
    while True:
        try:
            print("Enter the amount of the expense.")
            cost = input("Example: 19.95 or press C to cancel:\n")
            if cost.lower() == "c":
                clear_terminal()
                select_trip(trip_name)
            cost_float = float(cost)
            clear_terminal()
            return cost_float
        except ValueError:
            print(Fore.RED + f"{cost} is not valid input, please try again.\n")


def get_currency(trip_name):
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

    print("Select one of the following code options:\n")
    print(
        tabulate(
            [(str(code), currency) for code, currency in currencies.items()],
            headers=currencies_headers,
            tablefmt="mixed_grid"
        )
    )

    while True:
        print("")
        user_choice = input("Enter 1, 2, 3, or C to cancel:\n")
        validated_choice = validate_user_choice(user_choice, range(1, 4))
        validated_choice_bool, validated_choice_num = validated_choice
        try:
            if user_choice.lower() == "c":
                clear_terminal()
                select_trip(trip_name)
            elif validated_choice_bool:
                clear_terminal()
                return currencies[validated_choice_num]
        except gspread.exceptions.WorksheetNotFound:
            print("The trip creation process has been aborted.")
            time.sleep(1.5)
            clear_terminal()
            welcome_menu()


class Expense:
    """
    Expense class.
    Contains all necessary attributes that a user must provide.
    Chosen currency and exchange rate are returned trhough the methods.
    """
    def __init__(self, trip_name, date, name, concept, cost, currency):
        """
        Initialize the Expense object.
        """
        self.trip_name = trip_name
        self.date = date
        self.name = name
        self.concept = concept
        self.cost = cost
        self.currency = currency

    def get_chosen_currency(self):
        """
        Retrieves the chosen currency from the worksheet an return its value.
        """
        worksheet = SHEET.worksheet(self.trip_name)
        chosen_currency = worksheet.acell(
            "J1"
        ).value  # J1 is the cell storing the value in crate_new_trip()
        return chosen_currency

    def get_exchange_rate(self):
        """
        Get the exchage rate from the 'currency_exchange' worksheet.
        Return the value based on the currencies entered by the user
        when creating the trip and expense.
        """
        worksheet_currencies = SHEET.worksheet("currency_exchange")
        currencies_list = worksheet_currencies.get_all_values()

        worksheet_trip = SHEET.worksheet(self.trip_name)

        currency_base = self.currency
        currency_other = worksheet_trip.acell('J1').value
        matching_row = 0

        # Loop to find the row where base currency and currency other match
        for row in currencies_list:
            if row[0] == currency_base and row[2] == currency_other:
                matching_row = row
                break

        exchange_rate = matching_row[3]
        return exchange_rate


def check_expense(update_worksheet, trip_name, expense, row_edit):
    """
    Loop asking if the data entered is correct. The user has the possibility
    to change any field. Then the update_worksheet parameter will call the
    appropiate function so that the entry will be either added or edited.
    The user has the possibility to cancel at any time.
    """
    while True:
        record = [
            (attr, value) for attr, value in expense.__dict__.items()
        ]  # Iterate over the attributes of the class
        record_to_display = record[
            1:
        ]  # Index 0 is the trip name, which won't be added
        print(f"This is the record:\n")
        print(tabulate(record_to_display))
        print("Press Y if you want to confirm the expense")
        print("Press C if you want to cancel\n")
        print("If you want to make a change, enter name of the field.")
        field = input("Example: name\n")
        if field.lower() == "date":
            new_date = get_date(trip_name)
            expense.date = new_date
            clear_terminal()
        elif field.lower() == "name":
            new_name = get_name(trip_name)
            expense.name = new_name
            clear_terminal()
        elif field.lower() == "concept":
            new_concept = get_concept(trip_name)
            expense.concept = new_concept
            clear_terminal()
        elif field.lower() == "cost":
            new_cost = get_cost(trip_name)
            expense.cost = new_cost
            clear_terminal()
        elif field.lower() == "currency":
            new_currency = get_currency(trip_name)
            expense.currency = new_currency
            clear_terminal()
        elif field.lower() == "c":
            time.sleep(0.5)
            clear_terminal()
            select_trip(trip_name)
        elif field.lower() == "y":
            update_worksheet(trip_name, expense, row_edit)
            break
        else:
            clear_terminal()
            print("The value entered is not valid. Please try again.\n")


def write_new_expense(worksheet, expense, row_edit):
    """
    Appends a new the expense to the trip spreadhseet.
    Call methods from expense class to get the exchange rate
    of the chosen currency.
    """
    worksheet = SHEET.worksheet(worksheet)
    expense_arr = [
        value for attr, value in expense.__dict__.items()
    ]  # Iterate over the attributes of the class
    expense_arr_write = expense_arr[
        1:
    ]  # Index 0 is the trip name, which won't be added

    exchange_rate = float(expense.get_exchange_rate().replace(",", "."))
    cost_chosen_currency = (
        expense_arr[4] * exchange_rate
    )  # Index 4 is the cost

    chosen_currency = expense.get_chosen_currency()

    expense_arr_write.append(cost_chosen_currency)
    expense_arr_write.append(chosen_currency)
    worksheet.append_row(
        expense_arr_write,
        table_range="A:G"
    )  # Need to specify range to avoid appending in wrong place


def load_trips():
    """
    Print existing trips or load the welcome menu if there aren't any.
    The user can select one of the trips.
    The function returns the name of the selected trip.
    """
    worksheets = SHEET.worksheets()
    trips = {
        x + 1: worksheet.title for x, worksheet in enumerate(worksheets[1:])
    }
    options_arr = [key for key, value in trips.items()]
    options = ", ".join([str(key) for key, value in trips.items()])
    selected_trip = ""
    if not trips:
        print("There are currently no trips\n")
        time.sleep(1.5)
        clear_terminal()
        welcome_menu()
    else:
        clear_terminal()
        print("These are the existing trips:\n")
        print(
            tabulate(
                [(str(trip_num), trip) for trip_num, trip in trips.items()]
            )
        )
        print("")
        while True:
            print("Enter the number of the trip you want to edit:")
            print(options)
            print("Or enter C to go back.\n")
            user_choice = input(f"Enter your selection:\n")
            if user_choice.lower() == "c":
                clear_terminal()
                welcome_menu()
            validated_choice = validate_user_choice(user_choice, options_arr)
            validated_choice_bool, validated_choice_num = validated_choice
            if validated_choice_bool:
                selected_trip = trips[validated_choice_num]
                select_trip(selected_trip)


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
    clear_terminal()
    print(f"You have selected the {trip_name} trip.")
    print(
        "There is 1 entry.\n"
        if df.shape[0] == 1
        else f"There are {df.shape[0]} entries.\n"
    )
    print("What would you like to do?\n")
    print(
        tabulate([[1, "See summary"], [2, "Edit trip"], [3, "Delete trip"]])
        + "\n"
    )
    while True:
        print("Please, enter the number of your prefered option:")
        user_choice = input("1, 2, 3 or enter C to go back:\n")
        validated_choice = validate_user_choice(user_choice, range(1, 4))
        validated_choice_bool, validated_choice_num = validated_choice
        if validated_choice_bool or user_choice.lower() == "c":
            clear_terminal()
            if user_choice.lower() == "c":
                load_trips()
            elif validated_choice_num == 1:
                see_trip_summary(trip_name, df)
                print("")
                input("Enter any key to go back:\n")
                time.sleep(0.5)
                select_trip(trip_name)
            elif validated_choice_num == 2:
                edit_trip(trip_name, df)
            elif validated_choice_num == 3:
                delete_trip(trip_name, df)


def see_trip_summary(trip_name, df):
    """
    Print a table displaying how much each person spent.
    It also shows how much each has to pay/receive so that everyone
    pays the same amount.
    All displayed amounts have been converted to the user's currency.
    """
    if df.shape[0] == 0:
        print("There are no entries for this trip\n")

    else:
        chosen_curr = df["Chosen_currency"][0]
        nr_of_persons = df["Name"].value_counts().shape[0]
        df["Cost_chosen_currency"] = (
            df["Cost_chosen_currency"].str.replace(",", ".").astype(float)
        )  # Convert to float so that it can be added up
        total_cost = df[
            "Cost_chosen_currency"
        ].sum()  # Calculate the total cost of the trip
        total_cost_rnd = round(total_cost, 2)
        avg_cost = (
            total_cost / nr_of_persons
        )  # Calculate how much each person should pay
        sum_by_name = df.groupby("Name")[
            "Cost_chosen_currency"
        ].sum()  # Calculate how much each person has paid
        sum_by_name_list = [
            (name, value) for name, value in sum_by_name.items()
        ]  # Create list to be displayed
        header = [
            "Name",
            "Spent",
            "Price per person",
            "To pay (-) / Receive (+)"
        ]
        cost_diff = [
            (
                name,
                round(value, 2),
                round(avg_cost, 2),
                round(value - avg_cost, 2)
            )
            for name, value in sum_by_name_list]

        print(f"This is the summary of the {trip_name} trip:\n")
        print(f"You have selected {chosen_curr} as your currency.")
        print(
            f"Total cost of the trip in {chosen_curr} is {total_cost_rnd}.\n"
        )
        print(
            tabulate(
                cost_diff,
                headers=header,
                tablefmt="mixed_grid",
                numalign="center"
            )
        )


def edit_trip(trip_name, df):
    """
    Show all entries for the selected trip. The user can choose between
    deleting, editing or adding an entry.
    """
    options_array = [option for option in df.index.to_numpy()]
    options_array_str = ", ".join([str(choice) for choice in options_array])
    show_trip_entries(trip_name, df)
    if df.shape[0] == 0:
        while True:
            print("Enter A to add an entry")
            user_choice = input("Or enter C to go back:\n")
            if user_choice.lower() not in ["a", "c"]:
                print(Fore.RED + "Invalid choice, please try again.")
                continue
            if user_choice.lower() == "c":
                time.sleep(0.5)
                clear_terminal()
                select_trip(trip_name)
            elif user_choice.lower() == "a":
                clear_terminal()
                print(f"You are creating a new entry for {trip_name}")
                create_expense(trip_name)
                print(Fore.YELLOW + "Expense added successfully!")
                time.sleep(1)
                select_trip(trip_name)
    else:
        while True:
            print("Enter E to edit, D to delete, or A to add an entry.")
            user_choice = input("Or enter C to go back:\n")
            if user_choice.lower() not in ["e", "d", "a", "c"]:
                print("")
                print(Fore.RED + "Invalid choice, please try again.\n")
                continue
            if user_choice.lower() == "c":
                time.sleep(0.5)
                clear_terminal()
                select_trip(trip_name)
            if user_choice.lower() == "e":
                edit_delete_entry(
                    options_array,
                    options_array_str,
                    trip_name,
                    edit_trip_entry,
                    option_chosen="edit"
                )
            if user_choice.lower() == "d":
                edit_delete_entry(
                    options_array,
                    options_array_str,
                    trip_name,
                    delete_trip_entry,
                    option_chosen="delete"
                )
            if user_choice.lower() == "a":
                clear_terminal()
                print(f"You are creating a new entry for {trip_name}")
                create_expense(trip_name)
                print(Fore.YELLOW + "Expense added successfully!")
                time.sleep(1)
                select_trip(trip_name)


def edit_delete_entry(
    options_array,
    options_array_str,
    trip_name,
    edit_delete_trip_entry,
    option_chosen
):
    """
    Takes in the parameters necessary to either edit or delete an entry.
    Validates the user choice and calls the appropiate function.
    """
    while True:
        print(f"Select the number of the entry you want to {option_chosen}:")
        print(options_array_str)
        user_choice_edit_entry = input("Enter one of the above options:\n")
        validated_choice = validate_user_choice(
            user_choice_edit_entry, options_array
        )
        validated_choice_bool, validated_choice_num = validated_choice
        if validated_choice_bool:
            clear_terminal()
            print(
                f"You will {option_chosen} entry number {validated_choice_num}"
            )
            edit_delete_trip_entry(trip_name, validated_choice_num)


def show_trip_entries(trip_name, df):
    """
    Check if the worksheet is empty.
    If it's not empty displays the expenses.
    """
    relevant_columns = ["Date", "Name", "Concept", "Cost", "Currency"]
    if df.shape[0] == 0:
        print(f"The {trip_name} trip is empty.\n")
    else:
        print(f"The {trip_name} trip contains the following entries:\n")
        print(f"{df[relevant_columns]}\n")


def delete_trip_entry(trip_name, entry_ind):
    """
    The user can select an entry from the trip to delete.
    A summary of the selected entry will be displayed and the user
    must confirm that the entry should be deleted.
    """
    worksheet = SHEET.worksheet(trip_name)
    row_delete = (
        entry_ind + 2
    )  # +2 because worksheet starts at 1 and the first line is the header
    values_list = worksheet.row_values(row_delete)
    header = ["Date", "Name", "Concept", "Cost", "Currency"]
    print("You are going to delete the following expense:")
    print(tabulate(zip(header, values_list)))
    while True:
        user_choice = input(
            "Enter "
            + Fore.RED + "Y to delete"
            + Fore.RESET + " or N to cancel:\n"
        )
        if user_choice.lower() not in ["y", "n"]:
            print(
                Fore.RED +
                f"{user_choice} is not a valid choice, please try again."
            )
        elif user_choice.lower() == "y":
            worksheet.delete_rows(row_delete)
            print(Fore.YELLOW + "Entry successfully deleted.")
            time.sleep(1)
            clear_terminal()
            select_trip(trip_name)
        elif user_choice.lower() == "n":
            select_trip(trip_name)


def edit_trip_entry(trip_name, entry_ind):
    """
    The user can select an entry from the trip to edit.
    A summary of the selected entry will be displayed and the user
    must confirm that the entry should be edited.
    """
    worksheet = SHEET.worksheet(trip_name)
    row_edit = (
        entry_ind + 2
    )  # +2 because worksheet starts at 1 and the first line is the header
    values_list = worksheet.row_values(row_edit)
    date = values_list[0]
    name = values_list[1]
    concept = values_list[2]
    cost = float(values_list[3].replace(",", "."))  # Convert to float from str
    currency = values_list[4]
    expense = Expense(trip_name, date, name, concept, cost, currency)

    check_expense(overwrite_expense, trip_name, expense, row_edit)
    time.sleep(1.5)
    clear_terminal()
    select_trip(trip_name)


def overwrite_expense(worksheet, expense, row_edit):
    """
    Overwrites the existing expense in the trip worksheet.
    """
    worksheet = SHEET.worksheet(worksheet)
    expense_arr = [value for attr, value in expense.__dict__.items()]
    expense_arr_write = expense_arr[
        1:
    ]  # Index 0 is the trip name, which won't be added

    exchange_rate = float(expense.get_exchange_rate().replace(",", "."))
    cost_chosen_currency = (
        expense_arr[4] * exchange_rate
    )  # Index 4 is the cost
    chosen_currency = expense.get_chosen_currency()

    expense_arr_write.append(cost_chosen_currency)
    expense_arr_write.append(chosen_currency)

    worksheet.update(f"A{row_edit}:G{row_edit}", [expense_arr_write])
    print(Fore.YELLOW + "Expense successfully edited!")


def delete_trip(trip_name, df):
    """
    Display the trip entries and ask for the user confirmation
    before deleting it.
    """
    worksheet = SHEET.worksheet(trip_name)
    show_trip_entries(trip_name, df)
    print(f"Are you sure you want to delete it?\n")
    print(Fore.YELLOW + "This action is not reversible")
    while True:
        user_choice = input(
            "Enter "
            + Fore.RED + "Y to delete"
            + Fore.RESET + " or N to cancel:\n"
        )
        if user_choice.lower() not in ["y", "n"]:
            print(Fore.RED + "Invalid choice, please try again.\n")
        elif user_choice.lower() == "n":
            select_trip(trip_name)
        elif user_choice.lower() == "y":
            SHEET.del_worksheet(worksheet)
            print(Fore.YELLOW + f"{trip_name} successfully deleted!")
            time.sleep(2)
            clear_terminal()
            welcome_menu()


def main():
    """
    Run the programm.
    """
    welcome_menu()


main()
