import sqlite3

def connect():
    return sqlite3.connect('sqlite.db', check_same_thread=False)

def insert(cursor, table, columns, values):
    try:
        cursor.execute(f'INSERT INTO {table}({columns}) VALUES({values})')
        return True
    except Exception as e:
        print(f"An error occurred: {str(e)}")
        return False
    
def select(cursor, table):
    cursor.execute(f'SELECT * FROM {table}')
    return cursor.fetchall()

def select_where(cursor, table, condition):
    cursor.execute(f'SELECT * FROM {table} WHERE {condition}')
    return cursor.fetchall()

def update(cursor, table, columns, values, condition):
    cursor.execute(f'UPDATE {table} SET {columns} = {values} WHERE {condition}')
    return cursor.rowcount

def delete(cursor, table, condition):
    cursor.execute(f'DELETE FROM {table} WHERE {condition}')
    return cursor.rowcount


def create_supplier(name, address, city, zip_code, country):
    connector = connect()
    cursor = connector.cursor()

    columns = 'name, address, city, zip_code, country'
    values = f'"{name}", "{address}", "{city}", "{zip_code}", "{country}"'
    return insert(cursor, 'supplier', columns, values)

def get_supplier(id):
    connector = connect()
    cursor = connector.cursor()

    condition = f'id = {id}'
    return select_where(cursor, 'supplier', condition)

def get_supplieres(limit:int=None, condition=None):
    connector = connect()
    cursor = connector.cursor()

    if condition:
        query = f'SELECT * FROM supplier WHERE {condition}'
    else:
        query = 'SELECT * FROM supplier'

    if limit:
        query += f' LIMIT {limit}'

    cursor.execute(query)
    return cursor.fetchall()

def update_supplier(id, name, address, city, zip_code, country, contact_name, contact_phone, contact_email):
    connector = connect()
    cursor = connector.cursor()

    columns = f'name, address, city, zip_code, country, contact_name, contact_phone, contact_email'
    values = f'"{name}", "{address}", "{city}", "{zip_code}", "{country}", "{contact_name}", "{contact_phone}", "{contact_email}"'
    condition = f'id = {id}'
    return update(cursor, 'supplier', columns, values, condition)

def delete_supplier(id):
    connector = connect()
    cursor = connector.cursor()

    condition = f'id = {id}'
    return delete(cursor, 'supplier', condition)