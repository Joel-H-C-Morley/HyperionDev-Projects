# ========imports==========
from tabulate import tabulate
import sqlite3
import os.path


# ========The beginning of the class==========
class Book:
    """
    This is the book class. Within is initialisation and output a string of the book details
    """

    def __init__(self, book_id, title, author, quantity):
        """
        Initialises the object with country, code, product, cost, and quantity.
        """
        self.book_id = book_id
        self.title = title
        self.author = author
        self.quantity = quantity

    def __str__(self):
        """
        Return the string of the book details
        """
        return f'{self.book_id},{self.title},{self.author},{self.quantity}'


# ==========Functions outside the class==============
def create_dbase():
    """
    This function will create a file for the database and return the
    control of the database(cursor) and database object(db)
    """

    db = sqlite3.connect('bookstore_db')
    cursor = db.cursor()

    # Build empty table for database
    cursor.execute(
        '''
        CREATE TABLE 
            bookstore_db(
                id INTEGER PRIMARY KEY, 
                title TEXT,
                author TEXT, 
                qty INTEGER)
        ''')
    print('database created')
    # Save table
    db.commit()

    return db, cursor


def open_database():
    """
    This function will open the existing database, if there is no database it will call for one
    to be created. The function returns the control of the database(cursor) and database object(db).
    """

    # Statement to ensure the database file is either loaded or created
    path = './bookstore_db'
    check_file = os.path.isfile(path)
    if check_file:
        db = sqlite3.connect('bookstore_db')
        print('Opening database')
        cursor = db.cursor()  # Get a cursor object
    else:
        print('Creating database')
        db, cursor = create_dbase()

    return db, cursor


def get_last_id(cursor):
    """
    This function will find the most recent ID number created for the database. The database
    control object (cursor) is passed as an argument. The full information of the most recent
    book is returned
    """

    # Database is searched for the most recent (also the highest) ID number
    cursor.execute('''SELECT max(id) FROM bookstore_db''')
    last = cursor.fetchone()
    return last


def capture_book(book_id):
    """
    Function to allow a user to capture data about a book, use this data to create a book object.
    The ID for the new entry is passed as an argument and the book object is returned
    """

    # User enters the book information
    title = input('Enter book title: ')
    author = input('Enter book author: ')
    quantity = input('Enter quantity: ')
    # Book object created
    new_book = Book(book_id, title, author, quantity)
    return new_book


def add_book(book, cursor, db):
    """
    Enter the new book into the database. The book object, the database control(cursor) and object(db)
    are passed as arguments
    """

    # Insert data to database
    cursor.execute('''INSERT INTO bookstore_db(id, title, author, qty) VALUES(:id,:title,:author,:qty)''',
                    {'id': book.book_id, 'title': book.title, 'author': book.author, 'qty': book.quantity})
    # Save new database
    db.commit()


def view_all(cursor):
    """
    Print out the full database. The database controller(cursor) is passed as an argument
    """

    # Retrieve all records
    cursor.execute('''SELECT * FROM bookstore_db''')
    # Create list of information to use in the tabulate function
    book_table = []
    for record in cursor:
        book_table.append(list(record))
    print(tabulate(book_table, headers=["ID", "Title", "Author", "Quantity"]))


def re_stock(cursor, db):
    """
    Asks the user which book to update (by ID) and the new quantity. Updates the database accordingly.
    The function takes the database control object (cursor) and the database object (db) as arguments.
    """

    # Loop to ensure only numbers are entered by the user for ID and quantity
    while True:

        try:

            book_id = int(input("Enter ID of book to update: "))
            quantity = int(input("Enter new quantity: "))
            break

        except Exception as error:
            print(f'Error {error}. Input numbers only, try again')

    # Statement to catch error if no book is found using the ID number given by user
    try:

        # Update quantity in database
        cursor.execute('''UPDATE bookstore_db SET qty = ? WHERE id = ? ''', (quantity, book_id))
        db.commit()

        # Get info of updated book for confirmation statement
        cursor.execute('''SELECT * FROM bookstore_db WHERE id = ?''', (book_id,))
        book_del = cursor.fetchone()
        title_upd = book_del[1]
        quant_upd = book_del[3]
        print(f'The book \'{title_upd}\' quantity is now {quant_upd}!')

    except Exception as error:

        print(f'Error {error}. Book does not exist, check ID number')


