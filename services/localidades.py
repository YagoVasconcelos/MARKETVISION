import requests


def obter_estados():

    url = (
        "https://servicodados.ibge.gov.br/api/v1/localidades/estados"
    )

    try:

        response = requests.get(
            url,
            timeout=10
        )

        response.raise_for_status()

        dados = response.json()

        estados = sorted([
            estado["sigla"]
            for estado in dados
        ])

        return estados

    except:

        # fallback seguro
        return [
            "AC", "AL", "AP", "AM", "BA",
            "CE", "DF", "ES", "GO", "MA",
            "MT", "MS", "MG", "PA", "PB",
            "PR", "PE", "PI", "RJ", "RN",
            "RS", "RO", "RR", "SC", "SP",
            "SE", "TO"
        ]


def obter_cidades(uf):

    url = (
        f"https://servicodados.ibge.gov.br/api/v1/"
        f"localidades/estados/{uf}/municipios"
    )

    try:

        response = requests.get(
            url,
            timeout=10
        )

        response.raise_for_status()

        dados = response.json()

        cidades = sorted([
            cidade["nome"]
            for cidade in dados
        ])

        return cidades

    except:

        return []