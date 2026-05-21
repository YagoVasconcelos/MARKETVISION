import requests


# ==================================================
# BUSCAR DADOS DA CIDADE
# ==================================================

def obter_dados_cidade(cidade):

    try:

        cidade = str(cidade).strip().lower()

        # ==================================================
        # API IBGE
        # ==================================================

        url = (
            "https://servicodados.ibge.gov.br/api/v1/"
            "localidades/municipios"
        )

        response = requests.get(
            url,
            timeout=15
        )

        response.raise_for_status()

        dados = response.json()

        # ==================================================
        # PROCURAR CIDADE EXATA
        # ==================================================

        cidade_data = None

        for item in dados:

            nome = item["nome"].strip().lower()

            if nome == cidade:

                cidade_data = item
                break

        # ==================================================
        # NÃO ENCONTROU
        # ==================================================

        if not cidade_data:

            return None

        # ==================================================
        # RESULTADO
        # ==================================================

        resultado = {

            "cidade": cidade_data["nome"],

            "estado": cidade_data["microrregiao"]
            ["mesorregiao"]["UF"]["sigla"],

            "regiao": cidade_data["microrregiao"]
            ["mesorregiao"]["UF"]["regiao"]["nome"],

            "mesorregiao": cidade_data["microrregiao"]
            ["mesorregiao"]["nome"],

            "microrregiao": cidade_data["microrregiao"]["nome"]

        }

        return resultado

    except Exception as e:

        print("Erro IBGE:", e)

        return None