import sqlite3
from sqlite3 import Error

file_path = "database.DB"

def create_database(db_file):
    """
    create a database connection to a SQLite database
    generate the database
    close the connection
    """
    conn = None
    cur = None
    try:
        conn = sqlite3.connect(db_file)
        print(sqlite3.version)
        cur = conn.cursor()
        create_table = "CREATE TABLE [IF NOT EXISTS] [main].Transactions (" \
                       "transaction_id INTEGER PRIMARY KEY" \
                       "year INTEGER NOT NULL," \
                       "month TEXT NOT NULL," \
                       "day INTEGER NOT NULL," \
                       "transaction_num INTEGER NOT NULL," \
                       "transaction_description TEXT NOT NULL)"
        cur.execute(create_table)


    except Error as e:
        print(e)
    finally:
        cur.close()
        conn.close()

if __name__ == '__main__':
    create_database(db_file=file_path)
