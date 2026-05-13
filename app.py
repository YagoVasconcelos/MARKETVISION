import streamlit as st
import pandas as pd
import os
from datetime import datetime
from services.filters import apply_filters
from services.charts import (create_pie_chart, create_bar_chart, create_map)

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

# --- 4. PAINEL LATERAL (SIDEBAR) ---
with st.sidebar:
    st.markdown("### ⚙️ MarketVision")
    st.caption("v2.5 | Intelligence & Big Data")
    st.divider()

    with st.expander("📂 Carregar Dados", expanded=False):

        uploaded_file = st.file_uploader(
            "CSV",
            type=["csv"],
            label_visibility="collapsed"
        )

        if uploaded_file:

            nome_arquivo = (
                f"{datetime.now().strftime('%Y%m%d_%H%M%S')}_"
                f"{uploaded_file.name}"
            )

            caminho_upload = os.path.join(
                "data",
                "raw",
                "uploads",
                nome_arquivo
            )

            with open(caminho_upload, "wb") as f:
                f.write(uploaded_file.getbuffer())

            st.session_state.df_raw = load_csv(caminho_upload)
            st.session_state.base_ativa = nome_arquivo

            df_raw = st.session_state.df_raw

            st.success(f"Arquivo salvo: {nome_arquivo}")

    # HISTÓRICO DE BASES
    st.markdown("### 🗂 Histórico")
    st.success(f"📁 Base ativa: {st.session_state.base_ativa}")
    pasta_uploads = os.path.join(
        "data",
        "raw",
        "uploads"
    )

    arquivos = []

    if os.path.exists(pasta_uploads):

        arquivos = sorted(
            os.listdir(pasta_uploads),
            reverse=True
        )

    if arquivos:

        arquivo_escolhido = st.selectbox(
            "Bases disponíveis",
            arquivos,
            label_visibility="collapsed"
        )

        if st.button("📂 Abrir Base"):

            caminho_base = os.path.join(
                pasta_uploads,
                arquivo_escolhido
            )

            st.session_state.df_raw = load_csv(caminho_base)
            st.session_state.base_ativa = arquivo_escolhido

            df_raw = st.session_state.df_raw

            st.success(f"Base carregada: {arquivo_escolhido}")

    else:

        st.info("Nenhuma base salva.")

    st.markdown("<p class='sidebar-label'>📍 LOCALIZAÇÃO</p>", unsafe_allow_html=True)
    if 'cidade' in df_raw.columns:
        cidades_unicas = sorted(df_raw['cidade'].dropna().unique())
        cidades_sel = st.multiselect(
            "Cidades",
            cidades_unicas,
            default=[],
            key="c_filt",
            label_visibility="collapsed"
        )

    st.markdown("<p class='sidebar-label'>🏢 SEGMENTO</p>", unsafe_allow_html=True)
    if 'setor' in df_raw.columns:
        setores = ["Todos"] + sorted(list(df_raw['setor'].unique()))
        setor_sel = st.selectbox(
            "Setores", setores, 
            key="s_filt", label_visibility="collapsed"
        )
    st.divider()

# --- 5. APLICAÇÃO DOS FILTROS
df_filtered = apply_filters(
    df_raw,
    cidades=cidades_sel,
    setor=setor_sel
)

# --- 6. HEADER REFORMULADO (COLE AQUI POR CIMA DO ANTIGO) ---
# Usamos colunas bem ajustadas para o texto ficar colado no logo
col_logo, col_txt = st.columns([0.6, 9.4]) 

with col_logo:
    if os.path.exists("assets/logo.png"): 
        st.image("assets/logo.png", width=60) 

with col_txt:
    # Usamos HTML para forçar o título a subir e não ter margem embaixo
    st.markdown("<h2 style='margin: 0; padding: 0; line-height: 1;'>MarketVision PRO</h2>", unsafe_allow_html=True)
    st.markdown("<p style='color: #64748b; margin: 0;'>Inteligência de Mercado | Big Data</p>", unsafe_allow_html=True)

# As abas (tabs) vêm logo em seguida, sem espaço vazio
tab1, tab2, tab3 = st.tabs(["📊 Dashboard", "🧠 Insights", "📄 Relatórios"])

