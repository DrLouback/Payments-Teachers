from classes.F_Relatorio import F_Relatorio
import streamlit as st
import pandas as pd
import sqlite3
from datetime import datetime
db = 'db.sqlite3'
conn = sqlite3.connect(db)


#Dataframes tabela professores
df_professor = pd.read_sql('Select id_professor, name from professores', conn)  
st.header('Professor')
professor = st.selectbox('Professores', df_professor['name'], label_visibility='collapsed')
id_professor = df_professor.loc[df_professor['name'] == professor, 'id_professor'].values[0] #type: ignore

print(id_professor)

#Dataframes tabelas alunos
alunos = pd.read_sql('SELECT * FROM Alunos',conn)
alunos_name = alunos['name']

#Dataframes tabelas contratos
df_contratos = pd.read_sql('Select * from Contratos', conn)
contratos_nomes = df_contratos['contrato']


#Informações do aluno
data = st.date_input('Data de matrícula')
st.subheader('Nome do aluno')
aluno = st.selectbox('Aluno', alunos_name, label_visibility= 'collapsed')
id_aluno = alunos.loc[alunos['name'] == aluno, 'id'].values[0] #type: ignore
contrato_aluno = alunos.loc[alunos['id'] == id_aluno, 'contrato'].values[0] #type: ignore

#Informações do contrato
id_contrato = df_contratos.loc[df_contratos['contrato'] == contrato_aluno, 'id_contrato'].values[0] #type: ignore
valor = df_contratos.loc[df_contratos['id_contrato'] == id_contrato, 'valor'].values[0] #type: ignore
col1, col2 = st.columns(2)
st.divider()
with col1:
    st.subheader(contrato_aluno)
    x_semana = df_contratos.loc[df_contratos['id_contrato'] == id_contrato, 'x_semana'].values[0] #type: ignore
    qtd_semana = st.selectbox('Quantidade de aulas por semana', range(1,x_semana+1))
with col2:
    st.subheader(f'R${valor:.2f}')
    percentual = st.selectbox('Percentual', [35,60,70,100], format_func= lambda x: f'{x}%')
    
valor_desconto = st.number_input('Desconto no contrato', min_value= 0, step =10)

valor_devido = ((valor-valor_desconto)/x_semana)*qtd_semana * percentual/100
st.subheader(f'Valor devido R${valor_devido:.2f}')

if st.button('Matricular'):
    professor = F_Relatorio(db)
    professor.insert_datas(data, int(id_professor),  int(id_aluno) ,int(id_contrato), qtd_semana, percentual, int(valor), float(valor_desconto), float(valor_devido))
#df_frelatorio = pd.read_sql(f'Select * from F_Relatorio where id_professor = {id_professor}', conn)

st.markdown(f'{data, id_professor,  id_aluno ,id_contrato, qtd_semana, percentual, valor, valor_devido, valor_desconto}')

query = f"""Select f.data,
            a.name as Nome,
            c.contrato as Contrato,
            c.x_semana as Vezes_semana,
            f.percentual as Percentual,
            c.valor as Valor,
            f.desconto as Desconto,
            f.valor_devido as Valor_Devido
            from F_Relatorio f
            INNER JOIN Alunos a ON f.id_aluno = a.id
            INNER JOIN Contratos c ON f.id_contrato = c.id_contrato
            WHERE f.id_professor = '{id_professor}';


"""
st.dataframe(pd.read_sql(query,conn))