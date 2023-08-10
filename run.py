import gspread
from google.oauth2.service_account import Credentials
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

currency = SHEET.worksheet("currency_exchange")
pprint(currency.get_all_values())
