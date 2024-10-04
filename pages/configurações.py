import streamlit as st
from functions.month_change import month_change

st.header('Configurações do sistema')
st.subheader('Atualização automática do mês')

st.markdown('Deseja forçar atualização?')
atualizar = st.button('Sim', help= """Irá replicar os dados do último mês
          para o mês atual""")


if atualizar:
    month_change('Atualizar')

