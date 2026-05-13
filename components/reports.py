import streamlit as st

def render_reports(df_filtered):

    st.subheader("📄 Relatórios")

    csv_data = (
        df_filtered
        .to_csv(index=False)
        .encode('utf-8')
    )

    st.download_button(
        "📥 Baixar CSV Filtrado",
        csv_data,
        "relatorio_marketvision.csv",
        "text/csv"
    )