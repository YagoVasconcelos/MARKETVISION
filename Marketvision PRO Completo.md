# MarketVision PRO

## Visão Geral

O MarketVision PRO é uma plataforma de inteligência mercadológica desenvolvida em Python com Streamlit, focada em análise estratégica empresarial baseada em Big Data.

O sistema foi projetado para transformar bases empresariais em informações estratégicas capazes de auxiliar:

- análise de mercado
- identificação de oportunidades
- estudo de concorrência
- viabilidade econômica
- inteligência regional
- projeções de investimento
- tomada de decisão empresarial

---

# Objetivo do Sistema

O objetivo do MarketVision PRO é permitir que o usuário:

- carregue bases empresariais em CSV
- filtre cidades e setores
- visualize indicadores estratégicos
- descubra setores promissores
- analise concorrência regional
- simule investimentos
- receba recomendações automáticas
- visualize oportunidades por região

---

# Arquitetura do Projeto

```bash
MarketVision_PRO/
│
├── app.py
│
├── assets/
│   └── logo.png
│
├── styles/
│   └── style.css
│
├── data/
│   └── raw/
│       ├── empresas.csv
│       └── uploads/
│
├── services/
│   ├── loader.py
│   ├── filters.py
│   ├── charts.py
│   ├── analytics.py
│   └── ai_insights.py
│
└── README.md
```

---

# Tecnologias Utilizadas

## Backend

- Python
- Pandas
- NumPy
- Plotly
- Streamlit

## Frontend

- Streamlit UI
- CSS customizado
- Plotly Interactive Charts

## Processamento

- Data Analytics
- Score Estratégico
- Inteligência Regional
- Simulação Econômica

---

# Funcionalidades do Sistema

# 1. Upload Inteligente de Bases

O sistema permite importar arquivos CSV contendo dados empresariais.

## Recursos:

- upload direto pela sidebar
- salvamento automático
- histórico de uploads
- carregamento de bases anteriores
- cache inteligente
- padronização automática de colunas

---

# 2. Sistema de Filtros Dinâmicos

O usuário pode filtrar:

- cidades
- setores empresariais

Os filtros atualizam automaticamente:

- gráficos
- tabelas
- métricas
- mapas
- score estratégico
- ranking
- insights

---

# 3. Dashboard Estratégico

O dashboard principal apresenta:

## Métricas

- total de empresas
- setores ativos
- quantidade de cidades

## Gráficos

### Distribuição Empresarial

Exibe a distribuição dos setores empresariais.

### Capital Médio

Mostra o capital médio por setor.

### Inteligência Geográfica

Mapa interativo com:

- latitude
- longitude
- CNPJ
- setor
- capital social
- cidade

---

# 4. Consultoria Estratégica Inteligente

A aba Insights funciona como um núcleo analítico do sistema.

Ela realiza análises automáticas sobre:

- estabilidade empresarial
- concorrência
- viabilidade econômica
- oportunidades regionais
- compatibilidade de investimento

---

# Sistema Analítico

# Sobrevivência Empresarial

O sistema calcula:

```python
idade_empresa = data_atual - data_abertura
```

Depois calcula:

```python
média da idade das empresas por setor
```

## O que isso representa?

A sobrevivência empresarial mede:

- estabilidade do setor
- maturidade do mercado
- risco operacional
- longevidade das empresas

## Interpretação

| Sobrevivência Alta | Sobrevivência Baixa |
|---|---|
| Mercado estável | Mercado instável |
| Empresas duram mais | Empresas fecham rápido |
| Menor risco | Maior risco |
| Setor maduro | Setor volátil |

---

# Aberturas Recentes

O sistema identifica empresas abertas nos últimos 2 anos.

Objetivo:

- detectar crescimento de mercado
- identificar tendências
- medir aquecimento do setor

---

# Score Estratégico Inteligente

O principal recurso do sistema é o cálculo do Score Estratégico.

O score é um índice de oportunidade mercadológica.

Ele varia de:

```text
0 → mercado ruim
100 → mercado extremamente favorável
```

---

# Como o Score é Calculado

O score utiliza múltiplos fatores.

## 1. Sobrevivência Empresarial

Peso:

```text
35%
```

Quanto maior a estabilidade do setor:

- maior o score
- menor o risco

---

