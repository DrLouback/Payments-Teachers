from classes.Professores import Professores
import streamlit as st
import pandas
import sqlite3

db_file = 'db.sqlite3'
conn = sqlite3.connect(db_file)


st.title('Professores')

nome = st.text_input('Nome do Professor')
ok = st.button('Ok')

if ok:
    professor = Professores(db_file)
    professor.create_professor(nome)

query = 'Select * from Professores'
df = pandas.read_sql(query, conn)
st.dataframe(df, hide_index=True)