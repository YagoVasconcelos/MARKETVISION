import streamlit as st
import folium
import pandas as pd
import streamlit as st
from streamlit_folium import st_folium
from services.analytics import (calcular_regioes_oportunidade)
from services.geocode import obter_coordenadas

@st.cache_data
def obter_coordenadas_cached(cidade):
    return obter_coordenadas(cidade)

def render_mapa_oportunidades(df):

    st.subheader("🗺️ Mapa Estratégico IA")

    if df.empty:

        st.warning(
            "Sem dados para gerar mapa."
        )

        return

    regioes = calcular_regioes_oportunidade(df)

    if regioes.empty:

        st.warning(
            "Não foi possível gerar regiões."
        )

        return

    # ==================================================
    # MAPA BASE BRASIL
    # ==================================================

    mapa = folium.Map(

        location=[-14.2350, -51.9253],

        zoom_start=4
    )

    # ==================================================
    # TOP 20 REGIÕES
    # ==================================================

    top = regioes.head(20)

    for _, row in top.iterrows():

        cidade = row["cidade"]

        score = round(
            row["score_regiao"],
            2
        )

        popup = f"""
        <b>{cidade}</b><br>
        Score Regional: {score}
        """

        coords = obter_coordenadas_cached(cidade)

        if not coords:
            continue

        lat = coords["lat"]

        lon = coords["lon"]

        folium.CircleMarker(

            location=[lat, lon],

            radius=10,

            popup=popup,

            color="green",

            fill=True,

            fill_opacity=0.7

        ).add_to(mapa)

    st_folium(
        mapa,
        width="100%",
        height=600,
        returned_objects=[]
    )