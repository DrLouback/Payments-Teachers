import sqlite3

class Database:
    def __init__(self, db_file):
        self.db_file = db_file

    def __enter__(self):
        self.conn = sqlite3.connect(self.db_file)
        self.cursor = self.conn.cursor()
        return self.cursor
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        if exc_type is None:
            self.conn.commit()
        else:
            self.conn.rollback()
        self.conn.close()

    def drop_table(self, table):
        with Database(self.db_file) as cursor:
            cursor.execute(f'DROP TABLE IF EXISTS {table}')

    def show_databases(self):
        self.cursor.execute("SELECT name FROM sqlite_master WHERE type='table'")
        return self.cursor.fetchall()
    def select_all(self,table_name):
        return self.cursor.execute(f'SELECT * FROM {table_name}')
        