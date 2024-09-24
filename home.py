from classes.Professores import Professores
import streamlit as st
import pandas as pd
import sqlite3

conn = sqlite3.connect('db.sqlite3')

st.title('Bem vindo ao sistema de pagamentos')
st.header('Escolha o Professor')
lista_professores = pd.read_sql('Select * from Professores',conn)

prof_selecionado = st.selectbox('Label',lista_professores['name'],label_visibility='hidden')
id_professor = lista_professores.loc[lista_professores['name']== prof_selecionado, 'id_professor'].values[0] #type: ignore

query = f"""Select f.data as Data,
            a.name as Nome,
            c.contrato as Contrato,
            c.x_semana as Aulas,
            f.percentual as '%',
            c.valor as Valor,
            f.desconto as Desc,
            f.valor_devido as Devido
            from F_Relatorio f
            INNER JOIN Alunos a ON f.id_aluno = a.id
            INNER JOIN Contratos c ON f.id_contrato = c.id_contrato
            WHERE f.id_professor = '{id_professor}';


"""
st.table(pd.read_sql(query,conn))