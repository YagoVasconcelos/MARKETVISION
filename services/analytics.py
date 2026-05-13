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
    score_df["fit_investimento"] = (

        meu_capital /

        (score_df["capital_medio"] + 1)

    )

    # SCORE INTELIGENTE
    score_df["score"] = (

        # Sobrevivência alta = bom
        (
            score_df["sobrevivencia"] * 0.5
        )

        +

        # Menos concorrência = bom
        (
            100 / (score_df["concorrencia"] + 1) * 0.3
        )

        +

        # Menor capital necessário = melhor oportunidade
        (
            100000 / (score_df["capital_medio"] + 1) * 0.2
        )

    )

    score_df["nivel"] = pd.cut(
        score_df["score"],
        bins=[0, 5, 15, 100],
        labels=[
            "Baixa Oportunidade",
            "Média Oportunidade",
            "Alta Oportunidade"
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