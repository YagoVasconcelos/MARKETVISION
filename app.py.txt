import streamlit as st
import pandas as pd
import plotly.express as px

# CONFIG
st.set_page_config(
    page_title="MarketVision PRO",
    layout="wide",
    page_icon="📊"
)

# DARK STYLE
st.markdown("""
    <style>
        .stApp {
            background-color: #0e1117;
            color: white;
        }
        .css-1d391kg {
            background-color: #111827;
        }
    </style>
""", unsafe_allow_html=True)

# HEADER
st.title("🚀 MarketVision PRO")
st.markdown("### Inteligência de Mercado com Big Data")

# SIDEBAR
st.sidebar.title("📂 Controle")
file = st.sidebar.file_uploader("Envie um CSV", type=["csv"])

# FUNÇÃO
@st.cache_data
def load_data(file):
    df = pd.read_csv(file)
    df.columns = df.columns.str.lower()
    return df

if file:
    df = load_data(file)

    # FILTRO
    st.sidebar.subheader("🔎 Filtros")
    cidade = st.sidebar.multiselect("Cidade", df['cidade'].unique(), default=df['cidade'].unique())

    df = df[df['cidade'].isin(cidade)]

    # KPIs
    col1, col2, col3 = st.columns(3)

    col1.metric("Empresas", len(df))
    col2.metric("Setores", df['setor'].nunique())
    col3.metric("Cidades", df['cidade'].nunique())

    st.divider()

    # GRÁFICO
    colA, colB = st.columns(2)

    with colA:
        st.subheader("🏢 Setores")
        fig = px.pie(df, names='setor')
        st.plotly_chart(fig, use_container_width=True)

    with colB:
        st.subheader("📊 Distribuição")
        fig2 = px.bar(df['setor'].value_counts().reset_index(),
                      x='setor', y='count')
        st.plotly_chart(fig2, use_container_width=True)

    st.divider()

    # MAPA
    if 'lat' in df and 'lon' in df:
        st.subheader("🗺️ Mapa de Empresas")
        st.map(df[['lat', 'lon']])

    # OPORTUNIDADES
    st.subheader("💡 Oportunidades")
    setor_count = df['setor'].value_counts()
    oportunidades = setor_count[setor_count < 3]

    st.dataframe(oportunidades)

else:
    st.info("👈 Envie um CSV para começar")