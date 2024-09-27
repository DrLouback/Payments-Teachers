from classes.Professores import Professores
import streamlit as st
import pandas as pd
import sqlite3
from streamlit_extras.mandatory_date_range import date_range_picker
from datetime import datetime
import calendar

conn = sqlite3.connect('db.sqlite3')


st.title('Bem vindo ao sistema de pagamentos')
st.header('Escolha o Professor')

def datas() -> tuple: 
    today = datetime.today()
    month = today.month
    year = today.year
    range_month = calendar.monthrange(year, month)[1]
    last_day = datetime(year,month, range_month)
    start_day = datetime(year, month,1)
    resultado = st.date_input('Mês',(start_day, last_day))
    return resultado #type: ignore
    
inicio_mes, fim_mes = datas()

lista_professores = pd.read_sql('Select * from Professores',conn)

prof_selecionado = st.selectbox('Label',lista_professores['name'],label_visibility='hidden')
id_professor = lista_professores.loc[lista_professores['name']== prof_selecionado, 'id_professor'].values[0] #type: ignore

query = f"""Select f.data as Data,
            a.name as Nome,
            c.contrato as Contrato,
            f.x_semana as Aulas,
            f.percentual as '%',
            c.valor as Valor,
            FORMAT(f.desconto,1) as Desc,
            FORMAT(f.valor_devido,1) as Devido
            from F_Relatorio f
            INNER JOIN Alunos a ON f.id_aluno = a.id
            INNER JOIN Contratos c ON f.id_contrato = c.id_contrato
            WHERE f.id_professor = '{id_professor}' AND DATA BETWEEN '{inicio_mes}' AND '{fim_mes}';


"""
st.table(pd.read_sql(query,conn))

query_valor_devido = f"""SELECT SUM(valor_devido) as total FROM F_Relatorio
                        WHERE DATA BETWEEN '{inicio_mes}' AND '{fim_mes}';
                     """
total = pd.read_sql(query_valor_devido, conn).values[0]
for i in total:
    if i is not None:
        i = f'{i:,.2f}'
        st.subheader(f"Valor total: R${i.replace(',','.')}")