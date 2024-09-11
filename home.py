from classes.Professores import Professores
import streamlit as st
import pandas as pd
import sqlite3

conn = sqlite3.connect('db.sqlite3')

st.title('Bem vindo ao sistema ')
st.header('Escolha o Professor')
lista_professores = pd.read_sql('Select * from Professores',conn)

prof_selecionado = st.selectbox('',lista_professores['name'],label_visibility='hidden')




