import streamlit as st
from datetime import datetime
import sqlite3
import pandas as pd
import calendar
from classes.F_Relatorio import F_Relatorio

st.header('Configurações do sistema')
st.subheader('Atualização automática do mês')

st.markdown('Deseja forçar atualização?')
atualizar = st.button('Sim', help= """Irá replicar os dados do último mês
          para o mês atual""")

def month_change():
    conn = sqlite3.connect('db.sqlite3')
    today = datetime.today()
    day_one = datetime(year=today.year, month= today.month, day= 1)
    teste_day= datetime(today.year, month= today.month, day=1)

    if teste_day == day_one:

        last_month = today.month -1 if today.month >1 else 12
        ano = today.year if today.month > 1 else today.year - 1
        end_day_month = calendar.monthrange(year=ano,month=last_month)[1]
        start_last_month = datetime(year=ano, month= last_month, day=1).date()
        end_last_month = datetime(year=ano, month=last_month, day= end_day_month).date()
        
        conn = sqlite3.connect('db.sqlite3')
        

        cursor = conn.cursor()
        cursor.execute(f"""INSERT INTO F_Relatorio (data,id_professor,id_aluno,id_contrato,x_semana,percentual,valor,desconto,valor_devido)
                          SELECT '{datetime(today.year,month=today.month,day=today.day).strftime('%Y-%m-%d')}',id_professor,id_aluno,id_contrato,x_semana,percentual,valor,desconto,valor_devido
                          FROM F_Relatorio
                          WHERE data BETWEEN '{start_last_month}' AND '{end_last_month}';
                       """)
        conn.commit()
        
        query = f"""Select * from F_Relatorio where data between {start_last_month} AND
                    {end_last_month}"""
        
        dataframe = pd.read_sql(query,conn)
        st.dataframe(dataframe)
        

    else:
        st.markdown('Hoje não é dia 1')

if atualizar:
    month_change()

