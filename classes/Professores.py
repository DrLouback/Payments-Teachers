from classes.Database import Database

class Professores(Database):
    def __init__(self,db_file):
        super().__init__(db_file)
        self.nome_tabela = 'Professores'
        self.__create__table__()

    def __create__table__(self):
        with Database(self.db_file) as cursor:
            cursor.execute(f'CREATE TABLE IF NOT EXISTS {self.nome_tabela} ('
                                'id_professor INTEGER PRIMARY KEY AUTOINCREMENT,'
                                'nome_professor varchar(30) NOT NULL);'
      
                           )
    def create_professor(self, nome):
        with Database(self.db_file) as cursor:
            cursor.execute(f'INSERT INTO {self.nome_tabela} values (?,?)', (None,nome))
            

if __name__ == '__main__':

    professores = Professores('db.sqlite3')
    print(professores)