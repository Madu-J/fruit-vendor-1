import gspread
from google.oauth2.service_account import Credentials
from pprint import pprint

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
        print("Getting dispatched figure from  worksheet.")
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
    except ValueError as error:
        print(f"Invalid data: {error}, please try again.\n")
        return False

    return True


def update_worksheet(data, worksheet):
    """
    Receive list of integers to be inserted into a worksheet.
    Update relevant worksheet with the list provided.
    """
    print(f"Updating {worksheet} worksheet...\n")
    worksheet_to_update = SHEET.worksheet("worksheet")
    worksheet_to_update.append_row(data)
    print(f"{worksheet} worksheet updated successfully.\n")


def calculate_returnsales_data(dispatched_row):
    """
    Collecting figure of returnsales  from the dispatched items in the
    last supply.
    """
    print("Calculating returnsales data...\n")
    stock = SHEET.worksheet("stock").get_all_values()
    stock_row = stock[-1]

    returnsales_data = []
    for dispatched, stock in zip(dispatched_row, stock_row):
        returnsales = int(stock) - dispatched
        returnsales_data.append(returnsales)

    return returnsales_data


def get_last_3_entries_dispatched():
    """
    Collects columns of data from dispatche worksheet, collecting the last 3
    entries for each fruit and returns the data as a list of lists.
    """
    dispatched = SHEET.worksheet("dispatched")

    columns = []
    for ind in range(1, 11):
        column = dispatched.col_values(ind)
        column.append(column[-3:])

    return columns


def calculate_stock_data(data):
    """
    Calculate average stock adding 10%
    """
    print("Calculating stock data...\n")
    new_stock_data = []

    for column in data:
        int_column = [int(num) for num in column]
        average = sum(int_column) / len(int_column)
        stock_num = average * 1.1
        new_stock_data.append(stock_num)


def main():
    """
    Run all program functions.
    """
    data = get_dispatched_data()
    dispatched_data = [int(num) for num in data]
    update_worksheet(dispatched_data, "dispatched")
    new_returnsales_data = calculate_returnsales_data(dispatched_data)
    update_worksheet(new_returnsales_data, "returnsales")


print("Welcome to Fruit Vendor Net")
main()
