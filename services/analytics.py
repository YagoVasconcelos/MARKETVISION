import pandas as pd


def calcular_sobrevivencia(df):

    if 'data_abertura' not in df.columns:
        return pd.Series()

    df = df.copy()

    df["idade_anos"] = (
        pd.Timestamp.now() -
        pd.to_datetime(df["data_abertura"])
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
        pd.to_datetime(df["data_abertura"])
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