from classes.F_Relatorio import F_Relatorio
import streamlit as st
import pandas as pd
import sqlite3

db = 'db.sqlite3'
conn = sqlite3.connect(db)

df_professor = pd.read_sql('select * from Professores', conn)
professor_names = df_professor['name']

professor = st.selectbox('Nome do professor', professor_names)
filter_professor = df_professor.loc[df_professor['name'] == professor, 'id_professor'].values[0] #type: ignore

st.header(filter_professor)