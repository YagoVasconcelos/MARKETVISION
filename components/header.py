import streamlit as st
import os

def render_header():

    col_logo, col_txt = st.columns([0.6, 9.4])

    with col_logo:
        if os.path.exists("assets/logo.png"):
            st.image("assets/logo.png", width=60)

    with col_txt:
        st.markdown(
            "<h2 style='margin: 0; padding: 0; line-height: 1;'>MarketVision PRO</h2>",
            unsafe_allow_html=True
        )

        st.markdown(
            "<p style='color: #64748b; margin: 0;'>Inteligência de Mercado | Big Data</p>",
            unsafe_allow_html=True
        )
        