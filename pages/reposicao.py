from classes.F_Relatorio import F_Relatorio
import streamlit as st
import pandas as pd
import sqlite3
from datetime import datetime
db = 'db.sqlite3'
conn = sqlite3.connect(db)

lista_professores = pd.read_sql('Select * from Professores',conn)

prof_selecionado = st.selectbox('Label',lista_professores['name'],label_visibility='hidden')
id_professor_view = lista_professores.loc[lista_professores['name']== prof_selecionado, 'id_professor'].values[0] #type: ignore


@st.dialog('Lançar Reposição')
def lançar_reposicao():
    st.selectbox('Professor', prof_selecionado)
    st.title('oi')

if st.button('matricular'):
    matricular = lançar_reposicao()