import requests


def obter_cenario_economico():

    try:

        # ==================================================
        # SELIC
        # ==================================================

        selic_url = (
            "https://api.bcb.gov.br/dados/serie/"
            "bcdata.sgs.432/dados/ultimos/1?formato=json"
        )

        # ==================================================
        # IPCA
        # ==================================================

        ipca_url = (
            "https://api.bcb.gov.br/dados/serie/"
            "bcdata.sgs.433/dados/ultimos/1?formato=json"
        )

        # ==================================================
        # DÓLAR
        # ==================================================

        dolar_url = (
            "https://api.bcb.gov.br/dados/serie/"
            "bcdata.sgs.1/dados/ultimos/1?formato=json"
        )

        # ==================================================
        # REQUESTS
        # ==================================================

        selic = requests.get(selic_url).json()

        ipca = requests.get(ipca_url).json()

        dolar = requests.get(dolar_url).json()

        # ==================================================
        # RETORNO
        # ==================================================

        return {

            "inflacao": float(
                ipca[0]["valor"].replace(",", ".")
            ),

            "selic": float(
                selic[0]["valor"].replace(",", ".")
            ),

            "dolar": float(
                dolar[0]["valor"].replace(",", ".")
            ),

            # temporário até integrar IBGE
            "pib": 2.5,

            # temporário IA
            "estabilidade": 75
        }

    except:

        return {

            "inflacao": 5.2,

            "selic": 10.5,

            "dolar": 5.40,

            "pib": 2.3,

            "estabilidade": 70
        }