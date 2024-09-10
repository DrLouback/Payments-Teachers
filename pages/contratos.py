from classes import Database, Contratos, Alunos
import streamlit as st
import pandas as pd
import sqlite3

db = 'db.sqlite3'
conn = sqlite3.connect('db.sqlite3')

st.title('Cadastro de Contratos')

contrato = st.text_input('Nome contrato')
valor = st.number_input('Valor contrato')
x_semana = st.number_input('Vezes na semana')
ok_c = st.button('Ok',key='contrato')

if ok_c:
    contratos = Contratos.Contratos(db)
    contratos.create_contrato(contrato,valor,x_semana)
    

query = 'select * from Contratos'
df_c = pd.read_sql(query,conn)
name_contrato = df_c['contrato']

st.dataframe(df_c, hide_index= True)



