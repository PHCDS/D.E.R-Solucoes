# FV02 - Carregar os datasets a partir dos arquivos CSV
import csv
import os

PASTA = os.path.join(os.path.dirname(os.path.abspath(__file__)), "datasets")


class ErroDataset(Exception):
    pass


# T02 - converte e avisa quando a linha vem quebrada
def numero(linha, campo, arquivo, obrigatorio=True):
    texto = linha.get(campo, "").strip()
    if texto == "":
        if obrigatorio:
            raise ErroDataset(f"{arquivo}: linha {linha.get('id', '?')} sem o campo '{campo}'")
        return None
    try:
        return float(texto.replace(",", "."))
    except ValueError:
        raise ErroDataset(f"{arquivo}: '{texto}' não é número no campo '{campo}'")


def ler_csv(nome):
    caminho = os.path.join(PASTA, nome)
    # T03 - sem o arquivo o dimensionamento não começa
    if not os.path.exists(caminho):
        raise ErroDataset(f"Dataset '{nome}' não encontrado na pasta datasets/")
    with open(caminho, encoding="utf-8") as f:
        linhas = list(csv.DictReader(f))
    if not linhas:
        raise ErroDataset(f"Dataset '{nome}' está vazio")
    return linhas


# T01 - leitura dos três CSV
def carregar_modulos():
    lista = []
    for linha in ler_csv("modulos.csv"):
        lista.append({
            "id": int(linha["id"]),
            "fabricante": linha["fabricante"],
            "modelo": linha["modelo"],
            "potencia_wp": numero(linha, "potencia_wp", "modulos.csv"),
            "voc": numero(linha, "tensao_voc_v", "modulos.csv"),
            "vmp": numero(linha, "tensao_vmp_v", "modulos.csv"),
            "eficiencia": numero(linha, "eficiencia_pct", "modulos.csv"),
            "preco": numero(linha, "preco_brl", "modulos.csv"),
            "fornecedor": linha["fornecedor"],
        })
    return lista


def carregar_inversores():
    lista = []
    for linha in ler_csv("inversores.csv"):
        lista.append({
            "id": int(linha["id"]),
            "fabricante": linha["fabricante"],
            "modelo": linha["modelo"],
            "potencia_nominal": numero(linha, "potencia_nominal_w", "inversores.csv"),
            "potencia_max_fv": numero(linha, "potencia_max_fv_w", "inversores.csv"),
            "tensao_max": numero(linha, "tensao_max_entrada_v", "inversores.csv"),
            "mppt_min": numero(linha, "mppt_min_v", "inversores.csv"),
            "mppt_max": numero(linha, "mppt_max_v", "inversores.csv"),
            "qtd_mppt": int(numero(linha, "qtd_mppt", "inversores.csv")),
            "eficiencia": numero(linha, "eficiencia_pct", "inversores.csv"),
            "aceita_bateria": linha["aceita_bateria"].strip().lower() == "sim",
            "preco": numero(linha, "preco_brl", "inversores.csv"),
            "fornecedor": linha["fornecedor"],
        })
    return lista


def carregar_baterias():
    lista = []
    for linha in ler_csv("baterias.csv"):
        tensao = numero(linha, "tensao_nominal_v", "baterias.csv")
        ah = numero(linha, "capacidade_ah", "baterias.csv")
        kwh = numero(linha, "capacidade_kwh", "baterias.csv", obrigatorio=False)
        eficiencia = numero(linha, "eficiencia_pct", "baterias.csv", obrigatorio=False)
        litio = "litio" in linha["tecnologia"].lower()

        # campos que o fabricante não publica: o sistema completa e avisa
        kwh_calculado = kwh is None
        if kwh_calculado:
            kwh = tensao * ah / 1000
        eficiencia_adotada = eficiencia is None
        if eficiencia_adotada:
            eficiencia = 95.0 if litio else 85.0

        lista.append({
            "id": int(linha["id"]),
            "fabricante": linha["fabricante"],
            "modelo": linha["modelo"],
            "tecnologia": linha["tecnologia"],
            "tensao": tensao,
            "ah": ah,
            "kwh": round(kwh, 2),
            "kwh_calculado": kwh_calculado,
            "dod": numero(linha, "dod_pct", "baterias.csv"),
            "eficiencia": eficiencia,
            "eficiencia_adotada": eficiencia_adotada,
            "preco": numero(linha, "preco_brl", "baterias.csv"),
            "fornecedor": linha["fornecedor"],
        })
    return lista


def carregar_hsp():
    tabela = {}
    for linha in ler_csv("hsp_referencia.csv"):
        tabela[linha["regiao"]] = float(linha["hsp_medio_aproximado"])
    return tabela


def carregar_tudo():
    return {
        "modulos": carregar_modulos(),
        "inversores": carregar_inversores(),
        "baterias": carregar_baterias(),
        "hsp": carregar_hsp(),
    }
