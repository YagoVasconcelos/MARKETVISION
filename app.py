import streamlit as st
import pandas as pd
import plotly.express as px
import os

# CONFIG
st.set_page_config(
    page_title="MarketVision PRO",
    layout="wide",
    page_icon="📊"
)

st.image("logo.png", width=150)

# DARK MODE
st.markdown("""
    <style>
        .stApp {
            background-color: #0e1117;
            color: white;
        }
    </style>
""", unsafe_allow_html=True)

# HEADER
st.title("🚀 MarketVision PRO")
st.markdown("### Inteligência de Mercado com Big Data")

# SIDEBAR
st.sidebar.title("📂 Controle")
file = st.sidebar.file_uploader("Envie um CSV", type=["csv"])

# =========================
# LOAD DATA (SEM BUG)
# =========================
def load_data(source):
    df = pd.read_csv(source)
    df.columns = df.columns.str.lower()
    return df

# =========================
# CARREGAMENTO SEGURO
# =========================
try:
    if file:
        df = load_data(file)
    else:
        caminho = os.path.join("data", "exemplo.csv")
        df = load_data(caminho)
except Exception as e:
    st.error(f"Erro ao carregar dados: {e}")
    st.stop()

# =========================
# FILTROS
# =========================
st.sidebar.subheader("🔎 Filtros")

if 'cidade' in df.columns:
    cidade = st.sidebar.multiselect(
        "Cidade",
        df['cidade'].dropna().unique(),
        default=df['cidade'].dropna().unique()
    )
    df = df[df['cidade'].isin(cidade)]

# =========================
# KPIs
# =========================
col1, col2, col3 = st.columns(3)

col1.metric("Empresas", len(df))
col2.metric("Setores", df['setor'].nunique() if 'setor' in df.columns else 0)
col3.metric("Cidades", df['cidade'].nunique() if 'cidade' in df.columns else 0)

st.divider()

# =========================
# GRÁFICOS
# =========================
colA, colB = st.columns(2)

with colA:
    st.subheader("🏢 Setores")
    if 'setor' in df.columns:
        fig = px.pie(df, names='setor')
        st.plotly_chart(fig, width='stretch', key="grafico_pizza")

with colB:
    st.subheader("📊 Distribuição")
    if 'setor' in df.columns:
        setor_df = df['setor'].value_counts().reset_index()
        setor_df.columns = ['setor', 'count']
        fig2 = px.bar(setor_df, x='setor', y='count')
        st.plotly_chart(fig2, width='stretch', key="grafico_barra")

st.divider()

# =========================
# MAPA
# =========================
if 'lat' in df.columns and 'lon' in df.columns:
    st.subheader("🗺️ Mapa de Empresas")
    st.map(df[['lat', 'lon']])

# =========================
# OPORTUNIDADES
# =========================
oportunidades = (
    df['setor']
    .value_counts()
    .loc[lambda x: x < 3]
    .to_frame(name="quantidade")
)

st.dataframe(oportunidades)