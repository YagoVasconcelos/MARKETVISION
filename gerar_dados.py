import pandas as pd
import numpy as np
import os

def gerar_base_para_final():
    # Coordenadas Reais baseadas na sua lista (Fim do erro do oceano)
    municipios_pa = {
        "Abaetetuba": [-1.724, -48.887], "Abel Figueiredo": [-4.953, -48.397], "Acará": [-1.961, -48.198],
        "Afuá": [-0.156, -50.386], "Água Azul do Norte": [-6.782, -50.481], "Alenquer": [-1.947, -54.738],
        "Almeirim": [-1.523, -52.581], "Altamira": [-3.203, -52.206], "Anajás": [-0.987, -49.940],
        "Ananindeua": [-1.365, -48.371], "Anapu": [-3.472, -51.201], "Augusto Corrêa": [-1.021, -46.634],
        "Aurora do Pará": [-2.126, -47.556], "Aveiro": [-3.608, -55.332], "Bagre": [-1.901, -50.164],
        "Baião": [-2.793, -49.676], "Bannach": [-7.346, -50.517], "Barcarena": [-1.505, -48.625],
        "Belém": [-1.455, -48.504], "Belterra": [-3.054, -54.945], "Benevides": [-1.361, -48.246],
        "Bom Jesus do Tocantins": [-5.016, -48.605], "Bonito": [-1.363, -47.306], "Bragança": [-1.053, -46.765],
        "Brasil Novo": [-3.261, -52.518], "Brejo Grande do Araguaia": [-5.698, -48.514], "Breu Branco": [-3.754, -49.564],
        "Breves": [-1.681, -50.481], "Bujaru": [-1.515, -48.041], "Cachoeira do Piriá": [-1.758, -46.541],
        "Cachoeira do Arari": [-1.011, -48.963], "Cametá": [-2.244, -49.495], "Canaã dos Carajás": [-6.497, -49.876],
        "Capanema": [-1.196, -47.181], "Capitão Poço": [-1.746, -47.059], "Castanhal": [-1.297, -47.927],
        "Chaves": [0.156, -49.910], "Colares": [-0.931, -48.283], "Conceição do Araguaia": [-8.257, -49.264],
        "Concórdia do Pará": [-1.992, -47.951], "Cumaru do Norte": [-7.831, -50.781], "Curionópolis": [-6.102, -49.598],
        "Curralinho": [-1.815, -49.794], "Curuá": [-1.905, -54.116], "Curuçá": [-0.731, -47.850],
        "Dom Eliseu": [-4.285, -47.501], "Eldorado do Carajás": [-6.104, -49.355], "Faro": [-2.173, -56.745],
        "Floresta do Araguaia": [-7.781, -49.397], "Garrafão do Norte": [-2.221, -47.051], "Goianésia do Pará": [-3.845, -49.096],
        "Gurupá": [-1.405, -51.645], "Igarapé-Açu": [-1.127, -47.621], "Igarapé-Miri": [-1.976, -48.961],
        "Inhangapi": [-1.428, -47.918], "Ipixuna do Pará": [-2.561, -47.498], "Irituia": [-1.771, -47.438],
        "Itaituba": [-4.276, -55.983], "Itupiranga": [-5.134, -49.326], "Jacareacanga": [-6.221, -57.761],
        "Jacundá": [-4.451, -49.116], "Juruti": [-2.152, -56.096], "Limoeiro do Ajuru": [-1.895, -49.381],
        "Mãe do Rio": [-2.051, -47.551], "Magalhães Barata": [-0.796, -47.596], "Marabá": [-5.361, -49.125],
        "Maracanã": [-0.766, -47.451], "Marapanim": [-0.718, -47.631], "Marituba": [-1.355, -48.341],
        "Medicilândia": [-3.444, -52.886], "Melgaço": [-1.661, -50.716], "Mocajuba": [-2.584, -49.507],
        "Moju": [-1.884, -48.768], "Mojuí dos Campos": [-2.682, -54.642], "Monte Alegre": [-2.007, -54.069],
        "Muaná": [-1.528, -49.216], "Nova Esperança do Piriá": [-2.262, -46.966], "Nova Ipixuna": [-4.912, -49.311],
        "Nova Timboteua": [-1.208, -47.391], "Novo Progresso": [-7.017, -55.381], "Novo Repartimento": [-4.251, -49.941],
        "Óbidos": [-1.917, -55.518], "Oeiras do Pará": [-2.003, -49.854], "Oriximiná": [-1.766, -55.866],
        "Ourém": [-1.552, -47.111], "Ourilândia do Norte": [-6.754, -51.091], "Pacajá": [-3.837, -50.636],
        "Palestina do Pará": [-5.742, -48.318], "Paragominas": [-2.996, -47.352], "Parauapebas": [-6.067, -49.902],
        "Pau D'Arco": [-7.531, -50.051], "Peixe-Boi": [-1.192, -47.311], "Piçarra": [-6.442, -48.871],
        "Placas": [-3.868, -54.221], "Ponta de Pedras": [-1.385, -48.841], "Portel": [-1.936, -50.821],
        "Porto de Moz": [-1.748, -52.238], "Prainha": [-1.808, -53.483], "Primavera": [-0.941, -47.098],
        "Quatipuru": [-0.896, -47.003], "Redenção": [-8.026, -50.031], "Rio Maria": [-7.312, -50.021],
        "Rondon do Pará": [-4.776, -48.066], "Rurópolis": [-4.095, -54.908], "Salinópolis": [-0.613, -47.356],
        "Salvaterra": [-0.756, -48.516], "Santa Bárbara do Pará": [-1.226, -48.291], "Santa Cruz do Arari": [-0.665, -49.176],
        "Santa Izabel do Pará": [-1.298, -48.161], "Santa Luzia do Pará": [-1.515, -46.911], "Santa Maria das Barreiras": [-8.868, -49.711],
        "Santa Maria do Pará": [-1.353, -47.576], "Santana do Araguaia": [-9.442, -50.331], "Santarém": [-2.443, -54.708],
        "Santarém Novo": [-0.928, -47.396], "Santo Antônio do Tauá": [-1.152, -48.128], "São Caetano de Odivelas": [-0.751, -48.016],
        "São Domingos do Araguaia": [-5.538, -48.731], "São Domingos do Capim": [-1.674, -47.771], "São Félix do Xingu": [-6.643, -51.991],
        "São Francisco do Pará": [-1.168, -47.796], "São Geraldo do Araguaia": [-6.401, -48.538], "São João da Ponta": [-0.852, -47.921],
        "São João de Pirabas": [-0.771, -47.171], "São João do Araguaia": [-5.358, -48.788], "São Miguel do Guamá": [-1.626, -47.483],
        "São Sebastião da Boa Vista": [-1.718, -49.541], "Sapucaia": [-6.945, -49.681], "Senador José Porfírio": [-2.586, -51.948],
        "Soure": [-0.716, -48.523], "Tailândia": [-2.946, -48.953], "Terra Alta": [-1.038, -47.913],
        "Terra Santa": [-2.105, -56.486], "Tomé-Açu": [-2.418, -48.151], "Tracuateua": [-1.076, -46.906],
        "Trairão": [-4.573, -55.941], "Tucumã": [-6.748, -50.051], "Tucuruí": [-3.764, -49.673],
        "Ulianópolis": [-3.743, -47.331], "Uruará": [-3.718, -53.736], "Vigia": [-0.858, -48.143],
        "Viseu": [-1.197, -46.141], "Vitória do Xingu": [-2.882, -52.006], "Xinguara": [-7.097, -49.944]
    }

    setores = ["Alimentação", "Vestuário", "Tecnologia", "Serviços (MEI)", "Logística", "Saúde"]
    data = []
    
    print("🚀 Gerando Base de Dados com os 144 municípios do Pará...")

    for _ in range(8000):
        cidade = np.random.choice(list(municipios_pa.keys()))
        coords = municipios_pa[cidade]
        setor = np.random.choice(setores)
        
        # Capital Social (Mínimo R$ 1.000 para MEI)
        inv_inicial = np.random.uniform(1000, 25000) if "MEI" in setor else np.random.uniform(20000, 450000)
        anos = np.random.randint(1, 15)
        cap_atual = inv_inicial * (1 + (np.random.uniform(0.05, 0.18) * anos))

        # Dispersão mínima de 0.006 para ficar no centro urbano
        data.append({
            "cnpj": f"{np.random.randint(10,99)}.{np.random.randint(100,999)}/0001-{np.random.randint(10,99)}",
            "empresa": f"{np.random.choice(['J.P.', 'M.S.', 'A.C.'])} {setor.upper()} LTDA",
            "setor": setor,
            "cidade": cidade,
            "regiao": "Pará",
            "capital_social": round(cap_atual, 2),
            "investimento_inicial": round(inv_inicial, 2),
            "anos_atividade": anos,
            "lat": coords[0] + np.random.uniform(-0.003, 0.003),
            "lon": coords[1] + np.random.uniform(-0.003, 0.003)
        })

    df = pd.DataFrame(data)
    if not os.path.exists("data"): 
        os.makedirs("data")
    
    df.to_csv("data/exemplo.csv", index=False)
    print("✅ SUCESSO: Base oficial do Pará gerada!")

if __name__ == "__main__":
    gerar_base_para_final()