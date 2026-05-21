import requests


def obter_pib_municipio(cidade_id):

    """
    Busca PIB municipal via IBGE.
    """

    try:

        url = (
            f"https://servicodados.ibge.gov.br/api/v3/"
            f"agregados/5938/periodos/2021/variaveis/37"
            f"?localidades=N6[{cidade_id}]"
        )

        response = requests.get(
            url,
            timeout=10
        )

        dados = response.json()

        valor = (
            dados[0]["resultados"][0]
            ["series"][0]["serie"]
        )

        pib = list(valor.values())[0]

        return float(pib)

    except:

        return None