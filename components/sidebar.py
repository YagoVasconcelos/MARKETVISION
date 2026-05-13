import streamlit as st
import os
from datetime import datetime
from services.loader import load_csv

def render_sidebar(df_raw):

    cidades_sel = []
    setor_sel = "Todos"

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

                if uploaded_file.size > 50 * 1024 * 1024:
                    st.error("Arquivo muito grande.")
                    st.stop()

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

        st.markdown("### 🗂 Histórico")
        st.info(f"📁 Base ativa: {st.session_state.base_ativa}")

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

            cidades_unicas = sorted(
                df_raw['cidade'].dropna().unique()
            )

            cidades_sel = st.multiselect(
                "Cidades",
                cidades_unicas,
                default=[],
                key="c_filt",
                label_visibility="collapsed"
            )

        st.markdown("<p class='sidebar-label'>🏢 SEGMENTO</p>", unsafe_allow_html=True)

        if 'setor' in df_raw.columns:

            setores = ["Todos"] + sorted(
                list(df_raw['setor'].unique())
            )

            setor_sel = st.selectbox(
                "Setores",
                setores,
                key="s_filt",
                label_visibility="collapsed"
            )

        st.divider()

    return cidades_sel, setor_sel