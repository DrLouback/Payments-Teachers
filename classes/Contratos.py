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
                           'contrato varchar(50) UNIQUE,'
                           'valor int,'
                           'x_semana int);'
                           )
    def create_contrato(self,contrato,valor,x_semana):
        with Database(self.db_file) as cursor:
            cursor.execute(f'INSERT INTO {self.nome_tabela} (contrato, valor, x_semana) VALUES (?,?,?)',(contrato,valor,x_semana))

    def get_contrato(self, id_contrato):
        with Database(self.db_file) as cursor:
            cursor.execute(f'Select * from {self.nome_tabela} where id_contrato =  (?) ', (id_contrato))
            return cursor.fetchone()
