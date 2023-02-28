# ========imports==========

from tabulate import tabulate

# ========The beginning of the class==========
class Shoe:
    """
    This is the shoe class. Within is initialisation, get shoe cost, get stock quantity of shoe,
    set stock quantity of shoe and output a string of th shoe details
    """

    def __init__(self, country, code, product, cost, quantity):
        """
        Initialises the object with country, code, product, cost, and quantity.
        """
        self.country = country
        self.code = code
        self.product = product
        self.cost = cost
        self.quantity = quantity

    def get_cost(self):
        """
        Output the cost of the shoe
        """
        return int(self.cost)

    def get_quantity(self):
        """
        Output the stock quantity of the shoe
        """
        return int(self.quantity)

    def set_quantity(self, quantity):
        """
        Set the stock quantity of the shoe
        """
        self.quantity = quantity
        pass

    def __str__(self):
        """
        Return the string of the shoe details
        """
        return f'{self.country},{self.code},{self.product},{self.cost},{self.quantity}'


# ====================Shoe list======================
"""
The list will be used to store a list of objects of shoes.
"""
shoe_list = []
# ==========Functions outside the class==============


def read_shoes_data():
    """
    Function to read in the contents of the shoe database and create an object for each shoe
    """

    # Loop to ensure the database file is loaded correctly
    try:
        with open('inventory.txt', 'r') as f:
            shoe_info = f.read().splitlines()
        print(shoe_info.pop(0))

        for item in shoe_info:
            shoe_object = Shoe(*item.split(','))
            shoe_list.append(shoe_object)

    # Errors if database cannot be read
    except FileNotFoundError:
        print("Shoe database not found")
    except Exception as error:
        print(f"Other error: {error}")
    finally:
        pass


def capture_shoes():
    """
    Function to allow a user to capture data
    about a shoe, use this data to create a shoe object
    and then append this object inside the shoe list.
    """
    country = input('Enter country: ')
    code = input('Enter code: ')
    product = input('Enter product: ')
    cost = input('Enter cost: ')
    quantity = input('Enter quantity: ')
    shoe_list.append(Shoe(country, code, product, cost, quantity))


def view_all():
    """
    Print out the database
    """
    # Create a list of shoe-detail sublists, print as table
    shoe_table = []
    for item in shoe_list:
        shoe_table.append(item.__str__().split(','))
    print(tabulate(shoe_table, headers=["Country", "Code", "Product", "Cost", "Quantity"]))


def re_stock():
    """
    Function to find the shoe object with the lowest quantity.
    Asks the user if they want to add this quantity of shoes and then updates it.
    This quantity should be updated on the file for this shoe.
    """

    # Create a stock list of the items and their quantities, turn into dictionary
    stock_list = [item.get_quantity() for item in shoe_list]
    shoe_dict = dict(zip(shoe_list, stock_list))

    # Identify and print the shoe with the lowest stock
    selected_shoe = min(shoe_dict, key=shoe_dict.get)
    print(f'Lowest stock is {selected_shoe.product}({selected_shoe.code}) '
          f'in {selected_shoe.country} with {min(stock_list)} units')

    # Get new stock amount from user and update stock quantity
    re_stock_val = int(input('Enter the updated stock amount: '))
    selected_shoe.set_quantity(re_stock_val)
    print(f'{selected_shoe.product}({selected_shoe.code}) stock is now {selected_shoe.get_quantity()} units')


def search_shoe():
    """
     Function to search for a shoe from the list
     using the shoe code and returns this object so that it will be printed.
    """
    code = input("Enter shoe code to search: ")

    # Initialise match flag, search through the shoe object, if there is match, print and change flag
    shoe_match = False
    for item in shoe_list:
        if item.code == code:
            shoe_match = True
            print(item)
    if shoe_match is False:
        print("No shoe found")


def value_per_item():
    """
    Function to calculate the total value for each item.
    Print this information on the console for all the shoes.
    """
    for item in shoe_list:
        print(f'{item.product}({item.code}) = {item.get_cost()*item.get_quantity()}')


def highest_qty():
    """
    Write code to determine the product with the highest quantity and
    print this shoe as being for sale.
    """
    
    # Create a stock list of the items and their quantities, turn into dictionary
    stock_list = [item.get_quantity() for item in shoe_list]
    shoe_dict = dict(zip(shoe_list, stock_list))

    # Identify and print the shoe with the highest stock
    selected_shoe = max(shoe_dict, key=shoe_dict.get)
    print(
        f'Highest stock is {selected_shoe.product}({selected_shoe.code}) in {selected_shoe.country}'
        f'with {max(stock_list)} units')


def write_shoe_data():
    """
    Rewrite database including any updated entries
    """
    try:
        with open('inventory.txt', 'w') as f:
            f.write('Country,Code,Product,Cost,Quantity')
            for item in shoe_list:
                output = f'{item.country},'\
                    f'{item.code},'\
                    f'{item.product},'\
                    f'{item.cost},'\
                    f'{item.quantity}\n'
                f.write(output)

    # Errors if database cannot be read
    except FileNotFoundError:
        print("Shoe database not found")
    except Exception as error:
        print(f"Other error: {error}")


# ==========Main Menu=============
"""
Create a menu that executes each function above.
This menu should be inside the while loop. Be creative!
"""
read_shoes_data()
user_choice = ''
while user_choice != 'q':
    print('**********  MENU  **********')

    user_choice = input("\nWhat would you like to do?\n"
                        "n\t-\tEnter new shoe\n"
                        "v\t-\tView all shoes\n"
                        "re\t-\tRe-stock shoe\n"
                        "s\t-\tSearch shoe\n"
                        "st\t-\tSee stock value\n"
                        "h\t-\tFind highest quantity shoe\n"
                        "q\t-\tquit\n"
                        "Enter: ").lower()

    if user_choice == "n":
        capture_shoes()
    elif user_choice == "v":
        view_all()
    elif user_choice == "re":
        re_stock()
    elif user_choice == "s":
        search_shoe()
    elif user_choice == "st":
        value_per_item()
    elif user_choice == "h":
        highest_qty()
    elif user_choice == 'q':
        write_shoe_data()
        print('Goodbye')
    else:
        print("Oops - incorrect input")
