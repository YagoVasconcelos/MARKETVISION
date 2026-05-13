import streamlit as st

from services.analytics import (
    calcular_sobrevivencia,
    calcular_aberturas_recentes,
    calcular_melhor_setor
)


def render_insights(df_filtered):

    st.subheader("🧠 Consultoria Estratégica MarketVision")

    if df_filtered.empty:
        st.warning("⚠️ Ajuste os filtros para gerar insights.")
        return

    c1, c2 = st.columns(2)

    with c1:

        st.write("### ⏳ Sobrevivência por Setor")

        sobrevivencia = calcular_sobrevivencia(df_filtered)

        if not sobrevivencia.empty:
            st.bar_chart(sobrevivencia)

    with c2:

        st.write("### 🔥 Aberturas Recentes (2 anos)")

        recentes = calcular_aberturas_recentes(df_filtered)

        if not recentes.empty:
            st.line_chart(recentes)

    st.divider()

    st.subheader("💡 Simulador de Investimento Inteligente")

    st.number_input(
        "Investimento pretendido (R$)",
        min_value=1000,
        value=50000
    )

    melhor = calcular_melhor_setor(df_filtered)

    if melhor is not None:

        st.success(
            f"""
            ✅ Recomendação:
            O setor de **{melhor['setor']}**
            apresenta menor concorrência.
            """
        )