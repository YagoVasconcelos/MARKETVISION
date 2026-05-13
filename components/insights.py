import streamlit as st

from services.analytics import (
    calcular_sobrevivencia,
    calcular_aberturas_recentes,
    calcular_melhor_setor,
    calcular_score_oportunidade,
    calcular_regioes_oportunidade
)

def render_insights(df_filtered):

    st.subheader("🧠 Consultoria Estratégica MarketVision")

    if df_filtered.empty:
        st.warning("⚠️ Ajuste os filtros para gerar insights.")
        return

    # ==================================================
    # GRÁFICOS ANALÍTICOS
    # ==================================================

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

    # ==================================================
    # SIMULADOR
    # ==================================================

    st.subheader("💡 Simulador de Investimento Inteligente")

    meu_capital = st.number_input(
        "Investimento pretendido (R$)",
        min_value=1000,
        value=50000
    )

    # ==================================================
    # RANKING
    # ==================================================

    st.subheader("📈 Ranking Inteligente de Oportunidades")

    score_df = calcular_score_oportunidade(
        df_filtered,
        meu_capital
    )

    if not score_df.empty:

        st.dataframe(
            score_df.style.background_gradient(
                subset=["score"],
                cmap="RdYlGn"
            ),
            width='stretch'
        )

        st.bar_chart(
            score_df.set_index("setor")["score"]
        )

        top = score_df.iloc[0]

        st.progress(
            min(
                int(top["score"] * 5),
                100
            )
        )

        st.markdown(
            f"""
            ### 🏆 Melhor Oportunidade Atual

            **Setor:** {top['setor']}

            **Score Estratégico:** {top['score']:.2f}

            **Concorrência:** {top['concorrencia']}

            **Capital Médio:** R$ {top['capital_medio']:,.2f}

            **Sobrevivência Média:** {top['sobrevivencia']:.1f} anos
            """
        )

        st.success(
            f"""
            ✅ Recomendação Estratégica:

            O setor de **{top['setor']}**
            apresenta atualmente:

            - menor concorrência
            - boa sobrevivência empresarial
            - melhor oportunidade regional
            - equilíbrio entre capital e mercado
            """
        )

        k1, k2, k3 = st.columns(3)

        k1.metric(
            "🏢 Empresas Analisadas",
            len(df_filtered)
        )

        k2.metric(
            "📈 Melhor Score",
            round(score_df["score"].max(), 2)
        )

        k3.metric(
            "🔥 Setor Líder",
            score_df.iloc[0]["setor"]
        )

        st.subheader("🌎 Regiões Mais Promissoras")

        regioes = calcular_regioes_oportunidade(df_filtered)

        st.dataframe(regioes)

        st.bar_chart(
            regioes.set_index("cidade")["score_regiao"]
        )