# FV07 - Escolher um inversor compatível com os módulos selecionados

# margem de sobredimensionamento aceita do arranjo FV sobre a potência do inversor
FATOR_MAX = 1.3


# T01 + T02 - filtros de compatibilidade
def compativel(inversor, potencia_instalada_w, modulo, precisa_bateria=False):
    motivos = []

    if potencia_instalada_w > inversor["potencia_max_fv"]:
        motivos.append(f"arranjo de {potencia_instalada_w:.0f} W passa da entrada FV máxima "
                       f"({inversor['potencia_max_fv']:.0f} W)")

    if potencia_instalada_w > inversor["potencia_nominal"] * FATOR_MAX:
        motivos.append(f"arranjo passa de {FATOR_MAX:g}x a potência nominal "
                       f"({inversor['potencia_nominal']:.0f} W)")

    # a tensão de circuito aberto de um módulo já tem que caber na entrada
    if modulo["voc"] > inversor["tensao_max"]:
        motivos.append(f"Voc do módulo ({modulo['voc']:.1f} V) passa da tensão máxima "
                       f"({inversor['tensao_max']:.0f} V)")

    # tem que caber pelo menos uma string dentro da faixa de MPPT
    if not cabe_string_no_mppt(inversor, modulo):
        motivos.append(f"nenhuma string cabe na faixa de MPPT "
                       f"({inversor['mppt_min']:.0f}-{inversor['mppt_max']:.0f} V)")

    if precisa_bateria and not inversor["aceita_bateria"]:
        motivos.append("não aceita banco de baterias")

    return len(motivos) == 0, motivos


def cabe_string_no_mppt(inversor, modulo):
    # procura uma quantidade de módulos em série cuja Vmp fique dentro do MPPT
    # e cuja Voc não estoure a tensão máxima de entrada
    for n in range(1, 31):
        vmp = n * modulo["vmp"]
        voc = n * modulo["voc"]
        if inversor["mppt_min"] <= vmp <= inversor["mppt_max"] and voc <= inversor["tensao_max"]:
            return True
    return False


def modulos_por_string(inversor, modulo):
    melhor = 0
    for n in range(1, 31):
        vmp = n * modulo["vmp"]
        voc = n * modulo["voc"]
        if inversor["mppt_min"] <= vmp <= inversor["mppt_max"] and voc <= inversor["tensao_max"]:
            melhor = n
    return melhor


# T03 - descarta incompatível em vez de escolher pelo preço
def selecionar_inversor(inversores, potencia_instalada_w, modulo, precisa_bateria=False):
    compativeis = []
    descartados = []
    for inv in inversores:
        ok, motivos = compativel(inv, potencia_instalada_w, modulo, precisa_bateria)
        if ok:
            compativeis.append(inv)
        else:
            descartados.append((inv, motivos))

    if not compativeis:
        return None, descartados

    # entre os que servem, o mais barato
    escolhido = min(compativeis, key=lambda i: i["preco"])
    return escolhido, descartados


# T04 - aviso quando nenhum serve
def mostrar_inversor(inversor, descartados, potencia_instalada_w, modulo, precisa_bateria=False):
    print("\n--- INVERSOR ---")
    if inversor is None:
        print("Nenhum inversor do dataset atende esse arranjo.")
        if precisa_bateria:
            print("Lembre que com armazenamento só entra inversor híbrido.")
        print("Motivos dos descartes:")
        for inv, motivos in descartados[:5]:
            print(f"  {inv['fabricante']} {inv['modelo']}: {motivos[0]}")
        print("Opções: reduzir o percentual de atendimento ou escolher outro módulo.")
        return

    n_serie = modulos_por_string(inversor, modulo)
    print(f"{inversor['fabricante']} {inversor['modelo']}")
    print(f"Potência nominal: {inversor['potencia_nominal']:.0f} W | "
          f"Entrada FV máx: {inversor['potencia_max_fv']:.0f} W")
    print(f"Arranjo: {potencia_instalada_w:.0f} W "
          f"({potencia_instalada_w / inversor['potencia_nominal'] * 100:.0f}% da nominal)")
    print(f"MPPT {inversor['mppt_min']:.0f}-{inversor['mppt_max']:.0f} V | "
          f"até {n_serie} módulos em série por string")
    print(f"Aceita bateria: {'sim' if inversor['aceita_bateria'] else 'não'}")
    print(f"Preço: R$ {inversor['preco']:.2f} ({inversor['fornecedor']})")
    print(f"Descartados por incompatibilidade: {len(descartados)}")
