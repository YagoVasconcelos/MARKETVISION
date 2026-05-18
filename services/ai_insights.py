def gerar_parecer(score):

    if score >= 80:

        return {
            "nivel": "EXPANSÃO ACELERADA",
            "cor": "success",
            "texto": """
Mercado extremamente favorável.

• baixa saturação
• alta sobrevivência
• excelente potencial de crescimento
• oportunidade premium de entrada
"""
        }

    elif score >= 60:

        return {
            "nivel": "MERCADO FAVORÁVEL",
            "cor": "success",
            "texto": """
Mercado saudável para investimento.

• concorrência controlada
• estabilidade operacional
• crescimento sustentável
"""
        }

    elif score >= 40:

        return {
            "nivel": "MERCADO MODERADO",
            "cor": "warning",
            "texto": """
Mercado competitivo.

• concorrência intermediária
• exige diferenciação
• análise regional recomendada
"""
        }

    else:

        return {
            "nivel": "MERCADO SATURADO",
            "cor": "error",
            "texto": """
Mercado com risco elevado.

• alta concorrência
• saturação regional
• oportunidade reduzida
"""
        }