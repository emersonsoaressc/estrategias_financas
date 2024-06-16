import pandas as pd
import sgs
import numpy as np
import yfinance as yf
import datetime
import streamlit as st

import pandas as pd

from tqdm import tqdm
import random

import warnings
warnings.filterwarnings("ignore")


def baixar_base_dados_yfinance(lista_tickers, interval, start, end):
    tickers = lista_tickers
    df = yf.download(
        tickers=tickers, 
        interval=interval,
        start=start, 
        end=end)['Adj Close']

    df_bova = yf.download(
        tickers=('BOVA11.SA'), 
        interval='1d',
        start='2015-01-01', 
        end='2024-06-11')['Adj Close']

    df_retorno = pd.DataFrame()

    for i in df.columns:
        df_retorno[f'ln_{i}'] = np.log(df[i].shift(-1) / df[i])

    df_retorno.dropna(inplace=True)
    
    return df, df_bova, df_retorno


def baixar_selic(start,end):
    start=start.strftime('%d/%m/%Y')
    end=end.strftime('%d/%m/%Y')
    SELIC_CODE = 11
    df_selic = sgs.time_serie(SELIC_CODE, start='02/01/2015', end='10/06/2024')
    return df_selic