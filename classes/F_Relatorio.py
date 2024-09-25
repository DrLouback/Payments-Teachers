from classes.Database import Database

class F_Relatorio(Database):
    def __init__(self,db_file):
        super().__init__(db_file)
        self.nome_tabela = 'F_Relatorio'
        self.__create_table__()

    def __create_table__(self):
        with Database(self.db_file) as cursor:
            cursor.execute(f'CREATE TABLE IF NOT EXISTS {self.nome_tabela} ('
                            'data ,'
                            'id_professor INTEGER,'
                            'id_aluno INTEGER ,'
                            'id_contrato INTEGER,'
                            'x_semana INTEGER NOT NULL,'
                            'percentual INTEGER NOT NULL,'
                            'valor INTEGER NOT NULL,'
                            'desconto float,'
                            'valor_devido float,'
                            'FOREIGN KEY (id_professor) REFERENCES Professores(id_professor),'
                            'FOREIGN KEY (id_aluno) REFERENCES Alunos(id),'
                            'FOREIGN KEY (id_contrato) REFERENCES Contratos(id_contrato))')
            
    def insert_datas(self, data,id_professor,id_aluno,id_contrato,x_semana,percentual,valor,desconto,valor_devido):
        with Database(self.db_file) as cursor:
            cursor.execute(f'INSERT INTO {self.nome_tabela} VALUES (?,?,?,?,?,?,?,?,?)',(data,id_professor,id_aluno,id_contrato,x_semana,percentual,valor,desconto,valor_devido))

if __name__ == '__main__':
    report = F_Relatorio('db.sqlite3')
    report.insert_datas((2024, 9, 17), 3, 1, 1, 2, 60, 425, 255.0, 0)