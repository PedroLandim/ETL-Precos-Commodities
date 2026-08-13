import pandas as pd
import streamlit as st
import os
from sqlalchemy import create_engine, text
from dotenv import load_dotenv

load_dotenv()

DB_HOST = os.getenv('DB_HOST')
DB_PORT = os.getenv('DB_PORT')
DB_NAME = os.getenv('DB_NAME')
DB_USER = os.getenv('DB_USER')
DB_PASSWORD = os.getenv('DB_PASSWORD')
DB_SCHEMA = os.getenv('DB_SCHEMA')

DB_URL = f"postgresql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"

engine = create_engine(DB_URL)

def get_data():
    query = "SELECT * FROM public.dm_commodities"
    df = pd.read_sql(query, engine)
    return df

st.set_page_config(page_title="Dash de commodities", layout="wide")

st.title("Info de commodities do último dia")

df = get_data()

st.dataframe(df)

