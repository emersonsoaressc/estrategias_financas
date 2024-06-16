import streamlit as st
import pandas as pd
import numpy as np
from estrategia_financas import layout_page


#######################################
# CONSTRUÇÃO DA BARRA LATERAL COM LOGO
#######################################
def barraLateral():
    st.sidebar.image('image/logo_udesc60anos.png')
    st.sidebar.header('Curso de Ciências Econômicas')
    st.sidebar.subheader('Aluno: Emerson Soares')
    
    
    #######################################
    # ESCOLHA DO DEPARTAMENTO
    #######################################
    departamentos = ['Estratégia em Finanças']
    select_depto = st.sidebar.selectbox('Selecione o departamento:',departamentos)
    
    #######################################
    # SUB-TÓPICOS DE Estratégia em Finanças
    #######################################
    if select_depto == 'Estratégia em Finanças':
        st.write(layout_page())
