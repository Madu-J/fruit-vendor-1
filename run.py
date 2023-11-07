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


def get_dispatch_data():
    """
    Get dispatch figure input from list
    """
    while True:
        print("Get dispatch data from  last supply.")
        print("Data should be ten numbers separated by commas.")
        print("Example: 475,475,500,470,600,580,400,160,420,480\n")

        data_str = input("Enter your data here: ")

        dispatch_data = data_str.split(",")

        if validate_data(dispatch_data):
            print("Data is valid!")
            break

    return dispatch_data


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


def update_dispatch_worksheet(data):
    """
    Update dispatch worksheet, add new row with data provided.
    """
    print("updating dispatch worksheet...\n")
    dispatch_worksheet = SHEET.worksheet("dispatch")
    dispatch_worksheet.append_row(data)
    print("dispatch worksheet updated successfully.\n")


def calculate_returnsales_data(dispatched_row):
    """
    Collecting figure of returnsales  from the dispatched items in the
    last supply.
    """
    print("Calculating returnsales data...\n")
    stock = SHEET.worksheet("stock").get_all_values()
    stock_row = [-1]

    returnsales_data = []
    for stock, dispatch in zip(stock_row, "dispatch_row"):
        returnsales = int(stock) - dispatch
        returnsales_data.append(returnsales)
    
    return returnsales_data


def main():
    """
    Run all program functions.
    """
    data = get_dispatch_data()
    dispatch_data = [int(num) for num in data]
    update_dispatch_worksheet(dispatch_data)
    new_returnsales_data = calculate_returnsales_data(dispatch_data)
    print(new_returnsales_data)

   
print("Welcome to Fruit Vendor Net")
main()
