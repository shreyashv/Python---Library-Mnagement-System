import pandas as pd
import datetime as dt
source_file_path = r'C:\Users\Pravin\Python Project\BookCount.csv'
borrowing_logs_path = r'C:\Users\Pravin\Python Project\borrowing_logs.csv'
source_file = pd.read_csv(source_file_path)


def borrowbook(source_file,results):
    print("Enter the book number you want to borrow:")
    booknumber = input()
    try:
        booknumber = int(booknumber)
    except ValueError:
        booknumber = "fail"
    if(source_file.where(source_file['Book_number'] == booknumber).dropna().empty == False):
        print("Enter borrower's name:")
        filter = (source_file['Book_number'] == booknumber)
        filtered_results = source_file.where(filter).dropna()
        borrower_name = str(input())
        data = {'Book_number':  [int(filtered_results.iloc[0]['Book_number'])],
        'Book_Name': [filtered_results.iloc[0]['Book_Name']],
        'Author_Name':  [filtered_results.iloc[0]['Author_Name']],
        'Publisher_Name':  [filtered_results.iloc[0]['Publisher_Name']],
        'Borrower_Name':  [borrower_name],
        'Borrow_Date':  [dt.date.today()],
        'Due_Date': [dt.date.today() + dt.timedelta(days=7)],
        'Difference':  [7],
        'Fine':  [0]
        }
        borrowing_logs = pd.DataFrame(data)
        print(borrowing_logs)
        borrowing_logs.to_csv(borrowing_logs_path, index = False, header = False, mode = 'a')
        source_file.at[booknumber - 1,'Number_of_Books'] = source_file.at[booknumber - 1,'Number_of_Books'] - 1
        print("Book Selected - (" + source_file.at[booknumber - 1,'Book_Name'] + ") by " + source_file.at[booknumber - 1,'Publisher_Name'] + " is successfully borrowed")
        source_file.to_csv(source_file_path, index = False)
    else:
        print("PLease enter correct book number")
        borrowbook(source_file,results)


def checkEmpty(results):
    if(results.empty == True):
        print("No Results Found")
    else:
        print(results)
        borrowbook(source_file,results)

def search_book_func(source_file,search_book_name):
    Books = source_file['Book_Name'].str.upper()
    results = source_file[Books.str.match(search_book_name)]
    checkEmpty(results)

def search_author_func(source_file,search_author_name):
    Authors = source_file['Author_Name'].str.upper()
    results = source_file[Authors.str.match(search_author_name)]
    checkEmpty(results)

def search_publisher_func(source_file,search_publisher_name):
    Books = source_file['Publisher_Name'].str.upper()
    results = source_file[Books.str.match(search_publisher_name)]
    checkEmpty(results)
    

def search_again_func():
    print("Do you want to search again? Press 1\nPress 2 to go to the main menu\npress any other number to quit")
    search_again = input()
    try:
        search_again = int(search_again)
    except ValueError:
        search_again = "fail"
    if(search_again == 1):
        search_func()
    elif(search_again == 2):
        main_func()
    elif(search_again == "fail"):
        print("wrong input")
        search_again_func()
    else:
        quit()


def search_func():
    print("Select search crietria:\n1 for by Author Name\n2 for Publisher Name\n3 for Book Name\n4 to display all books")
    criteria = input()
    try:
        criteria = int(criteria)
    except ValueError:
        criteria = "fail"
        
    if(criteria == 1):
        print("Enter the Author Name:")
        author_name = str(input()).upper()
        search_author_func(source_file,author_name)
        search_again_func()

    elif(criteria == 2):
        print("Enter the Publisher Name:")
        publisher_name = str(input()).upper()
        search_publisher_func(source_file,publisher_name)
        search_again_func()

    elif(criteria == 3):
        print("Enter the Book Name:")
        book_name = str(input()).upper()
        search_book_func(source_file,book_name)
        search_again_func()

    elif(criteria == 4):
        print(source_file)
        borrowbook(source_file,source_file)
        search_again_func()
        
    else:
        print("Could not recognize input")
        search_again_func()

def log_activity_again():
    print("Do you want to filter again? Press 1\nPress 2 to go to the main menu\npress any other number to quit")
    search_again = input()
    try:
        search_again = int(search_again)
    except ValueError:
        search_again = "fail"
    if(search_again == 1):
        check_log_activity()
    elif(search_again == 2):
        main_func()
    elif(search_again == "fail"):
        print("wrong input")
        log_activity_again()
    else:
        quit()

def filter_by_name(borrowing_logs):
    print("Enter the borrower's name:")
    borrower = str(input()).upper()
    Borrower_Name = borrowing_logs['Borrower_Name'].str.upper()
    results = borrowing_logs[Borrower_Name.str.match(borrower)]
    if(results.empty == False):
        print(results)
        log_activity_again()
    else:
        print("Did not find the name entered, Please enter again")
        filter_by_name()


def filter_by_due_date(borrowing_logs):
    borrowing_logs['Due_Date'] = borrowing_logs['Due_Date'].astype(str)
    results = borrowing_logs.where(borrowing_logs['Due_Date'] == str(dt.date.today())).dropna()
    if(results.empty == False):
        print(results)
        log_activity_again()
    else:
        print("No records found")
        log_activity_again()

def update_logs(borrowing_logs):
    borrowing_logs['Difference'] = pd.to_datetime( borrowing_logs['Due_Date']) - pd.Timestamp.now().normalize()
    borrowing_logs['Difference'] = borrowing_logs['Difference'].astype(str).str.replace(" days","")
    borrowing_logs['Fine'] = pd.to_numeric(borrowing_logs['Difference']) * int(20)
    borrowing_logs['Fine'] = pd.to_numeric(borrowing_logs['Fine'])
    borrowing_logs.loc[(borrowing_logs.Fine > 0), 'Fine'] = 0
    borrowing_logs.to_csv(borrowing_logs_path, index = False)
    print(borrowing_logs)
    print("All Differences are updated in borrowing logs file")
    log_activity_again()

def check_log_activity():
    borrowing_logs = pd.read_csv(borrowing_logs_path)
    print(borrowing_logs)
    print("Enter 1 for filter by name\nEnter 2 for filter by today's due_date\nEnter 3 to update fine in borrowing logs")
    filter_logs = input()
    try:
        filter_logs = int(filter_logs)
    except ValueError:
            filter_logs = "fail"
    if(filter_logs == 1):
        filter_by_name(borrowing_logs)
    elif(filter_logs == 2):
        filter_by_due_date(borrowing_logs)
    elif(filter_logs == 3):
        update_logs(borrowing_logs)
    else:
        print("Wrong input")
        check_log_activity()


def main_func():
    print("Enter 1 for search and 2 for log activity:")
    activity = input()
    try:
        activity = int(activity)
    except ValueError:
            activity = "fail"
    if(activity == 1):
        search_func()
    elif(activity == 2):
        check_log_activity()
    else:
        print("could not understand the input, please enter again")
        main_func()


print(source_file)
main_func()