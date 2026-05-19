import streamlit as st
import plotly.express as px
import pandas as pd

from services.analytics import (
    calcular_score_oportunidade
)

from services.economia import (
    calcular_projecao_financeira,
    calcular_taxa_inteligente,
    calcular_risco_futuro,
    calcular_cenario_economico,
    calcular_impacto_setorial
)


def render_economia(df_filtered):

    st.subheader("📈 Economia Estratégica IA")

    # ==================================================
    # INDICADORES ECONÔMICOS
    # ==================================================

    indicadores = calcular_cenario_economico()

    st.subheader("🌎 Cenário Econômico Atual")

    e1, e2, e3, e4, e5 = st.columns(5)

    e1.metric(
        "💵 Dólar",
        f"R$ {indicadores['dolar']}"
    )

    e2.metric(
        "📈 SELIC",
        f"{indicadores['selic']}%"
    )

    e3.metric(
        "📉 Inflação",
        f"{indicadores['inflacao']}%"
    )

    e4.metric(
        "🇧🇷 PIB",
        f"{indicadores['pib']}%"
    )

    e5.metric(
        "🌎 Estabilidade",
        indicadores["estabilidade"]
    )

    if df_filtered.empty:
        st.warning(
            "⚠️ Ajuste os filtros para gerar projeções."
        )
        return

    # ==================================================
    # CAPITAL
    # ==================================================

    investimento = st.number_input(
        "💰 Capital Inicial para Investimento",
        min_value=1000,
        value=50000,
        step=1000
    )

    # ==================================================
    # SCORE DOS SETORES
    # ==================================================

    score_df = calcular_score_oportunidade(
        df_filtered,
        investimento
    )

    if score_df.empty:
        st.warning(
            "⚠️ Não foi possível calcular projeções."
        )
        return

    # ==================================================
    # TOP 3 SETORES
    # ==================================================

    top3 = score_df.head(3)

    st.subheader("🏆 Top 3 Segmentos Estratégicos")

    top3_view = top3[[

        "setor",
        "score",
        "concorrencia",
        "sobrevivencia"

    ]].copy()

    top3_view = top3_view.rename(columns={

        "setor": "🏢 Setor",

        "score": "🎯 Score Estratégico",

        "concorrencia": "⚔️ Concorrência",

        "sobrevivencia": "📈 Sobrevivência"

    })

    st.dataframe(

        top3_view.style
        .background_gradient(
            subset=["🎯 Score Estratégico"],
            cmap="Greens"
        )
        .format({

            "🎯 Score Estratégico": "{:.2f}",

            "📈 Sobrevivência": "{:.1f} anos"

        }),

        width='stretch',

        column_config={

            "🏢 Setor": st.column_config.TextColumn(
                "🏢 Setor",
                help="""
    Segmento econômico identificado
    como uma das melhores oportunidades
    pela IA estratégica.
    """
            ),

            "🎯 Score Estratégico": st.column_config.ProgressColumn(
                "🎯 Score Estratégico",
                min_value=0,
                max_value=100,
                help="""
    Pontuação estratégica calculada automaticamente.

    O sistema considera:

    • concorrência
    • sobrevivência
    • capital médio
    • potencial econômico
    • oportunidade regional

    Quanto maior o score,
    melhor a oportunidade.
    """,
                format="%.2f"
            ),

            "⚔️ Concorrência": st.column_config.NumberColumn(
                "⚔️ Concorrência",
                help="""
    Quantidade de empresas encontradas
    no segmento analisado.

    Menor concorrência pode indicar:
    • maior espaço de mercado
    • menor saturação
    • melhor oportunidade de entrada
    """,
                format="%d empresas"
            ),

            "📈 Sobrevivência": st.column_config.NumberColumn(
                "📈 Sobrevivência",
                help="""
    Tempo médio de sobrevivência
    das empresas do setor.

    Maior tempo pode indicar:
    • estabilidade empresarial
    • mercado consolidado
    • menor risco operacional
    """,
                format="%.1f anos"
            )

        }
    )

    # ==================================================
    # ECONOMIA GLOBAL
    # ==================================================

    st.subheader("" \
    "" \
    " Global")

    economia = calcular_cenario_economico()

    e1, e2, e3, e4, e5 = st.columns(5)

    e1.metric(
        "💸 Inflação",
        f"{economia['inflacao']}%"
    )

    e2.metric(
        "🏦 SELIC",
        f"{economia['selic']}%"
    )

    e3.metric(
        "💵 Dólar",
        f"R$ {economia['dolar']}"
    )

    e4.metric(
        "📈 PIB",
        f"{economia['pib']}%"
    )

    e5.metric(
        "🛡️ Estabilidade",
        f"{economia['estabilidade']}%"
    )

    # ==================================================
    # CENÁRIO
    # ==================================================

    cenario = st.selectbox(

        "📊 Cenário Econômico",

        [
            "Conservador",
            "Moderado",
            "Agressivo"
        ]
    )

    # ==================================================
    # PROJEÇÕES
    # ==================================================

    resultados = []

    for _, row in top3.iterrows():

        # ==================================================
        # RISCO FUTURO
        # ==================================================

        risco_data = calcular_risco_futuro(row)

        setor = row["setor"]

        # ==================================================
        # TAXA IA DINÂMICA
        # ==================================================

        taxa_base = calcular_taxa_inteligente(row, economia)

        impacto_setorial = calcular_impacto_setorial(
            setor,
            economia
        )

        taxa_base += impacto_setorial

        # ==================================================
        # AJUSTE PELO CENÁRIO
        # ==================================================

        if cenario == "Conservador":

            taxa = taxa_base * 0.8

        elif cenario == "Moderado":

            taxa = taxa_base

        else:

            taxa = taxa_base * 1.25

        # ==================================================
        # PROJEÇÕES
        # ==================================================

        proj_5 = calcular_projecao_financeira(
            investimento,
            taxa,
            5
        )

        proj_10 = calcular_projecao_financeira(
            investimento,
            taxa,
            10
        )

        proj_15 = calcular_projecao_financeira(
            investimento,
            taxa,
            15
        )

        resultados.append({

            "🏢 Setor": setor,

            "📊 Taxa IA": round(
                taxa * 100,
                2
            ),

            "📉 Risco Futuro": risco_data["risco"],

            "🛡️ Estabilidade": risco_data["nivel"],

            "📈 5 Anos": proj_5,

            "🚀 10 Anos": proj_10,

            "💎 15 Anos": proj_15

        })

    projecoes = pd.DataFrame(resultados)

    # ==================================================
    # TABELA
    # ==================================================

    st.subheader("🧠 Projeção Econômica")

    st.dataframe(

        projecoes.style
        .background_gradient(
            subset=["📈 5 Anos", "🚀 10 Anos", "💎 15 Anos"],
            cmap="Greens"
        )
        .background_gradient(
            subset=["📉 Risco Futuro"],
            cmap="Reds"
        )
        .format({

            "📊 Taxa IA": "{:.2f}%",

            "📉 Risco Futuro": "{:.0f}",

            "📈 5 Anos": "R$ {:,.2f}",

            "🚀 10 Anos": "R$ {:,.2f}",

            "💎 15 Anos": "R$ {:,.2f}"

        }),

        width='stretch',

        column_config={

            "🏢 Setor": st.column_config.TextColumn(
                "🏢 Setor",
                help="""
    Segmento econômico analisado pela IA estratégica.
    """
            ),

            "📊 Taxa IA": st.column_config.ProgressColumn(
                "📊 Taxa IA",
                min_value=0,
                max_value=100,
                help="""
    Taxa inteligente de crescimento projetado.

    A IA considera:

    • score estratégico
    • concorrência
    • sobrevivência
    • potencial econômico
    • capacidade de expansão
    """
            ),

            "📉 Risco Futuro": st.column_config.ProgressColumn(
                "📉 Risco Futuro",
                min_value=0,
                max_value=100,
                help="""
    Probabilidade futura de:

    • saturação
    • desaceleração
    • instabilidade econômica
    • retração do mercado
    """
            ),

            "🛡️ Estabilidade": st.column_config.TextColumn(
                "🛡️ Estabilidade",
                help="""
    Classificação automática de estabilidade do setor.
    """
            ),

            "📈 5 Anos": st.column_config.NumberColumn(
                "📈 5 Anos",
                help="Estimativa financeira para 5 anos."
            ),

            "🚀 10 Anos": st.column_config.NumberColumn(
                "🚀 10 Anos",
                help="Estimativa financeira para 10 anos."
            ),

            "💎 15 Anos": st.column_config.NumberColumn(
                "💎 15 Anos",
                help="Estimativa financeira para 15 anos."
            )

        }
    )

    # ==================================================
    # GRÁFICO
    # ==================================================

    grafico_df = pd.melt(

        projecoes,

        id_vars="🏢 Setor",

        value_vars=[
            "📈 5 Anos",
            "🚀 10 Anos",
            "💎 15 Anos"
        ],

        var_name="Período",

        value_name="Valor"
    )

    fig = px.line(

        grafico_df,

        x="Período",

        y="Valor",

        color="🏢 Setor",

        markers=True,

        title="📊 Evolução Financeira Projetada"
    )

    st.plotly_chart(
        fig,
        width='stretch'
    )

    # ==================================================
    # PARECER IA
    # ==================================================

    melhor = top3.iloc[0]

    st.success(
        f"""
        ✅ Projeção Inteligente:

        O setor de **{melhor['setor']}**
        apresenta atualmente o maior potencial
        de crescimento econômico no cenário
        {cenario.lower()}.

        O sistema identificou:

        • boa capacidade de expansão
        • potencial de escalabilidade
        • oportunidade estratégica elevada
        • crescimento sustentável no longo prazo
        """
    )