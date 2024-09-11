from classes.Professores import Professores
import streamlit as st
import pandas as pd
import sqlite3

conn = sqlite3.connect('db.sqlite3')

st.title('Bem vindo ao sistema ')
st.header('Escolha o Professor')
lista_professores = pd.read_sql('Select * from Professores',conn)

prof_selecionado = st.selectbox('Label',lista_professores['name'],label_visibility='hidden')
id_prof = lista_professores.loc[lista_professores['name']== prof_selecionado, 'id_professor'].values[0] #type: ignore

query = f"Select * from Professores where id_professor = '{id_prof}'"
df_selecionado = pd.read_sql(query,conn)
st.dataframe(df_selecionado)
