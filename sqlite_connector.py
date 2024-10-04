import sqlite3
from contextlib import contextmanager

# Default Functions
@contextmanager
def get_db_connection():
    connector = sqlite3.connect('sqlite.db')
    cursor = connector.cursor()
    try:
        yield cursor
        connector.commit()
    except Exception as e:
        connector.rollback()
        print(f"Database error: {e}")
    finally:
        cursor.close()
        connector.close()

def execute_query(query, params=()):
    with get_db_connection() as cursor:
        cursor.execute(query, params)
        return cursor

def insert(table, columns, values):
    query = f'INSERT INTO {table} ({columns}) VALUES ({", ".join(["?" for _ in values])})'
    cursor = execute_query(query, values)
    return cursor.rowcount

def select(table, columns='*', condition=None, params=()):
    query = f'SELECT {columns} FROM {table}'
    if condition:
        query += f' WHERE {condition}'
    with get_db_connection() as cursor:
        cursor.execute(query, params)
        return cursor.fetchall()

def update(table, columns, values, condition, condition_params=()):
    set_clause = ', '.join([f"{col} = ?" for col in columns])
    query = f'UPDATE {table} SET {set_clause} WHERE {condition}'
    params = values + condition_params
    cursor = execute_query(query, params)
    return cursor.rowcount

def delete(table, condition, params=()):
    query = f'DELETE FROM {table} WHERE {condition}'
    cursor = execute_query(query, params)
    return cursor.rowcount

# Custom Functions
def create_supplier(name, address, city, zip_code, country, contact_name, contact_phone, contact_email):
    columns = 'name, address, city, zip_code, country, contact_name, contact_phone, contact_email'
    values = (name, address, city, zip_code, country, contact_name, contact_phone, contact_email)
    return insert('supplier', columns, values)

def get_supplier(id):
    condition = 'id = ?'
    return select('supplier', condition=condition, params=(id,))

def get_supplieres(limit=None, condition=None, params=()):
    query = 'SELECT * FROM supplier'
    if condition:
        query += f' WHERE {condition}'
    if limit:
        query += f' LIMIT {limit}'
    with get_db_connection() as cursor:
        cursor.execute(query, params)
        return cursor.fetchall()

def update_supplier(id, columns, values):
    condition = f'id = {id}'
    return update('supplier', columns, values, condition)

def delete_supplier(id):
    condition = 'id = ?'
    return delete('supplier', condition, (id,))