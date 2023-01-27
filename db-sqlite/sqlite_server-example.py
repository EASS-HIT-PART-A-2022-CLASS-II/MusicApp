import sqlite3

def create_connection():
    conn = sqlite3.connect('sqlite:////db/musicapp.db')
    return conn

def close_connection(conn):
    conn.close()

def execute_query(query):
    conn = create_connection()
    cursor = conn.cursor()
    cursor.execute(query)
    conn.commit()
    close_connection(conn)

def execute_read_query(query):
    conn = create_connection()
    cursor = conn.cursor()
    result = cursor.execute(query).fetchall()
    close_connection(conn)
    return result
