from classes import Alunos
import streamlit as st
import pandas as pd
import sqlite3

conn = sqlite3.connect('db.sqlite3')
contratos = pd.read_sql('select * from Contratos',conn)
contratos_names = contratos['contrato']

st.title('Cadastro de Alunos')
name = st.text_input('Insira nome')
contrato = st.selectbox('Contrato', contratos_names)
ok = st.button('Ok')
if ok:
    alunos = Alunos.Alunos('db.sqlite3')
    alunos.create_user(name,contrato)

query = 'select * from Alunos'
df = pd.read_sql(query,conn)
st.dataframe(df, hide_index=True)





