import streamlit as st
import pandas as pd
import plotly.express as px
import numpy as np


# CONFIG
st.set_page_config(
    page_title="MarketVision PRO",
    layout="wide",
    page_icon="assets/logo.png"
)

# =========================
# ESTILO
# =========================
st.markdown("""
<style>
.stApp {
    background-color: #0e1117;
    color: white;
}
section[data-testid="stSidebar"] {
    background-color: #0f172a;
}
</style>
""", unsafe_allow_html=True)

# =========================
# SIDEBAR
# =========================
st.sidebar.title("⚙️ Painel")
file = st.sidebar.file_uploader("Enviar CSV", type=["csv"])

# =========================
# LOAD DATA
# =========================
def load_data(source):
    df = pd.read_csv(source)
    df.columns = df.columns.str.lower()
    return df

if file:
    df = load_data(file)
else:
    df = load_data("data/exemplo.csv")

df['capital'] = np.random.randint(5000, 500000, size=len(df))
st.write(df.columns)
# =========================
# FILTROS (ANTES DE TUDO)
# =========================
st.sidebar.subheader("🔎 Filtros")

if 'cidade' in df.columns:
    cidade = st.sidebar.multiselect(
        "Cidade",
        df['cidade'].dropna().unique(),
        default=df['cidade'].dropna().unique()
    )
    df = df[df['cidade'].isin(cidade)]

if 'data' in df.columns:
    data_range = st.sidebar.date_input(
        "Período",
        [df['data'].min(), df['data'].max()]
    )

# FILTRO POR SETOR
if 'setor' in df.columns:
    setor = st.sidebar.selectbox(
        "Segmento",
        df['setor'].unique()
    )

# =========================
# HEADER
# =========================
col1, col2 = st.columns([1, 5])

with col1:
    st.image("assets/logo.png", width=70)

with col2:
    st.markdown("## MarketVision PRO")
    st.caption("Inteligência de Mercado com Big Data")

# =========================
# TABS
# =========================
tab1, tab2, tab3 = st.tabs(["📊 Dashboard", "🧠 Insights", "📄 Relatórios"])

# =========================
# TAB 1 - DASHBOARD
# =========================
with tab1:

    col1, col2, col3 = st.columns(3)

    col1.metric("Empresas", len(df))
    col2.metric("Setores", df['setor'].nunique() if 'setor' in df.columns else 0)
    col3.metric("Cidades", df['cidade'].nunique() if 'cidade' in df.columns else 0)

    st.divider()

    colA, colB = st.columns(2)

    with colA:
        with st.container(border=True):
            st.subheader("🏢 Setores")
            if 'setor' in df.columns:
                fig = px.pie(df, names='setor')
                st.plotly_chart(fig, width='stretch')

    with colB:
        with st.container(border=True):
            st.subheader("📊 Distribuição")
            if 'setor' in df.columns:
                setor_df = df['setor'].value_counts().reset_index()
                setor_df.columns = ['setor', 'count']
                fig2 = px.bar(setor_df, x='setor', y='count')
                st.plotly_chart(fig2, width='stretch')

    if 'lat' in df.columns and 'lon' in df.columns:
        with st.container(border=True):
            st.subheader("🗺️ Mapa de Empresas")
            st.map(df[['lat', 'lon']])

    st.divider()
    st.subheader("🎯 Oportunidades Detectadas")

    if 'setor' in df.columns:
        oportunidades = (
            df['setor']
            .value_counts()
            .loc[lambda x: x < 3]
            .to_frame(name="Quantidade")
        )

        if not oportunidades.empty:
            st.success("Setores com baixa concorrência identificados 👇")
            st.dataframe(oportunidades)
        else:
            st.warning("Nenhuma oportunidade clara encontrada")

# =========================
# TAB 2 - INSIGHTS
# =========================
with tab2:

    st.subheader("🧠 Inteligência de Mercado")

    if 'setor' in df.columns:

        # =========================
        # RANKING
        # =========================
        ranking = df['setor'].value_counts().reset_index()
        ranking.columns = ['setor', 'quantidade']

        st.subheader("📊 Concorrência por Setor")
        st.dataframe(ranking)

        # =========================
        # RETORNO (capital médio)
        # =========================
        retorno = df.groupby('setor')['capital'].mean().sort_values()

        st.subheader("💰 Capital Médio por Setor")
        st.bar_chart(retorno)

        # =========================
        # SCORE INTELIGENTE
        # =========================
        score = df.groupby('setor').agg({
            'capital': 'mean',
            'setor': 'count'
        })

        score.columns = ['capital_medio', 'concorrencia']
        score['score'] = score['capital_medio'] / score['concorrencia']

        st.subheader("🎯 Score de Oportunidade")
        st.dataframe(score.sort_values(by='score', ascending=False))

        # =========================
        # RECOMENDAÇÃO
        # =========================
        if not score.empty:
            melhor = score.sort_values(by='score', ascending=False).iloc[0]

            st.success(f"""
            💡 Melhor oportunidade de investimento:

            Setor: {melhor.name}

            ✔ Alto capital médio  
            ✔ Baixa concorrência  
            ✔ Maior potencial de crescimento
            """)
        else:
            st.warning("Sem dados suficientes para análise")

# =========================
# TAB 3 - RELATÓRIOS
# =========================
with tab3:

    st.subheader("📄 Exportar Relatório")

    csv = df.to_csv(index=False).encode('utf-8')

    st.download_button(
        label="📥 Baixar CSV",
        data=csv,
        file_name="marketvision_relatorio.csv",
        mime="text/csv"
    )