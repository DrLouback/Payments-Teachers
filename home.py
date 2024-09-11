from classes.Professores import Professores
import streamlit as st
import pandas as pd
import sqlite3

st.title('Bem vindo ao sistema ')

professores = Professores('db.sqlite3')
print(professores)