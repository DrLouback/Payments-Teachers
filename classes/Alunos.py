from classes.Database import Database

class Alunos(Database):
    def __init__(self, db_file):
        super().__init__(db_file)
        self.nome_tabela = 'Alunos'
        self.__create_table__()


    def __create_table__(self):
        with Database(self.db_file) as cursor:
            cursor.execute(f'CREATE TABLE IF NOT EXISTS {self.nome_tabela} '
                           '('
                           'id INTEGER PRIMARY KEY AUTOINCREMENT,'
                           'name varchar(50),'
                           'contrato varchar (50));'
                        
                           )

    def create_user(self, nome, contrato):
        with Database(self.db_file) as cursor:
            cursor.execute(f'insert into {self.nome_tabela} (name, contrato) values (?,?)',(nome, contrato))
    
    def get_user(self, id):
        with Database(self.db_file) as cursor:
            cursor.execute(f'select * from {self.nome_tabela} where id = (?)',(id))
            return cursor.fetchone()

