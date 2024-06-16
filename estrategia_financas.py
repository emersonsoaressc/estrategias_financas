import streamlit as st
import pandas as pd
import numpy as np
from functions import baixar_base_dados_yfinance, baixar_selic
import datetime


def layout_page():
    st.title('TRABALHO DE FORMAÇÃO DE CARTEIRA DE INVESTIMENTOS')
    st.subheader('Disciplina: Estratégia em finanças')
    st.subheader('Professor: Daniel Augusto de Souza ')
    
    st.write('O objetivo do trabalho é calcular duas medidas fundamentais para avaliar a performance de uma carteira de investimentos em relação ao mercado, utilizando o modelo de precificação de ativos financeiros (CAPM). Essas medidas são o alfa e o beta da carteira. ')
    
    stocks_csv = pd.read_csv('stocks.csv')
    stocks = sorted(st.sidebar.multiselect('Insira o ticker das ações na carteira:',stocks_csv, max_selections=4))
    intervalo = st.sidebar.selectbox('Selecione o intervalo:',('1d','1mo'))
    start = st.sidebar.date_input('Selecione a data inicial:', value=datetime.date(2015, 1, 1))
    end = st.sidebar.date_input('Selecione a data final:')
    n_stocks = len(stocks)  
    st.sidebar.write(
        'Coloque o peso que cada ativo terá na carteira'
    )
    peso = []
    for i in range(0,n_stocks):
        ps = st.sidebar.number_input(f'Peso do ativo {stocks[i]}',0,100,key=f'peso_{i}')
        peso.append(ps/100)
    if (sum(peso) != 1) & (n_stocks > 0):
        st.sidebar.write('A soma dos pesos tem que ser de 100%')
    elif (sum(peso) == 1):
        if len(stocks) != 4:
            st.sidebar.warning('No momento, é obrigatório escolher 4 ativos!')
        if len(stocks) == 4:
            if st.sidebar.button('Gerar Carteira'):
                ### ========= ARQUITETURA DA PÁGINA ========= ### 

                ### ========= Dataframe dos ativos selecionados ========= ### 
                st.markdown(
                    '***Dataframe dos ativos escolhidos***'
                )
                
                df, df_bova, df_retorno = baixar_base_dados_yfinance(stocks, interval=intervalo, start=start, end=end)
                df_selic = baixar_selic(start=start, end=end)
                
                with st.expander('Dataframe dos ativos escolhidos', expanded=False):
                    st.write(df)
                with st.expander('Dataframe dos retornos dos ativos', expanded=False):
                    st.write(df_retorno)
                with st.expander('Dataframe do Benchmarck (BOVA11)'):
                    st.write(df_bova)
                with st.expander('Dataframe da Selic (diária)'):
                    st.write(df_selic)
                    
                    
                ### ========= Covariância dos retornos dos ativos selecionados ========= ### 
                st.markdown(
                    '***Covariância dos retornos dos ativos selecionados***'
                )               
                cov_retornos = df_retorno.cov()
                st.write(cov_retornos, )
                    
                    
                ### ========= Risco e Retorno dos ativos selecionados ========= ### 
                st.markdown(
                    '***Risco e Retorno dos ativos selecionados***'
                )
                risco_ativos = df_retorno.std()
                retorno_ativos = df_retorno.mean()
                risco_retorno = pd.concat([risco_ativos,retorno_ativos], axis=1)
                risco_retorno.rename(columns={0:'Risco', 1:'Retorno'}, inplace=True)
                st.write(risco_retorno)
                
                ### ========= Risco e Retorno do PORTFÓLIO ========= ### 
                st.markdown(
                    '***Risco e Retorno do PORTFÓLIO***'
                )
                df_risco_retorno = pd.concat([risco_ativos,retorno_ativos], axis=1)
                df_risco_retorno.rename(columns={0:'Risco', 1:'Retorno'}, inplace=True)
                df_risco_retorno['W'] = peso
                df_risco_retorno['W²'] = np.square(peso)
                df_risco_retorno['sigma²'] = np.square(df_risco_retorno['Retorno'])
                df_risco_retorno['W² x sigma²'] = df_risco_retorno['W²'] * df_risco_retorno['sigma²']
                st.write(df_risco_retorno)
                
                retorno_portfolio = (retorno_ativos*peso).sum()
                st.write(f'O retorno do portfólio foi de {round(retorno_portfolio,5)}')
                
                risco_portfolio = np.sqrt(
                df_risco_retorno['W² x sigma²'].sum() 
                + (2 * df_risco_retorno['W'][0] * df_risco_retorno['W'][1] * cov_retornos[f'ln_{stocks[0]}'][1])
                + (2 * df_risco_retorno['W'][0] * df_risco_retorno['W'][2] * cov_retornos[f'ln_{stocks[0]}'][2])
                + (2 * df_risco_retorno['W'][0] * df_risco_retorno['W'][3] * cov_retornos[f'ln_{stocks[0]}'][3])
                + (2 * df_risco_retorno['W'][1] * df_risco_retorno['W'][2] * cov_retornos[f'ln_{stocks[1]}'][2])
                + (2 * df_risco_retorno['W'][1] * df_risco_retorno['W'][3] * cov_retornos[f'ln_{stocks[1]}'][3])
                + (2 * df_risco_retorno['W'][2] * df_risco_retorno['W'][3] * cov_retornos[f'ln_{stocks[2]}'][3])
                )
                st.write(f'O risco do portfólio foi de {round(risco_portfolio,5)}')
                
                ### ========= Calculando o alfa e o beta da sua carteira por meio do CAPM ========= ### 
                st.markdown(
                    '***Calculando o alfa e o beta da sua carteira por meio do CAPM***'
                )
                rp = retorno_portfolio
                retorno_bova = np.log(df_bova.shift(-1) / df_bova)
                rm = retorno_bova.mean()
                retorno_selic = np.log(df_selic.shift(-1) / df_selic)
                rf = retorno_selic.mean()
                
                carteira = df_retorno*peso
                carteira['carteira'] = carteira[f'ln_{stocks[0]}']+carteira[f'ln_{stocks[1]}']+carteira[f'ln_{stocks[2]}']+carteira[f'ln_{stocks[3]}']
                df_cov_portfolio_mercado = pd.concat([carteira['carteira'],retorno_bova], axis=1)
                df_cov_portfolio_mercado.rename(columns={'Adj Close':'mercado'}, inplace=True)
                df_cov_portfolio_mercado = df_cov_portfolio_mercado.cov()
                cov_portfolio_mercado = df_cov_portfolio_mercado['mercado'][1]
                
                var_retornos_mercado = retorno_bova.var()
                beta = cov_portfolio_mercado/var_retornos_mercado
                alpha = rp - (rf + beta*(rm - rf))
                
                st.success(f'Retorno da carteira (Rp): {round(rp,7)}')
                st.success(f'Retorno do mercado (Rm): {round(rm,7)}')
                st.success(f'Taxa livre de risco (Rf): {round(rf,7)}')
                st.success(f'Covariância entre os retornos da carteira e do mercado: {round(cov_portfolio_mercado,20)}')
                st.success(f'Variância dos retornos do mercado: {round(var_retornos_mercado,20)}')
                st.success(f'Beta (b): {round(beta,20)}')
                st.success(f'Alpha (a): {round(alpha,20)}')

