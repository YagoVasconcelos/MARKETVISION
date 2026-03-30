import pandas as pd

def load_data(file):
    df = pd.read_csv(file)
    df.columns = df.columns.str.lower()
    return df

def get_kpis(df):
    return {
        "empresas": len(df),
        "setores": df['setor'].nunique() if 'setor' in df else 0,
        "cidades": df['cidade'].nunique() if 'cidade' in df else 0
    }

def oportunidades(df):
    setor_count = df['setor'].value_counts()
    return setor_count[setor_count < 5]

def crescimento(df):
    df['crescimento'] = (df.index % 10) * 10
    return df.groupby('setor')['crescimento'].mean().reset_index()