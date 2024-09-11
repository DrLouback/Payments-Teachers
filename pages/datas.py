from classes.F_Relatorio import F_Relatorio
import streamlit as st
import pandas as pd
import sqlite3

db = 'db.sqlite3'
conn = sqlite3.connect(db)
professor = F_Relatorio(db)


def selecionar_valor(tabela_pandas, coluna_exibição, coluna_buscada):
    dataframe = pd.read_sql(f'SELECT * FROM {tabela_pandas}', conn)
    dado_escolhido = st.selectbox('Escolha', dataframe[coluna_exibição])
    dado_buscado = dataframe.loc[dataframe[coluna_exibição] == dado_escolhido, coluna_buscada].values[0] #type: ignore
    return dado_buscado
col1,col2,col3 = st.columns(3)
with col1:
    id_professor = selecionar_valor('Professores','name','id_professor')
with col2:
    id_aluno = selecionar_valor('Alunos','name','id')
with col3:
    id_contrato = selecionar_valor('Contratos','contrato','id_contrato')

def pegar_valor(tabela_pandas, coluna_ref, coluna_buscada):
    dataframe = pd.read_sql(f'Select * from {tabela_pandas} ',conn)
    resultado = dataframe.loc[dataframe[coluna_ref] == coluna_ref, coluna_buscada ].values[0] #type: ignore
    return resultado
with col1:
    data = st.date_input('data')
if id_contrato:
    #x_semana = pegar_valor('Contratos',id_contrato,'x_semana')
    percentual = '35'
    #valor = pegar_valor('Contratos',id_contrato,'valor')
    desconto = 0
    #valor_devido = valor 
#pandas_teste = st.dataframe([selecionar_id('Professores','name','id_professor'),selecionar_id('Alunos','name','id')])

    frame_teste = pd.DataFrame(columns=['id_professor','id_aluno','id_contrato','x_semana','%','valor','desconto','valor_devido'])

    professor.insert_datas(data, id_professor, id_aluno, id_contrato, x_semana, percentual, valor, desconto, valor_devido)
