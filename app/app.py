import pandas as pd
import streamlit as st
import os
from sqlalchemy import create_engine
from sqlalchemy.engine import URL
from dotenv import load_dotenv

load_dotenv()

def get_setting(name):
    if name in st.secrets and st.secrets.get(name):
        return st.secrets.get(name)
    return os.getenv(name)


DB_HOST = get_setting('DB_HOST')
DB_PORT = get_setting('DB_PORT')
DB_NAME = get_setting('DB_NAME')
DB_USER = get_setting('DB_USER')
DB_PASSWORD = get_setting('DB_PASSWORD')

missing_settings = [
    name for name, value in {
        'DB_HOST': DB_HOST,
        'DB_NAME': DB_NAME,
        'DB_USER': DB_USER,
        'DB_PASSWORD': DB_PASSWORD,
    }.items()
    if not value
]

if missing_settings:
    st.error(
        'Faltam variáveis de conexão configuradas: ' + ', '.join(missing_settings)
    )
    st.stop()

try:
    db_port = int(DB_PORT) if DB_PORT not in (None, '') else None
except ValueError:
    st.error('DB_PORT precisa ser um número inteiro válido.')
    st.stop()

DB_URL = URL.create(
    drivername='postgresql',
    username=DB_USER,
    password=DB_PASSWORD,
    host=DB_HOST,
    port=db_port,
    database=DB_NAME,
)

engine = create_engine(DB_URL)

def get_data():
    query = "SELECT * FROM public.dm_commodities"
    df = pd.read_sql(query, engine)
    return df

st.set_page_config(page_title="Dash de commodities", layout="wide")

st.title("Info de commodities do último dia")

df = get_data()

st.dataframe(df)

