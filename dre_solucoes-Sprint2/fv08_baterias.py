# FV08 - Incluir baterias e calcular a capacidade para a autonomia desejada
import math

DIAS_MES = 30


# T01 - pergunta se quer armazenamento e qual a autonomia
def perguntar_armazenamento():
    print("\n--- ARMAZENAMENTO ---")
    if input("O cliente quer banco de baterias? (s/n): ").strip().lower() != "s":
        return None
    while True:
        texto = input("Autonomia desejada em horas: ").strip().replace(",", ".")
        try:
            horas = float(texto)
        except ValueError:
            horas = -1
        if 0 < horas <= 72:
            return horas
        print("A autonomia tem que ser maior que zero e no máximo 72 horas.")


def mostrar_baterias(baterias):
    print("\n--- BATERIAS DISPONÍVEIS ---")
    for b in baterias:
        marca_kwh = " (calculado)" if b["kwh_calculado"] else ""
        marca_ef = " (adotado)" if b["eficiencia_adotada"] else ""
        print(f"[{b['id']}] {b['fabricante']} {b['modelo']} | {b['tecnologia']} | "
              f"{b['tensao']:g} V {b['ah']:.0f} Ah | {b['kwh']:.2f} kWh{marca_kwh} | "
              f"DoD {b['dod']:.0f}% | ef. {b['eficiencia']:.0f}%{marca_ef} | R$ {b['preco']:.2f}")


def escolher_bateria(baterias):
    mostrar_baterias(baterias)
    while True:
        texto = input("Número da bateria: ").strip()
        if texto.isdigit():
            for b in baterias:
                if b["id"] == int(texto):
                    return b
        print("Essa bateria não está na base.")


# T02 + T03 - E_d, E_autonomia, C_bat e N_bat
def dimensionar_banco(consumo_mensal_kwh, autonomia_horas, bateria):
    energia_diaria = consumo_mensal_kwh / DIAS_MES              # E_d
    energia_autonomia = energia_diaria * autonomia_horas / 24    # E_autonomia

    dod = bateria["dod"] / 100
    eficiencia = bateria["eficiencia"] / 100
    capacidade_necessaria = energia_autonomia / (dod * eficiencia)  # C_bat

    capacidade_util = bateria["kwh"] * dod
    quantidade = math.ceil(energia_autonomia / (capacidade_util * eficiencia))
    capacidade_instalada = round(quantidade * bateria["kwh"], 2)

    return {
        "bateria": bateria,
        "autonomia_horas": autonomia_horas,
        "energia_diaria_kwh": round(energia_diaria, 2),
        "energia_autonomia_kwh": round(energia_autonomia, 2),
        "capacidade_necessaria_kwh": round(capacidade_necessaria, 2),
        "capacidade_util_unitaria_kwh": round(capacidade_util, 2),
        "quantidade": quantidade,
        "capacidade_instalada_kwh": capacidade_instalada,
    }


def mostrar_banco(banco):
    print("\n--- BANCO DE BATERIAS ---")
    # T05 - sem armazenamento não há banco
    if banco is None:
        print("Sistema dimensionado sem armazenamento.")
        return
    b = banco["bateria"]
    print(f"Autonomia pedida: {banco['autonomia_horas']:g} h")
    print(f"Consumo diário (E_d): {banco['energia_diaria_kwh']:.2f} kWh/dia")
    print(f"Energia de autonomia: {banco['energia_autonomia_kwh']:.2f} kWh")
    print(f"Capacidade necessária (C_bat): {banco['capacidade_necessaria_kwh']:.2f} kWh")
    print(f"Bateria escolhida: {b['fabricante']} {b['modelo']} "
          f"({b['kwh']:.2f} kWh, DoD {b['dod']:.0f}%)")
    print(f"Capacidade útil por unidade: {banco['capacidade_util_unitaria_kwh']:.2f} kWh")
    print(f"Quantidade de baterias: {banco['quantidade']}")
    print(f"Capacidade instalada: {banco['capacidade_instalada_kwh']:.2f} kWh")
    if b["kwh_calculado"]:
        print("Obs: capacidade em kWh calculada pelo sistema (fabricante não publica).")
    if b["eficiencia_adotada"]:
        print(f"Obs: eficiência de {b['eficiencia']:.0f}% adotada como premissa "
              f"(fabricante não publica).")
