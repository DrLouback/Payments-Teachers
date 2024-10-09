from classes.Database import Database

#Criar o banco para reposições realizadas 

class Reposicoes(Database):
    def __init__(self, db_file):
        super().__init__(db_file)
        self.nome_tabela = 'Reposicoes'
        self.__create_table__()

    def __create_table__(self):
        with Database(self.db_file) as cursor:
            cursor.execute(f""" CREATE TABLE IF NOT EXISTS {self.nome_tabela} (
                                id_reposicao INTEGER PRIMARY KEY AUTOINCREMENT,
                                id_aluno INTEGER,
                                old_date DATE,
                                id_old_professor,
                                new_date DATE,
                                id_new_professor INTEGER,
                                valor INTEGER,
                                FOREIGN KEY (id_aluno) REFERENCES Aluno(id),
                                FOREIGN KEY (id_old_professor) REFERENCES Professores(id_professor),
                                FOREIGN KEY (id_new_professor) REFERENCES Professores(id_professor)
                
                           
                           );
                           
                           """)
    def insert_reposicao(self, id_aluno,old_date,id_old_professor, new_date, id_new_professor, valor):
        with Database(self.db_file) as cursor:
            cursor.execute(f"""INSERT INTO {self.nome_tabela} (id_reposicao,id_aluno, old_date, id_old_professor, new_date, id_new_professor, valor) 
                                   VALUES (?,?,?,?,?,?,?) """, (None,id_aluno,old_date,id_old_professor,new_date,id_new_professor,valor))
                