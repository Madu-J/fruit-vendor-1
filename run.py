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
    while True:
       print("Calculate dispatched from stock list.")
       print("Data should be ten numbers separated by commas.")
       print("Example: 475,475,500,470,600,580,400,160,420,480\n")

       data_str = input("Enter your data here: ")

       dispatched_data = data_str.split(",")

       if validate_data(dispatched_data):
        print("Data is valid!")
        break

    return dispatched_data


def validate_data(values):
    """
    Inside the try, converts all string values into integers.
    Raises ValueError if strings can not be converted into int,
    or if there aren't exactly 10 values.
    """
    print(values)
    try:
        [int(value) for value in values]
        if len(values) != 10:
            raise ValueError(
                f"Exactly 10 values required, you provided {len(values)}"
            )
    except ValueError as e:
        print(f"Invalid data: {e}, please try again.\n")
        return False

    return True


data = get_dispatched_data()
