import gspread
from google.oauth2.service_account import Credentials

SCOPE = [
    "https://www.googleapis.com/auth/spreadsheets",
    "https://www.googleapis.com/auth/drive.file",
    "https://www.googleapis.com/auth/drive"
    ]

CREDS = Credentials.from_service_account_file('creds.json')
SCOPED_CREDS = CREDS.with_scopes(SCOPE)
GSPREAD_CLIENT = gspread.authorize(SCOPED_CREDS)
SHEET = GSPREAD_CLIENT.open('fruit_vendor')


def get_dispatched_data():
    """
    Get dispatched figure input from list
    """
    print("Calculate dispatched figure from the last market.")
    print("Data should be ten numbers separated by slash.")
    print("Example: 475/475/500/470/600/580/400/160/420/480\n")

    info_str = input("Enter your data here:")
    print(f"the data provided is {info_str}")


get_dispatched_data()
