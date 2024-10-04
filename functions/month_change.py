import streamlit as st
from datetime import datetime
import sqlite3
import pandas as pd
import calendar
from classes.logs import Logs

#Função para copiar a Tabela F_Relatorio do mês anterior para o mês atual.
def month_change(call = None):
    
    conn = sqlite3.connect('db.sqlite3') 
    today_datetime = datetime.today() #variável para configurar variáveis condicionais
    day_one = datetime(year=today_datetime.year, month= today_datetime.month, day= 1) 
    if call == 'Atualizar':
        now = day_one
    else:
        now = datetime.now().date()

    #Lista de datas na tabela de logs
    df_log = pd.read_sql('Select * from Logs', conn)
    log_days = df_log['data'].values
    

    if  now == day_one and  str(now) not in str(log_days):
        log_month_change = Logs('db.sqlite3')
        log_month_change._insert_log(now, 'month_change', 'system', 'configuracoes')
        
    
        last_month = today_datetime.month -1 if today_datetime.month >1 else 12
        ano = today_datetime.year if today_datetime.month > 1 else today_datetime.year - 1
        end_day_month = calendar.monthrange(year=ano,month=last_month)[1]
        start_last_month = datetime(year=ano, month= last_month, day=1).date()
        end_last_month = datetime(year=ano, month=last_month, day= end_day_month).date()
            
        conn = sqlite3.connect('db.sqlite3')
        

        cursor = conn.cursor()
        cursor.execute(f"""INSERT INTO F_Relatorio (data,id_professor,id_aluno,id_contrato,x_semana,percentual,valor,desconto,valor_devido)
                            SELECT '{datetime(today_datetime.year,month=today_datetime.month,day=today_datetime.day).strftime('%Y-%m-%d')}',id_professor,id_aluno,id_contrato,x_semana,percentual,valor,desconto,valor_devido
                            FROM F_Relatorio
                            WHERE data BETWEEN '{start_last_month}' AND '{end_last_month}';
                        """)
        conn.commit()
        
        query = f"""Select * from F_Relatorio where data between {start_last_month} AND
                        {end_last_month}"""
            
        dataframe = pd.read_sql(query,conn)
        st.dataframe(dataframe)
        st.success('Dados atualizados')
        st.rerun()
    if call != None and str(now) in str(log_days):
        st.error('Dados já foram atualizados')
            
