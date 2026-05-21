import requests


def obter_coordenadas(cidade):

    """
    Busca latitude e longitude
    via OpenStreetMap.
    """

    try:

        url = (
            "https://nominatim.openstreetmap.org/search"
        )

        params = {

            "city": cidade,

            "country": "Brazil",

            "format": "json",

            "limit": 1
        }

        headers = {
            "User-Agent": "marketvision-pro"
        }

        response = requests.get(
            url,
            params=params,
            headers=headers,
            timeout=10
        )

        dados = response.json()

        if dados:

            return {

                "lat": float(dados[0]["lat"]),

                "lon": float(dados[0]["lon"])
            }

    except:

        return None

    return None