# --- DAQUI PARA BAIXO SEGUE O RESTO DO SEU CÓDIGO (with tab1:, etc) ---

with tab1:
    m1, m2, m3 = st.columns(3)
    m1.metric("🏢 Empresas no Filtro", len(df_filtered))
    m2.metric("📊 Setores Ativos", df_filtered['setor'].nunique() if 'setor' in df_filtered else 0)
    m3.metric("🌍 Cidades", df_filtered['cidade'].nunique() if 'cidade' in df_filtered else 0)

    st.divider()

    c1, c2 = st.columns(2)
    with c1:
        with st.container(border=True):
            st.subheader("🏢 Distribuição")
            fig = create_pie_chart(df_filtered)
            # Tira a margem interna para o gráfico crescer na caixa
            fig.update_layout(margin=dict(t=30, b=10, l=10, r=10), height=350)
            st.plotly_chart(fig, width='stretch', key="p_main")
    
    with c2:
        with st.container(border=True):
            st.subheader("💰 Capital Médio")
            
            # --- ALTERAÇÃO AQUI ---
            fig2 = create_bar_chart(df_filtered)
            
            fig2.update_layout(
                margin=dict(t=30, b=10, l=10, r=10), 
                height=350,
                showlegend=False # Esconde a legenda aqui para não poluir, já que a da pizza serve
            )
            # -----------------------
            
            st.plotly_chart(fig2, width='stretch', key="b_cap")

    # MAPA COM TRAVA DE SEGURANÇA
    if 'lat' in df_filtered.columns and 'lon' in df_filtered.columns:
        with st.container(border=True):
            st.subheader("🗺️ Inteligência Geográfica (Dados Oficiais)")

            # Criando o mapa
            fig_mapa = create_map(df_filtered)

            # Configurando o balão (Hover) de forma manual e segura
            fig_mapa.update_traces(
                hovertemplate="""
                <b>%{hovertext}</b><br>
                <b>CNPJ:</b> %{customdata[0]}<br>
                <b>Setor:</b> %{customdata[1]}<br>
                <b>Capital:</b> R$ %{customdata[2]:,.2f}<br>
                <b>Cidade:</b> %{customdata[3]}
                <extra></extra>
                """
            )

            fig_mapa.update_layout(
                height=700,
                margin={"r":0,"t":0,"l":0,"b":0},
                legend=dict(orientation="h", yanchor="bottom", y=0.01, xanchor="left", x=0.01, bgcolor="rgba(0,0,0,0.5)")
            )

            st.plotly_chart(fig_mapa, width='stretch', key="mapa_final_v3")

with tab2:
    st.subheader("🧠 Consultoria Estratégica MarketVision")
    if not df_filtered.empty:
        if 'data_abertura' in df_filtered.columns:
            df_filtered['idade_anos'] = (pd.Timestamp.now() - pd.to_datetime(df_filtered['data_abertura'])).dt.days / 365
            c1, c2 = st.columns(2)
            with c1:
                st.write("### ⏳ Sobrevivência por Setor")
                sobrevivencia = df_filtered.groupby('setor')['idade_anos'].mean().sort_values(ascending=False)
                st.bar_chart(sobrevivencia)
            with c2:
                st.write("### 🔥 Aberturas Recentes (2 anos)")
                recentes = df_filtered[df_filtered['idade_anos'] <= 2]
                if not recentes.empty: st.line_chart(recentes['setor'].value_counts())

        st.divider()
        st.subheader("💡 Simulador de Investimento Inteligente")
        meu_capital = st.number_input("Investimento pretendido (R$)", min_value=1000, value=50000)
        stats = df_filtered.groupby('setor').agg({'capital_social': 'mean', 'setor': 'count'}).rename(columns={'setor': 'qtd'}).reset_index()
        if not stats.empty:
            melhor = stats.sort_values(by='qtd').iloc[0]
            st.success(f"✅ Recomendação: O setor de **{melhor['setor']}** apresenta menor concorrência.")
    else:
        st.warning("⚠️ Ajuste os filtros para gerar insights.")

with tab3:
    st.subheader("📄 Relatórios")
    csv_data = df_filtered.to_csv(index=False).encode('utf-8')
    st.download_button("📥 Baixar CSV Filtrado", csv_data, "relatorio_marketvision.csv", "text/csv")