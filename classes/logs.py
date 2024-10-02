from classes.Database import Database

class Logs(Database):
    def __init__(self, db_file):
        super().__init__(db_file)
        self.table_name = 'Logs'
        self.__create_table__()
    
    def __create_table__(self):
        with Database(self.db_file) as cursor:
            cursor.execute(f"""CREATE TABLE IF NOT EXISTS {self.table_name} (
                           id_log INTEGER PRIMARY KEY AUTOINCREMENT,
                           data ,
                           operation varchar(50),
                           usuario varchar (50),
                           app varchar(50)
                           );
                           """)
    def _insert_log(self, data, operation, usuario, app):
        with Database(self.db_file) as cursor:
            cursor.execute(f"Insert into {self.table_name} (data, operation, usuario, app) VALUES (?,?,?,?)",(data, operation, usuario, app))