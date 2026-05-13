import pandas as pd

def apply_filters(
    df,
    cidades=None,
    setor=None
):

    df_filtered = df.copy()

    # FILTRO CIDADE
    if cidades is not None and 'cidade' in df_filtered.columns:

        if len(cidades) > 0:

            df_filtered = df_filtered[
                df_filtered['cidade'].isin(cidades)
            ]

        else:

            df_filtered = df_filtered.iloc[0:0]

        df_filtered = df_filtered[
            df_filtered['cidade'].isin(cidades)
        ]

    # FILTRO SETOR
    if (
        setor
        and setor != "Todos"
        and 'setor' in df_filtered.columns
    ):

        df_filtered = df_filtered[
            df_filtered['setor'] == setor
        ]

    return df_filtered