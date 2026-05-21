import pandas as pd
from services.ibge_api import obter_dados_cidade
from services.pib_api import obter_pib_municipio

def calcular_sobrevivencia(df):

    if 'data_abertura' not in df.columns:
        return pd.Series()

    df = df.copy()

    df["idade_anos"] = (
        pd.Timestamp.now() -
        pd.to_datetime(
            df["data_abertura"],
            errors="coerce"
        )
    ).dt.days / 365

    sobrevivencia = (
        df.groupby("setor")["idade_anos"]
        .mean()
        .sort_values(ascending=False)
    )

    return sobrevivencia


def calcular_aberturas_recentes(df):

    if 'data_abertura' not in df.columns:
        return pd.Series()

    df = df.copy()

    df["idade_anos"] = (
        pd.Timestamp.now() -
        pd.to_datetime(df["data_abertura"], errors="coerce")
    ).dt.days / 365

    recentes = df[df["idade_anos"] <= 2]

    return recentes["setor"].value_counts()


def calcular_melhor_setor(df):

    if (
        df.empty or
        'setor' not in df.columns or
        'capital_social' not in df.columns
    ):
        return None

    stats = (
        df.groupby('setor')
        .agg({
            'capital_social': 'mean',
            'setor': 'count'
        })
        .rename(columns={'setor': 'qtd'})
        .reset_index()
    )

    if stats.empty:
        return None

    melhor = stats.sort_values(by='qtd').iloc[0]

    return melhor

def calcular_score_oportunidade(df, meu_capital):

    if df.empty:
        return pd.DataFrame()

    df = df.copy()

    # ==================================================
    # BONUS REGIONAL IA
    # ==================================================

    df["bonus_regional"] = 0

    # ==================================================
    # IA REGIONAL POR CIDADE
    # ==================================================

    if "cidade" in df.columns:

        for idx, row in df.iterrows():

            cidade = row["cidade"]

            cidade_info = obter_dados_cidade(cidade)

            bonus = 0

            potencial = 0

            pib_bonus = 0

            if cidade_info:

                regiao = cidade_info["regiao"]

                cidade_id = cidade_info.get("id")

                potencial = calcular_potencial_regional(regiao)

                # ==================================================
                # BONUS REGIONAL
                # ==================================================

                if regiao == "Norte":
                    bonus += 8

                elif regiao == "Nordeste":
                    bonus += 6

                elif regiao == "Centro-Oeste":
                    bonus += 7

                elif regiao == "Sul":
                    bonus += 5

                elif regiao == "Sudeste":
                    bonus += 4

                # ==================================================
                # PIB MUNICIPAL
                # ==================================================

                if cidade_info:

                    regiao = cidade_info["regiao"]

                    cidade_id = cidade_info.get("id")

                    potencial = calcular_potencial_regional(regiao)

                    # bônus regional
                    if regiao == "Norte":
                        bonus += 8

                    elif regiao == "Nordeste":
                        bonus += 6

                    elif regiao == "Centro-Oeste":
                        bonus += 7

                    elif regiao == "Sul":
                        bonus += 5

                    elif regiao == "Sudeste":
                        bonus += 4

                    # PIB municipal
                    if cidade_id:

                        pib = obter_pib_municipio(cidade_id)

                        if pib:

                            if pib > 50000:
                                pib_bonus += 10

                            elif pib > 30000:
                                pib_bonus += 7

                            elif pib > 15000:
                                pib_bonus += 5

                            else:
                                pib_bonus += 2

                df.at[idx, "bonus_regional"] = (
                    bonus +
                    potencial +
                    pib_bonus
                )

    # idade empresa
    df["idade_anos"] = (
        pd.Timestamp.now() -
        pd.to_datetime(df["data_abertura"], errors="coerce")
    ).dt.days / 365

    # agrupamento estratégico
    score_df = (
        df.groupby("setor")
        .agg({
            "capital_social": "mean",
            "idade_anos": "mean",
            "setor": "count",
            "bonus_regional": "mean"
        })
    )

    score_df.columns = [
        "capital_medio",
        "sobrevivencia",
        "concorrencia",
        "bonus_regional"
    ]

    # compatibilidade do investimento do usuário
    score_df["fit_investimento"] = 1 - abs(

        meu_capital - score_df["capital_medio"]

    ) / (

        score_df["capital_medio"] + 1

    )

    # SCORE INTELIGENTE
    # NORMALIZAÇÃO DOS DADOS

    score_df["sobrevivencia_norm"] = (
        score_df["sobrevivencia"] /
        score_df["sobrevivencia"].max()
    )

    score_df["concorrencia_norm"] = 1 - (
        score_df["concorrencia"] /
        score_df["concorrencia"].max()
    )

    score_df["capital_norm"] = 1 - (
        score_df["capital_medio"] /
        score_df["capital_medio"].max()
    )

    # NORMALIZAÇÃO DO FIT DE INVESTIMENTO

    score_df["fit_investimento"] = (
        score_df["fit_investimento"]
        /
        score_df["fit_investimento"].max()
    ).clip(0, 1)

    # SCORE FINAL (0-100)

    score_df["score"] = (

        score_df["sobrevivencia_norm"] * 35

        +

        score_df["concorrencia_norm"] * 25

        +

        score_df["capital_norm"] * 15

        +

        score_df["fit_investimento"] * 25

        +

        score_df["bonus_regional"]

    )

    score_df["nivel"] = pd.cut(
        score_df["score"],
        bins=[0, 40, 70, 100],
        labels=[
            "🔴 Baixa",
            "🟡 Média",
            "🟢 Alta"
        ]
    )

    score_df = score_df.sort_values(
        by="score",
        ascending=False
    )

    score_df["risco"] = pd.cut(
        score_df["concorrencia"],
        bins=[0, 20, 100, 999999],
        labels=[
            "Baixo",
            "Médio",
            "Alto"
        ]
    )

    score_df = score_df.sort_values(
        by="score",
        ascending=False
    )

    return score_df.reset_index()

def calcular_regioes_oportunidade(df):

    if (
        df.empty or
        'cidade' not in df.columns
    ):
        return pd.DataFrame()

    regioes = (
        df.groupby("cidade")
        .agg({
            "setor": "count",
            "capital_social": "mean"
        })
        .rename(columns={
            "setor": "empresas",
            "capital_social": "capital_medio"
        })
    )

    # SCORE REGIONAL
    regioes["score_regiao"] = (

        # menos empresas = melhor oportunidade
        (100 / (regioes["empresas"] + 1) * 0.6)

        +

        # menor capital médio = melhor entrada
        (100000 / (regioes["capital_medio"] + 1) * 0.4)

    )

    regioes = regioes.sort_values(
        by="score_regiao",
        ascending=False
    )

    return regioes.reset_index()

def calcular_potencial_regional(regiao):

    """
    IA territorial estratégica.
    """

    potenciais = {

        "Norte": 9,
        "Nordeste": 8,
        "Centro-Oeste": 10,
        "Sul": 7,
        "Sudeste": 6

    }

    return potenciais.get(regiao, 5)