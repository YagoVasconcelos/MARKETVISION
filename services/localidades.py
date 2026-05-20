import requests


# ==================================================
# ESTADOS
# ==================================================

def obter_estados():

    url = (
        "https://servicodados.ibge.gov.br/api/v1/"
        "localidades/estados"
    )

    response = requests.get(url)

    dados = response.json()

    estados = sorted([

        estado["sigla"]

        for estado in dados

    ])

    return estados


# ==================================================
# CIDADES
# ==================================================

def obter_cidades(uf):

    if not uf:
        return []

    url = (
        f"https://servicodados.ibge.gov.br/api/v1/"
        f"localidades/estados/{uf}/municipios"
    )

    response = requests.get(url)

    dados = response.json()

    cidades = sorted([

        cidade["nome"]

        for cidade in dados

    ])

    return cidades