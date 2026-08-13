# imports
import pandas as pd
import yfinance as yf
import datetime as dt
import os
from sqlalchemy import create_engine, text
from dotenv import load_dotenv


# Variáveis de ambiente
commodities = ['GC=F', 'CL=F', 'NG=F', 'SI=F']

load_dotenv()

DB_HOST = os.getenv('DB_HOST')
DB_PORT = os.getenv('DB_PORT')
DB_NAME = os.getenv('DB_NAME')
DB_USER = os.getenv('DB_USER')
DB_PASSWORD = os.getenv('DB_PASSWORD')
DB_SCHEMA = os.getenv('DB_SCHEMA')

DB_URL = f"postgresql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"

engine = create_engine(DB_URL)

# extração de dados

def buscar_dados_commodities(simbolo, period="3y"):
    ticker = yf.Ticker(simbolo)
    dados = ticker.history(period=period)[["Close"]]
    dados["simbolo"] = simbolo
    return dados

def buscar_todos_dados_commodities(commodities):
    todos_dados = []
    for simbolo in commodities:
        dados = buscar_dados_commodities(simbolo)
        todos_dados.append(dados)
    return pd.concat(todos_dados)

def salvar_no_postgres(df, schema='public'):
    with engine.begin() as conn:
        conn.execute(text(f'TRUNCATE TABLE {schema}.commodities'))

    df.to_sql('commodities', engine, schema=schema, if_exists='append', index=True, index_label='date')

# inicialização teste

if __name__ == "__main__":
    dados_concatenados = buscar_todos_dados_commodities(commodities)
    salvar_no_postgres(dados_concatenados)