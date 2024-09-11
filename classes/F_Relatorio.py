from classes.Database import Database

class F_Relatorio(Database):
    def __init__(self,db_file):
        super().__init__(db_file)
        self.nome_tabela = 'F_Relatorio'

    def __create_table__(self):
        with Database(self.db_file) as cursor:
            cursor.execute(f'CREATE TABLE IF NOT EXISTS {self.nome_tabela} ('
                            'data DATE,'
                            'id_professor,'
                            'id_aluno,'
                            'id_contrato,'
                            'x_semana INTEGER NOT NULL,'
                            'percentual INTEGER NOT NULL,'
                            'valor INTEGER NOT NULL,'
                            'desconto float,'
                            'valor_devido float,'
                            'FOREIGN KEY (id_professor) REFERENCES Professores(id_professor),'
                            'FOREIGN KEY (id_aluno) REFERENCES Alunos(id),'
                            'FOREIGN KEY (id_contrato) REFERENCES Contratos(id_contrato);')
            
    def insert_datas(self, data,id_professor,id_aluno,id_contrato,x_semana,percentual,valor,desconto,valor_devido):
        self.cursor.execute(f'INSERT INTO {self.nome_tabela} VALUES (?,?,?,?,?,?,?,?)',(data,id_professor,id_aluno,id_contrato,x_semana,percentual,valor,desconto,valor_devido))