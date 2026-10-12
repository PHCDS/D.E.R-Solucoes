# FV06 - Saber a potência necessária e a quantidade de módulos
import math

DIAS_MES = 30

# T02 - rendimento global adotado (premissa de projeto, documentada no README)
# Cobre perdas de temperatura, sujeira, cabeamento, mismatch e inversor.
RENDIMENTO_GLOBAL = 0.78


# T01 - P_FV = E_FV / (HSP x 30 x rendimento)
def calcular_potencia_necessaria(energia_alvo_kwh, hsp, rendimento=RENDIMENTO_GLOBAL):
    kwp = energia_alvo_kwh / (hsp * DIAS_MES * rendimento)
    return round(kwp * 1000, 2)  # em Wp


# T03 - escolha do módulo dentro do dataset
def mostrar_modulos(modulos):
    print("\n--- MÓDULOS DISPONÍVEIS ---")
    for m in modulos:
        print(f"[{m['id']}] {m['fabricante']} {m['modelo']} | {m['potencia_wp']:.0f} Wp | "
              f"{m['eficiencia']:.1f}% | R$ {m['preco']:.2f}")


def buscar_modulo(modulos, modulo_id):
    for m in modulos:
        if m["id"] == modulo_id:
            return m
    return None


def escolher_modulo(modulos):
    mostrar_modulos(modulos)
    while True:
        texto = input("Número do módulo: ").strip()
        if texto.isdigit():
            modulo = buscar_modulo(modulos, int(texto))
            if modulo:
                return modulo
        print("Esse módulo não está na base.")


# T04 + T05 - N arredondado para cima e potência instalada recalculada
def dimensionar(energia_alvo_kwh, hsp, modulo, rendimento=RENDIMENTO_GLOBAL):
    potencia_necessaria = calcular_potencia_necessaria(energia_alvo_kwh, hsp, rendimento)
    quantidade = math.ceil(potencia_necessaria / modulo["potencia_wp"])
    potencia_instalada = round(quantidade * modulo["potencia_wp"], 2)
    geracao_estimada = round(potencia_instalada / 1000 * hsp * DIAS_MES * rendimento, 2)

    return {
        "potencia_necessaria_w": potencia_necessaria,
        "modulo": modulo,
        "quantidade": quantidade,
        "potencia_instalada_w": potencia_instalada,
        "geracao_estimada_kwh": geracao_estimada,
        "rendimento": rendimento,
    }


def mostrar_dimensionamento(d):
    m = d["modulo"]
    print("\n--- DIMENSIONAMENTO ---")
    print(f"Potência necessária: {d['potencia_necessaria_w']:.2f} Wp "
          f"({d['potencia_necessaria_w'] / 1000:.2f} kWp)")
    print(f"Módulo escolhido: {m['fabricante']} {m['modelo']} ({m['potencia_wp']:.0f} Wp)")
    print(f"Quantidade de módulos: {d['quantidade']}")
    print(f"Potência instalada: {d['potencia_instalada_w']:.2f} Wp "
          f"({d['potencia_instalada_w'] / 1000:.2f} kWp)")
    print(f"Geração estimada: {d['geracao_estimada_kwh']:.2f} kWh/mês")
