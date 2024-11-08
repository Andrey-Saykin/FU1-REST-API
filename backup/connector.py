import sqlite3


connector = sqlite3.connect('sqlite.db')
cursor = connector.cursor()

def first_test():
    cursor.execute('INSERT INTO konto(name, kontostand) VALUES("Max Mustermann", 1000)')
    connector.commit()

def second_test():
    cursor.execute('SELECT * FROM konto')
    print(cursor.fetchall())

def close():
    cursor.close()
    connector.close()

def test_menu():
    user_input = None
    valid_options = ['1', '2', '3', '4']
    while not user_input in valid_options:
        print("\n1. Insert")
        print("2. Select")
        print("3. Delete")
        print("4. Exit")
        user_input = input("Enter a number: ")

    if user_input == '1':
        test_insert()
    elif user_input == '2':
        test_select()
    elif user_input == '3':
        test_delete()
    elif user_input == '4':
        close()
        exit()

def test_insert():
    name = input("Enter a name: ")
    balance = input("Enter a balance: ")
    try:
        balance = float(balance)
        cursor.execute(f'INSERT INTO konto(name, kontostand) VALUES("{name}", {balance})')
        connector.commit()
    except ValueError:
        print("Invalid balance. Please enter a valid decimal value.")
    except Exception as e:
        print(f"An error occurred: {str(e)}")
    
def test_select():
    cursor.execute('SELECT * FROM konto')
    print(cursor.fetchall())

def test_delete():
    try:
        id = int(input("Enter an id: "))
        cursor.execute(f'DELETE FROM konto WHERE id = {id}')
        if cursor.rowcount == 0:
            print("No record found with the given id.")
        else:
            connector.commit()
            print("Record deleted successfully.")
    except ValueError:
        print("Invalid id. Please enter a valid number.")
    except Exception as e:
        print(f"An error occurred: {str(e)}")

if __name__ == '__main__':
    while True:
        test_menu()