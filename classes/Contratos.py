from classes.Database import Database

class Contratos(Database):
    def __init__(self, db_file):
        super().__init__(db_file)
        self.nome_tabela = 'Contratos'
        self.__create_table__()

    def __create_table__(self):
        with Database(self.db_file) as cursor:
            cursor.execute(f'CREATE TABLE IF NOT EXISTS {self.nome_tabela} ('
                           'id_contrato INTEGER PRIMARY KEY AUTOINCREMENT,'
                           'contrato varchar(50) UNIQUE NOT NULL,'
                           'valor int NOT NULL,'
                           'x_semana int NOT NULL);'
                           )
    def create_contrato(self,contrato,valor,x_semana):
        with Database(self.db_file) as cursor:
            cursor.execute(f'INSERT INTO {self.nome_tabela} (contrato, valor, x_semana) VALUES (?,?,?)',(contrato,valor,x_semana))

    def get_contrato(self, id_contrato):
        with Database(self.db_file) as cursor:
            cursor.execute(f'Select * from {self.nome_tabela} where id_contrato =  (?) ', (id_contrato))
            return cursor.fetchone()
    
    def delete_contrato(self, id_contrato):
        with Database(self.db_file) as cursor:
            cursor.execute(f'DROP * FROM {self.nome_tabela} where id_contrato = (?)', (id_contrato))
    
    def update_contrato(self, id_contrato, contrato, valor, x_semana):
        with Database(self.db_file) as cursor:
            cursor.execute("""  Update Contratos (contrato, valor, x_semana)
                                SET contrato = ?, valor = ?, x_semana = ?
                                WHERE id_contrato = ?;
                                
                           """)