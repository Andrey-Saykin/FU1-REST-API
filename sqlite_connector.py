import sqlite3

# Default Functions
def connect():
    return sqlite3.connect('sqlite.db')

def insert(cursor, table, columns, values):
    try:
        query = f'INSERT INTO {table}({columns}) VALUES({values})'
        print(query)
        cursor.execute(query)
        return cursor.lastrowid
    except Exception as e:
        print(f"An error occurred: {str(e)}")
        return False
    
def select(cursor, table):
    cursor.execute(f'SELECT * FROM {table}')
    return cursor.fetchall()

def select_where(cursor, table, condition):
    query = f'SELECT * FROM {table} WHERE {condition}'
    print(query)
    cursor.execute(query)
    return cursor.fetchall()

def update(cursor, table, columns, values, condition):
    query = f'UPDATE {table} SET {columns} WHERE {condition}'
    print(query)
    cursor.execute(query, values)
    return cursor.rowcount

def delete(cursor, table, condition):
    cursor.execute(f'DELETE FROM {table} WHERE {condition}')
    return cursor.rowcount

# Custom Functions
def create_supplier(name, address, city, zip_code, country, contact_name, contact_phone, contact_email):
    connector = connect()
    cursor = connector.cursor()

    columns = f'name, address, city, zip_code, country, contact_name, contact_phone, contact_email'
    values = f'"{name}", "{address}", "{city}", "{zip_code}", "{country}", "{contact_name}", "{contact_phone}", "{contact_email}"'
    success = insert(cursor, 'supplier', columns, values)
    if success:
        connector.commit()
    return success

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

def update_supplier(id, columns, values):
    connector = connect()
    cursor = connector.cursor()

    condition = f'id = {id}'
    changes = update(cursor, 'supplier', columns, values, condition)
    if changes:
        connector.commit()
    return changes

def delete_supplier(id):
    connector = connect()
    cursor = connector.cursor()

    condition = f'id = {id}'
    deleted = delete(cursor, 'supplier', condition)
    if deleted:
        connector.commit()
    return deleted