import requests

def calcular_projecao_financeira(
    investimento,
    taxa_crescimento,
    anos
):

    """
    Calcula projeção financeira composta.

    VF = VP * (1 + i)^t

    Onde:

    VF = valor futuro
    VP = valor presente
    i  = taxa de crescimento
    t  = tempo
    """

    valor_futuro = (
        investimento *
        ((1 + taxa_crescimento) ** anos)
    )

    return round(
        valor_futuro,
        2
    )

def calcular_taxa_inteligente(row, economia):

    """
    Taxa IA dinâmica baseada em:
    • score estratégico
    • sobrevivência
    • concorrência
    • economia nacional/global
    """

    score = row["score"]

    sobrevivencia = row["sobrevivencia"]

    concorrencia = row["concorrencia"]

    # ==================================================
    # BASE
    # ==================================================

    taxa = 0.08

    # ==================================================
    # SCORE
    # ==================================================

    taxa += (score / 100) * 0.12

    # ==================================================
    # SOBREVIVÊNCIA
    # ==================================================

    taxa += min(
        sobrevivencia / 100,
        0.05
    )

    # ==================================================
    # CONCORRÊNCIA
    # ==================================================

    taxa -= min(
        concorrencia / 10000,
        0.04
    )

    # ==================================================
    # ECONOMIA
    # ==================================================

    inflacao = economia["inflacao"]

    selic = economia["selic"]

    pib = economia["pib"]

    estabilidade = economia["estabilidade"]

    dolar = economia["dolar"]

    # inflação reduz crescimento
    taxa -= inflacao / 100

    # selic reduz expansão
    taxa -= selic / 200

    # PIB melhora crescimento
    taxa += pib / 100

    # estabilidade melhora confiança
    taxa += estabilidade / 1000

    # dólar alto gera pequena pressão
    if dolar > 5:
        taxa -= 0.01

    # ==================================================
    # LIMITES
    # ==================================================

    taxa = max(0.03, taxa)

    taxa = min(0.45, taxa)

    return taxa

def calcular_risco_futuro(row):

    """
    Calcula risco econômico futuro
    baseado em indicadores estratégicos.
    """

    score = row["score"]

    concorrencia = row["concorrencia"]

    sobrevivencia = row["sobrevivencia"]

    capital = row["capital_medio"]

    risco = 0

    # ==================================================
    # CONCORRÊNCIA
    # ==================================================

    if concorrencia > 500:

        risco += 30

    elif concorrencia > 200:

        risco += 20

    else:

        risco += 10

    # ==================================================
    # SOBREVIVÊNCIA
    # ==================================================

    if sobrevivencia < 3:

        risco += 30

    elif sobrevivencia < 6:

        risco += 15

    else:

        risco += 5

    # ==================================================
    # SCORE
    # ==================================================

    if score < 40:

        risco += 30

    elif score < 70:

        risco += 15

    else:

        risco += 5

    # ==================================================
    # CAPITAL MUITO ALTO
    # ==================================================

    if capital > 1000000:

        risco += 20

    elif capital > 300000:

        risco += 10

    # ==================================================
    # LIMITES
    # ==================================================

    risco = min(risco, 100)

    # ==================================================
    # CLASSIFICAÇÃO
    # ==================================================

    if risco <= 30:

        nivel = "🟢 Baixo"

    elif risco <= 60:

        nivel = "🟡 Moderado"

    else:

        nivel = "🔴 Alto"

    return {

        "risco": risco,

        "nivel": nivel

    }

def calcular_cenario_economico():

    """
    Busca indicadores econômicos reais
    via Banco Central do Brasil.
    """

    try:

        # ==================================================
        # SELIC
        # ==================================================

        selic_url = (
            "https://api.bcb.gov.br/dados/serie/"
            "bcdata.sgs.432/dados/ultimos/1?formato=json"
        )

        # ==================================================
        # IPCA / INFLAÇÃO
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
        # DADOS ECONÔMICOS
        # ==================================================

        economia = {

            "inflacao": float(
                ipca[0]["valor"]
                .replace(",", ".")
            ),

            "selic": float(
                selic[0]["valor"]
                .replace(",", ".")
            ),

            "dolar": float(
                dolar[0]["valor"]
                .replace(",", ".")
            ),

            # temporário
            "pib": 2.5,

            # temporário
            "estabilidade": 75
        }

        return economia

    except:

        # ==================================================
        # FALLBACK
        # ==================================================

        return {

            "inflacao": 5.2,

            "selic": 10.5,

            "dolar": 5.40,

            "pib": 2.3,

            "estabilidade": 70
        }
    
def obter_indicadores_economicos():

    return {

        "dolar": 5.42,

        "selic": 10.50,

        "inflacao": 4.20,

        "pib": 2.10,

        "estabilidade": "Moderada"

    }

def calcular_impacto_setorial(setor, economia):

    """
    IA econômica setorial.
    Ajusta crescimento conforme economia.
    """

    setor = str(setor).lower()

    impacto = 0

    dolar = economia["dolar"]

    selic = economia["selic"]

    inflacao = economia["inflacao"]

    pib = economia["pib"]

    # ==================================================
    # TECNOLOGIA
    # ==================================================

    if "tecnologia" in setor:

        impacto += pib / 100

        impacto -= inflacao / 300

    # ==================================================
    # CONSTRUÇÃO
    # ==================================================

    elif "constr" in setor:

        impacto -= selic / 120

    # ==================================================
    # VAREJO
    # ==================================================

    elif "varejo" in setor:

        impacto -= inflacao / 150

    # ==================================================
    # AGRO
    # ==================================================

    elif "agro" in setor:

        if dolar > 5:
            impacto += 0.04

    # ==================================================
    # EXPORTAÇÃO
    # ==================================================

    elif "export" in setor:

        if dolar > 5:
            impacto += 0.05

    # ==================================================
    # LIMITES
    # ==================================================

    impacto = max(-0.08, impacto)

    impacto = min(0.10, impacto)

    return impacto