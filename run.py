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
    print("Data should be ten numbers separated by commas.")
    print("Example: 475,475,500,470,600,580,400,160,420,480\n")

    data_str = input("Enter your data here: ")
    dispatched_data = data_str.split(",")
    validate_data(dispatched_data)


def validate_data(values):
    """
    Inside the try, converts all string values into integers.
    Raises ValueError if strings can not be converted into int,
    or if there aren't exactly 10 values.
    """
    try:
        if len(values) != 10:
            raise ValueError(
                f"Exactly 10 values required, you provided {len(values)}"
            )
    except ValueError as e:
        print(f"Invalid data: {e}, please try again.\n")


get_dispatched_data()