def search_shoe(cursor):
    """
    Function to search for a book.
    This can take any entry and look for a partial match across all fields.
    The database control object (cursor) is passed as an argument
    """

    # Take search term from user
    search = input("Enter search term to partial match to either id, title or author: ")
    # Search database for any partially matching entry
    cursor.execute('''SELECT * FROM bookstore_db 
                    WHERE (id like ?) OR (author like ?) OR (title like ?)''',
                    ("%"+search+"%", "%"+search+"%", "%"+search+"%"))

    # Create list of results to use in tabulate function
    book_table = []
    for record in cursor:
        book_table.append(list(record))
    print(tabulate(book_table, headers=["ID", "Title", "Author", "Quantity"]))


def highest_qty(cursor):
    """
    Print out all the books in order of quantity
    The database control object (cursor) is passed as an argument
    """

    # Select all entries in database and order them by quantity
    cursor.execute('''SELECT * FROM bookstore_db 
                    ORDER BY qty DESC''')

    # Create list of the returned books to use in the tabulate function
    book_table = []
    for record in cursor:
        book_table.append(list(record))
    print(tabulate(book_table, headers=["ID", "Title", "Author", "Quantity"]))


def delete_book(cursor, db):
    """
    This function will remove a record from the database by ID number
    The function takes the database control object (cursor) and the database object (db) as arguments.
    """

    # Loop to ensure correct ID is entered by user
    while True:

        try:

            book_id = int(input("Enter ID of book to update: "))
            break

        except ValueError:
            print("Input numbers only, please try again")
        except Exception as error:
            print(f"Other error: {error}. Try again")

    # Statement catches an error if ID the user enters does not exist
    try:

        # Get chosen book details for confirmation statement
        cursor.execute('''SELECT * FROM bookstore_db 
                        WHERE id = ?''', (book_id,))
        book_del = cursor.fetchone()
        title_del = book_del[1]
        author_del = book_del[2]

        # Delete chosen book from database
        cursor.execute('''DELETE FROM bookstore_db WHERE id = ? ''', (book_id,))
        db.commit()
        print(f'Book {title_del} by {author_del}, deleted')

    except Exception as error:
        print(f'Error {error}. Book does not exist in database')


# ==========Main Menu=============
# Open the book database
dbase, dbcursor = open_database()

# Open user choice menu
user_choice = ''
while user_choice != 'q':
    print('**********  MENU  **********')

    user_choice = input("\nWhat would you like to do?\n"
                        "n\t-\tEnter new book\n"
                        "v\t-\tView all books\n"
                        "re\t-\tUpdate book quantity\n"
                        "s\t-\tSearch book\n"
                        "h\t-\tSort books by quantity\n"
                        "d\t-\tDelete book\n"
                        "q\t-\tquit\n"
                        "Enter: ").lower()

    if user_choice == "n":
        new_id = get_last_id(dbcursor)[0]
        try:
            book_object = capture_book(new_id+1)
        except TypeError:
            book_object = capture_book(3001)
        add_book(book_object, dbcursor, dbase)
    elif user_choice == "v":
        view_all(dbcursor)
    elif user_choice == "re":
        re_stock(dbcursor, dbase)
    elif user_choice == "s":
        search_shoe(dbcursor)
    elif user_choice == "h":
        highest_qty(dbcursor)
    elif user_choice == "d":
        delete_book(dbcursor, dbase)
    elif user_choice == 'q':
        print('Goodbye')
    else:
        print("Oops - incorrect input")
