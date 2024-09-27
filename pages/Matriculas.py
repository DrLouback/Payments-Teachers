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


@st.dialog('Cadastrar Aluno')
def matricular():

    db = 'db.sqlite3'
    conn = sqlite3.connect(db)
    #Dataframes tabela professores
    df_professor = pd.read_sql('Select id_professor, name from professores', conn)  
    st.header('Professor')
    professor = st.selectbox('Professores', df_professor['name'], label_visibility='collapsed', index= int(id_professor_view-1))
    id_professor = df_professor.loc[df_professor['name'] == professor, 'id_professor'].values[0] #type: ignore

    

    #Dataframes tabelas alunos
    alunos = pd.read_sql('SELECT * FROM Alunos',conn)
    alunos_name = alunos['name']

    #Dataframes tabelas contratos
    df_contratos = pd.read_sql('Select * from Contratos', conn)
    contratos_nomes = df_contratos['contrato']


    #Informações do aluno
    data = st.date_input('Data de matrícula')
    st.subheader('Nome do aluno')
    aluno = st.selectbox('Aluno', alunos_name, label_visibility= 'collapsed')
    id_aluno = alunos.loc[alunos['name'] == aluno, 'id'].values[0] #type: ignore
    contrato_aluno = alunos.loc[alunos['id'] == id_aluno, 'contrato'].values[0] #type: ignore

    #Informações do contrato
    id_contrato = df_contratos.loc[df_contratos['contrato'] == contrato_aluno, 'id_contrato'].values[0] #type: ignore
    valor = df_contratos.loc[df_contratos['id_contrato'] == id_contrato, 'valor'].values[0] #type: ignore
    col1, col2 = st.columns(2)
    st.divider()
    with col1:
        st.subheader(contrato_aluno)
        x_semana = df_contratos.loc[df_contratos['id_contrato'] == id_contrato, 'x_semana'].values[0] #type: ignore
        qtd_semana = st.selectbox('Quantidade de aulas por semana', range(1,x_semana+1))
        
    with col2:
        st.subheader(f'R${valor:.2f}')
        percentual = st.selectbox('Percentual', [35,60,70,100], format_func= lambda x: f'{x}%')
        
    valor_desconto = st.number_input('Desconto no contrato', min_value= 0, step =10)

    valor_devido = ((valor-valor_desconto)/x_semana)*qtd_semana * percentual/100
    st.subheader(f'Valor devido R${valor_devido:.2f}')

    if st.button('Matricular Aluno'):
        professor = F_Relatorio(db)
        professor.insert_datas(data=data, id_professor= int(id_professor), id_aluno= int(id_aluno) ,id_contrato= int(id_contrato), x_semana= qtd_semana, percentual= percentual, valor= int(valor), desconto=  float(valor_desconto), valor_devido= float(valor_devido))
        st.rerun()
        return True
    

def view_professor():        
    query = f"""Select f.data,
                    a.name as Nome,
                    c.contrato as Contrato,
                    f.x_semana as Aulas,
                    f.percentual as Percentual,
                    c.valor as Valor,
                    f.desconto as Desconto,
                    f.valor_devido as Valor_Devido
                    from F_Relatorio f
                    INNER JOIN Alunos a ON f.id_aluno = a.id
                    INNER JOIN Contratos c ON f.id_contrato = c.id_contrato
                    WHERE f.id_professor = '{id_professor_view}';


        """
    st.dataframe(pd.read_sql(query,conn), hide_index= True)


if st.button('Matricular'):
    matricula = matricular()
    if matricula == True:
        st.rerun()

view_professor()

    