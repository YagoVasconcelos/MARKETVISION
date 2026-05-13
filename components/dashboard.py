import streamlit as st
from services.charts import (
    create_pie_chart,
    create_bar_chart,
    create_map
)

def render_dashboard(df_filtered):

    m1, m2, m3 = st.columns(3)

    m1.metric("🏢 Empresas no Filtro", len(df_filtered))
    m2.metric(
        "📊 Setores Ativos",
        df_filtered['setor'].nunique()
        if 'setor' in df_filtered else 0
    )

    m3.metric(
        "🌍 Cidades",
        df_filtered['cidade'].nunique()
        if 'cidade' in df_filtered else 0
    )

    st.divider()

    c1, c2 = st.columns(2)

    with c1:

        with st.container(border=True):

            st.subheader("🏢 Distribuição")

            if not df_filtered.empty:

                fig = create_pie_chart(df_filtered)

                fig.update_layout(
                    margin=dict(t=30, b=10, l=10, r=10),
                    height=350
                )

                st.plotly_chart(
                    fig,
                    width='stretch',
                    key="p_main"
                )

            else:
                st.warning("Sem dados para exibir.")

    with c2:

        with st.container(border=True):

            st.subheader("💰 Capital Médio")

            if not df_filtered.empty:

                fig2 = create_bar_chart(df_filtered)

                fig2.update_layout(
                    margin=dict(t=30, b=10, l=10, r=10),
                    height=350,
                    showlegend=False
                )

                st.plotly_chart(
                    fig2,
                    width='stretch',
                    key="b_cap"
                )

            else:
                st.warning("Sem dados para exibir.")

    if (
        not df_filtered.empty and
        'lat' in df_filtered.columns and
        'lon' in df_filtered.columns
    ):

        with st.container(border=True):

            st.subheader("🗺️ Inteligência Geográfica")

            fig_mapa = create_map(df_filtered)

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
                margin={"r":0,"t":0,"l":0,"b":0}
            )

            st.plotly_chart(
                fig_mapa,
                width='stretch',
                key="mapa_final_v3"
            )