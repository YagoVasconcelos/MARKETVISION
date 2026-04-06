import streamlit as st
import pandas as pd
import plotly.express as px
import numpy as np
import os

# --- CONFIGURAÇÃO ---
st.set_page_config(page_title="MarketVision PRO", layout="wide", page_icon="assets/logo.png")

st.markdown("""
    <style>
        /* 1. Remove o espaço gigante do topo da página */
        .block-container {
            padding-top: 3rem !important;
            padding-bottom: 0rem !important;
            padding-left: 3rem !important;
            padding-right: 3rem !important;
        }

        /* 2. Reduz o espaço entre o Header (MarketVision) e as Tabs */
        [data-testid="stVerticalBlock"] > div:has(div.stTabs) {
            margin-top: -30px !important;
        }

        /* 3. Reduz o espaço entre as Métricas (10000) e o conteúdo abaixo */
        [data-testid="stMetric"] {
            padding: 2px !important;
            margin-bottom: -10px !important;
        }

        /* 4. Remove o espaço morto entre colunas e o divisor (st.divider) */
        hr {
            margin-top: 1px !important;
            margin-bottom: 1px !important;
        }

        /* 5. Ajuste fino na sidebar para acompanhar o topo */
        [data-testid="stSidebarUserContent"] {
            padding-top: -1rem !important;
        }
        
        /* 6. Puxa o título para perto do logo */
        .stMarkdown h2 {
            margin-top: -10px !important;
            padding-bottom: 0px !important;
        }
    </style>
""", unsafe_allow_html=True)

# --- 2. FUNÇÃO DE CARREGAMENTO ---
def load_data(source):
    df = pd.read_csv(source)
    df.columns = df.columns.str.lower()
    if 'data_abertura' in df.columns:
        df['data_abertura'] = pd.to_datetime(df['data_abertura'])
    if 'capital_social' in df.columns:
        df['capital_social'] = pd.to_numeric(df['capital_social'], errors='coerce').fillna(0)
    return df

# --- 3. LOGICA INICIAL DE DADOS (CORRIGIDO: VEM ANTES DA SIDEBAR) ---
file = None # Inicializa para evitar erros
try:
    # Primeiro verificamos se há um arquivo na sidebar ANTES de renderizar o resto
    caminho_exemplo = os.path.join("data", "exemplo.csv")
    df_raw = load_data(caminho_exemplo)
except Exception as e:
    st.error(f"Erro ao carregar base: {e}")
    st.stop()

# --- 4. PAINEL LATERAL (SIDEBAR) ---
with st.sidebar:
    st.markdown("### ⚙️ MarketVision")
    st.caption("v2.5 | Intelligence & Big Data")
    st.divider()

    with st.expander("📂 Carregar Dados", expanded=False):
        uploaded_file = st.file_uploader("CSV", type=["csv"], label_visibility="collapsed")
        if uploaded_file:
            df_raw = load_data(uploaded_file)

    st.markdown("<p class='sidebar-label'>📍 LOCALIZAÇÃO</p>", unsafe_allow_html=True)
    if 'cidade' in df_raw.columns:
        cidades_unicas = sorted(df_raw['cidade'].dropna().unique())
        cidades_sel = st.multiselect(
            "Cidades", cidades_unicas, default=cidades_unicas, 
            key="c_filt", label_visibility="collapsed"
        )

    st.markdown("<p class='sidebar-label'>🏢 SEGMENTO</p>", unsafe_allow_html=True)
    if 'setor' in df_raw.columns:
        setores = ["Todos"] + sorted(list(df_raw['setor'].unique()))
        setor_sel = st.selectbox(
            "Setores", setores, 
            key="s_filt", label_visibility="collapsed"
        )
    st.divider()

# --- 5. APLICAÇÃO DOS FILTROS ---
# --- 5. APLICAÇÃO DOS FILTROS --- (Mantenha o que você já tem aqui)
df_filtered = df_raw.copy()
if 'cidade' in df_raw.columns:
    df_filtered = df_filtered[df_filtered['cidade'].isin(cidades_sel)]

if 'setor' in df_raw.columns and setor_sel != "Todos":
    df_filtered = df_filtered[df_filtered['setor'] == setor_sel]


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
            fig = px.pie(df_filtered, names='setor', hole=0.4)
            # Tira a margem interna para o gráfico crescer na caixa
            fig.update_layout(margin=dict(t=30, b=10, l=10, r=10), height=350)
            st.plotly_chart(fig, width='stretch', key="p_main")
    
    with c2:
        with st.container(border=True):
            st.subheader("💰 Capital Médio")
            cap_setor = df_filtered.groupby('setor')['capital_social'].mean().reset_index()
            fig2 = px.bar(cap_setor, x='setor', y='capital_social')
            # Tira a margem interna e ajusta a altura
            fig2.update_layout(margin=dict(t=30, b=10, l=10, r=10), height=350)
            st.plotly_chart(fig2, width='stretch', key="b_cap")

    # MAPA COM TRAVA DE SEGURANÇA
    if 'lat' in df_filtered.columns and 'lon' in df_filtered.columns:
        with st.container(border=True):
            st.subheader("🗺️ Localização Real (Dados IBGE)")
            
            # Filtro extra: remove qualquer dado fora do limite do Pará (Segurança anti-oceano)
            df_mapa = df_filtered[
                (df_filtered['lat'] < 2.5) & (df_filtered['lat'] > -10.0) &
                (df_filtered['lon'] < -45.0) & (df_filtered['lon'] > -59.0)
            ]

            fig_mapa = px.scatter_map(
                df_mapa, # Usamos o df_mapa limpo aqui
                lat="lat", lon="lon", 
                color="setor", 
                size_max=12,
                zoom=6, # Zoom mais afastado para ver o estado todo primeiro
                opacity=0.8,
                hover_name="empresa", 
                map_style="carto-darkmatter"
            )
            
            fig_mapa.update_layout(
                height=600, 
                margin={"r":0,"t":0,"l":0,"b":0}
            )
            st.plotly_chart(fig_mapa, width='stretch', key="mapa_final_v10")

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