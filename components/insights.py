import streamlit as st
import plotly.graph_objects as go

from services.analytics import (
    calcular_sobrevivencia,
    calcular_aberturas_recentes,
    calcular_melhor_setor,
    calcular_score_oportunidade,
    calcular_regioes_oportunidade
)
from services.ai_insights import gerar_parecer

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

        score_df_view = score_df[[
            "setor",
            "score",
            "concorrencia",
            "capital_medio",
            "sobrevivencia",
            "nivel",
            "risco"
        ]].copy()

        score_df_view = score_df_view.rename(columns={

            "setor": "🏢 Setor",
            "score": "🎯 Score Estratégico",
            "concorrencia": "⚔️ Concorrência",
            "capital_medio": "💰 Capital Médio",
            "sobrevivencia": "📈 Sobrevivência",
            "nivel": "🚀 Nível",
            "risco": "🛡️ Risco"
        })

        st.dataframe(

            score_df_view.style
            .background_gradient(
                subset=["🎯 Score Estratégico"],
                cmap="RdYlGn"
            )
            .format({

                "🎯 Score Estratégico": "{:.2f}",
                "💰 Capital Médio": "R$ {:,.2f}",
                "📈 Sobrevivência": "{:.1f} anos"

            }),

            width='stretch',

            column_config={

                "🏢 Setor": st.column_config.TextColumn(
                    "🏢 Setor",
                    help="Segmento empresarial analisado."
                ),

                "🎯 Score Estratégico": st.column_config.ProgressColumn(
                    "🎯 Score Estratégico",
                    help="Índice geral calculado pela IA analítica." \
                    "O Score Estratégico é basicamente uma nota inteligente que o sistema cria para dizer: " \
                    " Quão boa é a oportunidade de investir nesse setor?" \
                    "Ele junta vários fatores do mercado e transforma tudo em uma pontuação de 0 a 100.",
                    min_value=0,
                    max_value=100,
                    format="%.2f"
                ),

                "⚔️ Concorrência": st.column_config.NumberColumn(
                    "⚔️ Concorrência",
                    help="Quantidade de empresas no setor.",
                    format="%d empresas"
                ),

                "💰 Capital Médio": st.column_config.NumberColumn(
                    "💰 Capital Médio",
                    help="Média de capital social do setor.",
                    format="R$ %.2f"
                ),

                "📈 Sobrevivência": st.column_config.NumberColumn(
                    "📈 Sobrevivência",
                    help="Tempo médio de sobrevivência.",
                    format="%.1f anos"
                ),

                "🚀 Nível": st.column_config.TextColumn(
                    "🚀 Nível",
                    help="Classificação estratégica automática."
                ),

                "🛡️ Risco": st.column_config.TextColumn(
                    "🛡️ Risco",
                    help="Nível de risco do mercado."
                )

            }
        )

        st.bar_chart(
            score_df.set_index("setor")["score"]
        )

        top = score_df.iloc[0]

        score_visual = min(
            top["score"],
            100
        )

        gauge = go.Figure(
            go.Indicator(
                mode="gauge+number",

                value=score_visual,

                title={
                    "text": "Score Estratégico"
                },

                gauge={

                    "axis": {
                        "range": [0, 100]
                    },

                    "bar": {
                        "color": "#00ffaa"
                    },

                    "steps": [

                        {
                            "range": [0, 30],
                            "color": "#d60b0b"
                        },

                        {
                            "range": [30, 70],
                            "color": "#e0bc1b"
                        },

                        {
                            "range": [70, 100],
                            "color": "#0caf3d"
                        }

                    ]
                }
            )
        )

        gauge.update_layout(
            height=300,
            margin=dict(
                l=20,
                r=20,
                t=60,
                b=20
            )
        )

        st.plotly_chart(
            gauge,
            width='stretch',
        )

        # ==================================================
        # INTERPRETAÇÃO AUTOMÁTICA DO SCORE
        # ==================================================

        parecer = gerar_parecer(
            top["score"]
        )

        if parecer["cor"] == "success":
            st.success(parecer["texto"])

        elif parecer["cor"] == "warning":
            st.warning(parecer["texto"])

        else:
            st.error(parecer["texto"])

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
            "🎯 Índice Estratégico",
            round(score_df["score"].max(), 2),

            help="""
            Índice calculado com base em:

            • concorrência regional
            • sobrevivência das empresas
            • capital médio do setor
            • potencial de mercado

            Quanto maior o score,
            melhor a oportunidade estratégica.
            """
        )

        k3.metric(
            "🔥 Setor Líder",
            score_df.iloc[0]["setor"]
        )

        st.subheader("🌎 Regiões Mais Promissoras")

        regioes = calcular_regioes_oportunidade(df_filtered)

        # ==================================================
        # TABELA REGIONAL INTELIGENTE
        # ==================================================

        regioes_view = regioes.rename(columns={

            "cidade": "🌎 Cidade",

            "empresas": "🏢 Empresas",

            "capital_medio": "💰 Capital Médio",

            "score_regiao": "🎯 Score Regional"

        })

        st.dataframe(

            regioes_view.style
            .background_gradient(
                subset=["🎯 Score Regional"],
                cmap="Blues"
            )
            .format({

                "💰 Capital Médio": "R$ {:,.2f}",

                "🎯 Score Regional": "{:.2f}"

            }),

            width='stretch',

            column_config={

                "🌎 Cidade": st.column_config.TextColumn(
                    "🌎 Cidade",
                    help="""
        Cidade analisada pelo sistema estratégico.

        Representa a região onde foram encontradas
        empresas compatíveis com os filtros atuais.
        """
                ),

                "🏢 Empresas": st.column_config.NumberColumn(
                    "🏢 Empresas",
                    help="""
        Quantidade de empresas encontradas na cidade.

        Menor quantidade pode indicar:
        • menor concorrência
        • mercado menos saturado
        • maior oportunidade de entrada
        """,
                    format="%d empresas"
                ),

                "💰 Capital Médio": st.column_config.NumberColumn(
                    "💰 Capital Médio",
                    help="""
        Média de capital social das empresas da região.

        Ajuda a identificar:
        • barreira financeira
        • nível econômico do mercado
        • dificuldade de entrada
        """,
                    format="R$ %.2f"
                ),

                "🎯 Score Regional": st.column_config.ProgressColumn(
                    "🎯 Score Regional",
                    help="""
        Índice estratégico calculado automaticamente.

        O sistema considera:
        • quantidade de empresas
        • capital médio regional
        • saturação do mercado

        Quanto maior o score:
        • melhor a oportunidade regional
        • menor a concorrência
        • maior potencial estratégico
        """,
                    min_value=0,
                    max_value=100,
                    format="%.2f"
                )

            }
        )

        st.bar_chart(
            regioes.set_index("cidade")["score_regiao"]
        )