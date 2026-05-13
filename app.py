import streamlit as st
import pandas as pd
import os
from datetime import datetime
from services.filters import apply_filters
from services.charts import (create_pie_chart, create_bar_chart, create_map)
from components.header import render_header
from components.sidebar import render_sidebar
from components.dashboard import render_dashboard
from components.insights import render_insights
from components.reports import render_reports
from services.analytics import calcular_sobrevivencia


# --- SESSION STATE INICIAL ---
if "df_raw" not in st.session_state:
    st.session_state.df_raw = None

if "base_ativa" not in st.session_state:
    st.session_state.base_ativa = "empresas.csv"

# --- CONFIGURAÇÃO ---
st.set_page_config(page_title="MarketVision PRO", layout="wide", page_icon="assets/logo.png")

with open("styles/style.css") as f:
    st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

# --- 2. FUNÇÃO DE CARREGAMENTO ---
from services.loader import load_csv

# --- 3. LOGICA INICIAL DE DADOS ---
file = None

try:
    if st.session_state.df_raw is None:
        caminho_exemplo = os.path.join(
            "data",
            "raw",
            "empresas.csv"
        )
        st.session_state.df_raw = load_csv(caminho_exemplo)

except Exception as e:

    st.error(f"Erro ao carregar base: {e}")
    st.stop()

df_raw = st.session_state.df_raw

# --- VALORES PADRÃO DOS FILTROS ---
cidades_sel = []
setor_sel = "Todos"

# --- 4. SIDEBAR COMPONENT ---
cidades_sel, setor_sel = render_sidebar(df_raw)

# --- 5. APLICAÇÃO DOS FILTROS
df_filtered = apply_filters(
    df_raw,
    cidades=cidades_sel,
    setor=setor_sel
)

render_header()

# As abas (tabs) vêm logo em seguida, sem espaço vazio
tab1, tab2, tab3 = st.tabs(["📊 Dashboard", "🧠 Insights", "📄 Relatórios"])

with tab1:
    render_dashboard(df_filtered)

with tab2:
    render_insights(df_filtered)

with tab3:
    render_reports(df_filtered)