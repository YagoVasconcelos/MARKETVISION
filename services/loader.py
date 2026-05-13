import pandas as pd
import streamlit as st

@st.cache_data
def load_csv(path):

    df = pd.read_csv(path)

    df.columns = df.columns.str.lower()

    if 'data_abertura' in df.columns:
        df['data_abertura'] = pd.to_datetime(
            df['data_abertura'],
            errors='coerce'
        )

    if 'capital_social' in df.columns:
        df['capital_social'] = pd.to_numeric(
            df['capital_social'],
            errors='coerce'
        ).fillna(0)

    return df