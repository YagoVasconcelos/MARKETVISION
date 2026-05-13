import plotly.express as px


def create_pie_chart(df):

    fig = px.pie(
        df,
        names='setor',
        hole=0.4
    )

    fig.update_layout(
        margin=dict(
            t=30,
            b=10,
            l=10,
            r=10
        ),
        height=350
    )

    return fig


def create_bar_chart(df):

    cap_setor = (
        df.groupby('setor')['capital_social']
        .mean()
        .reset_index()
    )

    fig = px.bar(
        cap_setor,
        x='setor',
        y='capital_social',
        color='setor',
        text_auto='.2s'
    )

    fig.update_layout(
        margin=dict(
            t=30,
            b=10,
            l=10,
            r=10
        ),
        height=350,
        showlegend=False
    )

    return fig


def create_map(df):

    fig = px.scatter_map(
        df,
        lat="lat",
        lon="lon",
        color="setor",
        size="capital_social",
        size_max=15,
        zoom=12,
        hover_name="empresa",
        custom_data=[
            "cnpj",
            "setor",
            "capital_social",
            "cidade"
        ],
        map_style="carto-darkmatter"
    )

    fig.update_traces(
        hovertemplate="""
        <b>%{hovertext}</b><br>
        <b>CNPJ:</b> %{customdata[0]}<br>
        <b>Setor:</b> %{customdata[1]}<br>
        <b>Capital:</b> R$ %{customdata[2]:,.2f}<br>
        <b>Cidade:</b> %{customdata[3]}
        <extra></extra>
        """
    )

    fig.update_layout(
        height=700,
        margin={
            "r":0,
            "t":0,
            "l":0,
            "b":0
        },
        legend=dict(
            orientation="h",
            yanchor="bottom",
            y=0.01,
            xanchor="left",
            x=0.01,
            bgcolor="rgba(0,0,0,0.5)"
        )
    )

    return fig