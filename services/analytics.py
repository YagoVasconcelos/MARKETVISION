import pandas as pd


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
            "setor": "count"
        })
    )

    score_df.columns = [
        "capital_medio",
        "sobrevivencia",
        "concorrencia"
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