## 2. Concorrência

Peso:

```text
25%
```

Quanto menor a concorrência:

- maior a oportunidade
- maior o score

---

## 3. Capital Médio

Peso:

```text
15%
```

Setores que exigem menor capital tendem a facilitar entrada no mercado.

---

## 4. Compatibilidade de Investimento

Peso:

```text
25%
```

O sistema compara:

```python
capital do usuário
vs
capital médio do setor
```

Objetivo:

descobrir se o investimento do usuário é compatível com o setor analisado.

---

# Inteligência do Simulador

O simulador não utiliza valores fixos.

Ele recalcula dinamicamente:

- ranking
- score
- setor líder
- recomendações
- classificação estratégica

Toda vez que o usuário altera:

```text
Investimento pretendido
```

O sistema recalcula automaticamente a viabilidade dos setores.

---

# Fórmula Geral do Score

```python
score = (
    sobrevivencia * 35
    + concorrencia * 25
    + capital * 15
    + fit_investimento * 25
)
```

---

# Classificação Automática

O sistema classifica automaticamente os setores.

## Níveis

| Score | Classificação |
|---|---|
| 0 → 40 | 🔴 Baixa oportunidade |
| 40 → 70 | 🟡 Média oportunidade |
| 70 → 100 | 🟢 Alta oportunidade |

---

# Sistema de Risco

O sistema também calcula o risco do mercado.

Baseado em:

- quantidade de concorrentes
- saturação do setor

## Classificações

| Concorrência | Risco |
|---|---|
| Baixa | Baixo |
| Média | Médio |
| Alta | Alto |

---

# Melhor Oportunidade Atual

O sistema identifica automaticamente:

- setor mais promissor
- melhor equilíbrio estratégico
- menor concorrência relativa
- maior estabilidade
- melhor compatibilidade econômica

---

# Regiões Mais Promissoras

O sistema calcula oportunidades por cidade.

## Critérios:

- quantidade de empresas
- capital médio regional
- saturação empresarial

Objetivo:

identificar regiões com:

- menor concorrência
- maior potencial de entrada
- melhor viabilidade regional

---

# Tabelas Inteligentes

As tabelas do sistema possuem:

- nomes profissionais
- ícones estratégicos
- tooltips explicativos
- gradiente visual
- colunas descritivas
- barras de progresso

Ao passar o mouse sobre uma coluna:

o sistema explica:

- significado
- objetivo
- função estratégica

---

# Gauge Estratégico

O Gauge mostra visualmente:

- nível de oportunidade do setor
- intensidade estratégica
- qualidade do mercado

## Cores

| Cor | Significado |
|---|---|
| Vermelho | Mercado desfavorável |
| Amarelo | Mercado moderado |
| Verde | Mercado favorável |

---

# Sistema de Parecer Inteligente

O sistema gera pareceres automáticos.

Exemplos:

- mercado favorável
- mercado competitivo
- alto risco operacional
- oportunidade estratégica elevada

Isso transforma os dados em:

- interpretação automática
- leitura executiva
- consultoria inteligente

---

# Inteligência Geográfica

O mapa estratégico permite:

- visualizar empresas
- detectar concentrações
- estudar regiões
- analisar expansão regional
- identificar polos econômicos

---

# Histórico de Uploads

Todos os arquivos importados são armazenados automaticamente.

Isso permite:

- reabrir bases antigas
- comparar cenários
- manter histórico operacional

---

# Objetivo Estratégico do Projeto

O MarketVision PRO não é apenas um dashboard.

O sistema evoluiu para:

```text
Plataforma de Inteligência Estratégica Empresarial
```

Com foco em:

- Business Intelligence
- Big Data
- Inteligência de Mercado
- Analytics
- Estratégia Empresarial
- Viabilidade Econômica
- Consultoria Inteligente

---

# Futuras Expansões

## Planejadas

- IA preditiva
- Machine Learning
- previsão de falência
- recomendação automática de cidades
- heatmaps inteligentes
- análise CNAE avançada
- dashboards executivos
- exportação PDF
- relatórios automáticos
- painel de tendências
- detecção de crescimento econômico
- análise temporal
- clusterização empresarial

---

# Desenvolvido por

Yago Marinho - Soluções Tecnologicas - TecPrimus

MarketVision PRO ©