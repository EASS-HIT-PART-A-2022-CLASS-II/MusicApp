import mysql.connector


def create_connection():
    try:
        conn = mysql.connector.connect(
            user='root', password='root', host='database', port=3306, database='db')
        return conn
    except mysql.connector.Error as e:
        print(f'Error: {e}')
        return None


def execute_read_query(query):
    conn = create_connection()
    if conn:
        try:
            try:
                cursor = conn.cursor()
            except mysql.connector.Error as e:
                print(f'Error creating cursor: {e}')
                return None
            cursor.execute(query)
            result = cursor.fetchall()
            return result
        except mysql.connector.Error as e:
            print(f'Error executing query: {e}')
        finally:
            close_connection(conn)
    else:
        print('Error: Connection not established')

def close_connection(conn):
    conn.close()


query = f"SELECT * FROM tracks"
result = execute_read_query(query)
if result:
    print(result)
