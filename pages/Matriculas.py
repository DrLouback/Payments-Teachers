from classes.F_Relatorio import F_Relatorio
from classes.Reposicoes import Reposicoes
import streamlit as st
import pandas as pd
import sqlite3
import datetime as dt
import locale

locale.setlocale(locale.LC_TIME, 'pt_BR.UTF-8')
db = 'db.sqlite3'
conn = sqlite3.connect(db)

lista_professores = pd.read_sql('Select * from Professores',conn)

prof_selecionado = st.selectbox('Label',lista_professores['name'],label_visibility='hidden')
id_professor_view = lista_professores.loc[lista_professores['name']== prof_selecionado, 'id_professor'].values[0] #type: ignore

def filtro_mes():
    relatorio = pd.read_sql('Select data from F_Relatorio', conn)
    relatorio['data'] = pd.to_datetime(relatorio['data'] )
    relatorio['mes'] = relatorio['data'].dt.strftime('%B')
    relatorio['mes'] = [mes.capitalize() for mes in relatorio['mes']]
    return relatorio['mes']

mes = st.selectbox('Mês', filtro_mes().unique())


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
    
@st.dialog('Lançar Reposição')
def lançar_reposicao():
    conn = sqlite3.connect('db.sqlite3')
    with st.form('Reposição'):
        st.selectbox('Professor', prof_selecionado)
        query_aluno = f"""Select 
                a.name as Nome,
                a.id as ID
                from F_Relatorio f
                INNER JOIN Alunos a ON f.id_aluno = a.id
                WHERE id_professor = '{id_professor_view}' 
                ;"""
        alunos = pd.read_sql(query_aluno,conn)
        aluno_selecionado = st.selectbox('Aluno', alunos)
        id_aluno = alunos.loc[alunos['Nome']== aluno_selecionado, 'ID'].values[0]
        
        old_date = st.date_input('Dia desmarcado')
        new_professor = st.selectbox('Professor que repôs', lista_professores['name'])
        id_new_professor = lista_professores.loc[lista_professores['name'] == new_professor, 'id_professor'].values[0] #type: ignore
        new_date = st.date_input('Dia remarcado')
        
        submitted = st.form_submit_button("Submit")
        if submitted:
            reposicao = Reposicoes('db.sqlite3')
            reposicao.insert_reposicao(int(id_aluno),old_date,int(id_professor_view),new_date,int(id_new_professor),8)
    query_reposicoes = """Select a.name as Nome,
                          p.name as Professor_Original,
                          r.old_date as Data_Original,
                          p2.name as Professor_Marcado,
                          r.new_date as Data_Reposição,
                          valor as Valor
                          FROM Reposicoes r
                          INNER JOIN Alunos a ON r.id_aluno = a.id
                          INNER JOIN Professores p ON r.id_old_professor = p.id_professor
                          INNER JOIN Professores p2 on r.id_new_professor = p2.id_professor
                        
    """    
    reposicoes = pd.read_sql(query_reposicoes, conn)
    reposicoes['Data_Reposição'] = pd.to_datetime(reposicoes['Data_Reposição'])
    reposicoes['mes'] = reposicoes['Data_Reposição'].dt.strftime('%B')
    reposicoes['mes'] = [mes.capitalize() for mes in reposicoes['mes']]
    filtro_mes = reposicoes['mes'] == mes
    reposicoes = reposicoes[filtro_mes]
    reposicoes['Data_Reposição'] = reposicoes['Data_Reposição']
    st.dataframe(reposicoes, hide_index= True)


#configurando a F_Relatorio para mostrar os meses


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
    relatorio = pd.read_sql(query,conn)
    relatorio['mes'] = filtro_mes() 
    filtro = relatorio['mes'] == mes
    resultado = relatorio[filtro]
    st.dataframe(resultado, hide_index= True)

col1, col2 = st.columns([1,1])
with col1:
    if st.button('Matricular'):
        matricula = matricular()
        if matricula == True:
            st.rerun()
with col2:
    if st.button('Reposição'):
        reposicao = lançar_reposicao()

filtro_mes()
view_professor()

